import socket
import threading
import random
import json
import time

bufferSize  = 1024
with open('interfaces.json') as file:
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
def outbound(socket,router,lock, addr_port):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        #Send to some neighbor given longest prefix protocol or FIB
        neighbor = router.longestPrefix(interest)
        packet = {"type": "interest", "dataname": interest, "addr_port": addr_port, "req_name": router.name} # interest packet
        router.setPit(interest, addr_port, router.name)
        print("Sending: ",json.dumps(packet).encode(), (neighbor[len(neighbor)-1][1],neighbor[len(neighbor)-1][2]))
        socket.sendto(json.dumps(packet).encode(), (neighbor[len(neighbor)-1][1],neighbor[len(neighbor)-1][2]))
        lock.release()
        #msgFromServer = socket.recvfrom(bufferSize)
        #print(msgFromServer[0].decode())


########## Inbound ##############
def fresh(name, router):
    if name in router.getCS():
        if (float(time.time() - router.getCS()[name][1])) > 10.0:
            # print("Stale")
            return False
        else:
            # print("Fresh")
            return True      

def handle_packet(router, packet, socket, interface):
    """
    interest packet: 
    packet = {"type": "interest", "dataname": dataname, "addr_port": (<ip>, <listenport>), "req_name":<requestor name>}

    Data packet:
    packet = {"type": "data", "dataname": dataname, "data": <data>, "freshness": <freshness in seconds>}

    Public key interest packet
    packet = {"type": "publicKeyRequest", "data":packet['req_name'], "return_address":(<ip address>, <listen port>)}
    
    Public Key data
    packet = {"type": "publicKeyPayload", "data": <publicKey>, "dataname": <public key's device name>}
    """
    print("HANDLING PACKET")
    packet = json.loads(packet.decode())
    print(router)
    #Interest packet
    if packet["type"] == "interest":
        name = packet["dataname"]
        sender_addr_port = packet["addr_port"]
        req_name = packet["req_name"]
        print("Interest Packet Received!")
        if name in router.getCS() and fresh(name,router):
            print("I have the Data!")
            #Produce data packet name : data : freshness
            # packet = (name, router.getCS()[name], 0)
            router.setPit(packet['dataname'], sender_addr_port, packet['req_name'], True)
            packet = {"type": "publicKeyRequest", "data":packet['req_name'], "return_address":(router.location[1], router.location[2])}
            print("Forward to " + router.centralNodes[0][0], router.centralNodes[0][1])
            socket.sendto(json.dumps(packet).encode(), tuple((router.centralNodes[0][0], router.centralNodes[0][1])))
            return
        elif (name, sender_addr_port, req_name) not in router.getPit():
            print("I don't have the Data, updating PIT!")
            router.setPit(name, sender_addr_port, req_name)
            print("PIT ", router.getPit())
            #Forward Interest based on longest prefix
            next_node = router.longestPrefix(name)
            if next_node==[] or router.getMultiRequest()==2:
                next_nodes = []
                for node in router.getFib():
                    if len(node[0].split("/")) != 4:
                        next_nodes.append(node)
                next_node = [random.choice(next_nodes)] 
                router.setMultiRequest()
            else:
                next_node = router.longestPrefix(name)
                router.updateMultiRequest()
            print(next_node)
            print("Forwarding to ", next_node[len(next_node)-1]) 
            interest_packet = {"type": "interest", "dataname": name, "addr_port": (router.getLocation()[1], router.getLocation()[2]), "req_name": packet['req_name']} # interest packet
            socket.sendto(json.dumps(interest_packet).encode(), (next_node[len(next_node)-1][1], next_node[len(next_node)-1][2]))
            return

    #Data packet
    elif packet['type'] == 'data':
        name = packet["dataname"]
        print("Data packet Received!")
        data = packet["data"]
        inPit = False
        #Remove elements in PIT which contain interest
        for interest in router.getPit():
            if interest[0] == name:
                print("Satisfying interest table")
                router.popPit(interest[0],interest[1])
                #Send data packet to requesters
                # print(interest[1][1], router.location[1], interest[1][2], router.location[2])
                if interest[1][0] == router.location[1] and interest[1][1]==router.location[2]:
                    print(type(data))
                    print(data)
                    print('#'*30,f"\n\t\tDATA IS: {interface.decrypt_message(data)}\n\n", '#'*30)
                else:
                    address = interest[1]
                    print(json.dumps(packet).encode(), address)
                    socket.sendto(json.dumps(packet).encode(), tuple(address))
                inPit = True
        if inPit:
            print("Updating Content store")
            router.setCS(name,data, packet["freshness"])
            print(router.getCS())
            return
        else:
            print("Not in interest table, ignore packet.")
            return
    
    elif packet['type'] == 'publicKeyPayload':
        req_name = packet["dataname"]
        public_key = packet['data']
        for i in router.getPit():
            if(i[2]==req_name and i[3]==True):
                dataname = i[0]
                addr = i[1]
        if not dataname:
            print('Interest not in pit table: Returning')
            return
        publicKey = packet['data']
        router.popPit(dataname, addr)
        encrypted_data = interface.encrypt_message(message=router.getCS()[dataname][0], public_key_str=public_key)
        packet = {"type": "data", "dataname": dataname, "data":encrypted_data, "freshness": router.getCS()[dataname][1]}
        print("Forward to " + str(addr))
        print("encrypted data:", encrypted_data)
        print(json.dumps(packet).encode(), tuple(addr))
        socket.sendto(json.dumps(packet).encode(), tuple(addr))
        return
    return

# Listen for incoming datagrams
def inbound(socket,name,lock,router, interface):
    while(True):
        print("running inbound")
        bytesAddressPair = socket.recvfrom(bufferSize)
        print(f"\nRECEIVED DATA: {bytesAddressPair}")
        lock.acquire()
        message = bytesAddressPair[0]
        handle_packet(router,message,socket, interface)
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

    def send_public_key_to_central_node(self, socket):
        centralNode = self.router.centralNodes[0]
        publicKeyPayload_packet = {"type": "publicKeyPayload", "data": self.interface.save_public_key(save_to_disk=False, return_type_string=True), "dataname": self.router.name}
        print("Sending: ",json.dumps(publicKeyPayload_packet).encode(), (centralNode[0], centralNode[1]))
        socket.sendto(json.dumps(publicKeyPayload_packet).encode(), (centralNode[0], centralNode[1]))
    
    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        self.send_public_key_to_central_node(s_outbound)
        
        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock,self.router, self.interface))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.router,self.lock, (self.address, self.listen_port)))
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
