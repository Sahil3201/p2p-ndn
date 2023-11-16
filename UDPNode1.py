import socket
import threading
import random
import json
import Interfaces
import time

bufferSize  = 1024
file = open('interfaces.json')
references = json.load(file)

#Finds the node with the given name in the reference json and returns its index
def find_node(name):
    for i in range(len(references)):
        if(name == list(references[i].keys())[0]):
            return i

########### Setup #########
def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket

########## Update ##############
def update(interface,router,name):
    while True:
        interface.update()
        #Update content store with data
        router.setCS(name,interface.data,time.time())
        time.sleep(10)


########## Outbound #############
#Send interest packet
def outbound(socket,router,lock,interface):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        #Send to some neighbor given longest prefix protocol or FIB
        neighbor = router.longestPrefix(interest)
        packet = (interest, interface)
        router.setPit(interest,interface)
        print("Sending: ",json.dumps(packet).encode(), (neighbor[len(neighbor)-1][1],neighbor[len(neighbor)-1][2]))
        socket.sendto(json.dumps(packet).encode(), (neighbor[len(neighbor)-1][1],neighbor[len(neighbor)-1][2]))
        lock.release()
        #msgFromServer = socket.recvfrom(bufferSize)
        #print(msgFromServer[0].decode())


########## Inbound ##############
def fresh(name, router):
    if name in router.getCS():
        if (float(time.time() - router.getCS()[name][1])) > 10.0:
            print("Stale")
            return False
        else:
            print("Fresh")
            return True      

def handle_packet(router, packet,socket):
    print("HANDLING PACKET")
    packet = json.loads(packet.decode())
    name = packet[0]
    #Interest packet
    if len(packet) == 2:
        interface = packet[1]
        print("Interest Packet Received!")
        if name in router.getCS() and fresh(name,router):
            print("I have the Data!")
            #Produce data packet name : data : freshness
            address = router.getAddress(interface)
            packet = (name,router.getCS()[name],0)
            #print("Forward to " + interface)
            socket.sendto(json.dumps(packet).encode(), address)
            return
        elif packet not in router.getPit():
            print("I don't have the Data, updating PIT!")
            router.setPit(name,interface)
            print("PIT ", router.getPit())
            #Forward Interest based on longest prefix
            if router.getMultiRequest() ==  2:
                next_nodes = []
                for node in router.getFib():
                    if len(node[0].split("/")) != 4:
                        next_nodes.append(node)
                next_node = [random.choice(next_nodes)] 
                router.setMultiRequest()
            else:
                next_node = router.longestPrefix(name)
                router.updateMultiRequest()
            print("Forwarding to ", next_node[len(next_node)-1]) 
            packet = (name, router.getLocation()[0])
            socket.sendto(json.dumps(packet).encode(),(next_node[len(next_node)-1][1],next_node[len(next_node)-1][2]))
            return

    #Data packet
    else:
        print("Data packet Received!")
        data = packet[1]
        inPit = False
        #Remove elements in PIT which contain interest
        for interest in router.getPit(): 
            if interest[0] == name:
                print("Satisfying interest table")
                router.popPit(interest[0],interest[1])
                #Send data packet to requesters
                if interest[1] != router.name:
                    address = router.getAddress(interest[1])
                    socket.sendto(json.dumps(packet).encode(), address)
                inPit = True
        if inPit:
            print("Updating Content store")
            router.setCS(name,data[0],data[1])
            print(router.getCS())
            return
        else:
            print("Not in interest table, ignore packet.")
            return
    
    return

# Listen for incoming datagrams
def inbound(socket,name,lock,router):
    while(True):
        print("running inbound")
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        handle_packet(router,message,socket)
        lock.release()


class p2p_node():
    def __init__(self,name,router,interface):
        #Interface name
        self.name = name

        #Thread Mutex
        self.lock = threading.Lock()

        #Set router and interface class
        self.router = router
        self.interface = interface

        #Find network details from json
        index=find_node(name)   
        network_details = references[index][name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
    
    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)
        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock,self.router))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.router,self.lock,self.name))
        t3 = threading.Thread(target=update, args=(self.interface,self.router,self.name))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        t3.join()
