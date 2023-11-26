import interfaces
import threading, json
import UDPNode1
from interfaces import Base
from UDPNode1 import setup_sockets, find_node

bufferSize  = 1024
with open('interfaces.json') as file:
    references = json.load(file)

def c_inbound(interface, socket_inbound, socket_outbound, name, lock):
    while(True):
        bytesAddressPair = socket_inbound.recvfrom(bufferSize)
        print(f"\nRECEIVED DATA: {bytesAddressPair}")
        lock.acquire()
        message = bytesAddressPair[0]
        c_handle_packet(message, socket_outbound, interface, lock)
        lock.release()

def c_handle_packet(message, socket, interface, lock):
    print("HANDLING PACKET")
    packet = json.loads(message.decode())
    if (packet["type"] == "publicKeyRequest"):
        # packet = {"type": "publicKeyRequest", "data":packet['req_name'], "return_address":(<ip address>, <listen port>)}
        publicKey = interface.keystore[packet['data']]
        dataname = packet['data']
        addr_port = packet['return_address']
        t2 = threading.Thread(target=c_outbound, args=(interface, socket, lock, addr_port, dataname, publicKey))
        t2.start()
    elif (packet["type"] == "publicKeyPayload"):
        # packet = {"type": "publicKeyPayload", "data": self.interface.public_key, "dataname": self.router.name, "signature":self.interface.sign_message(self.router.name)}
        interface.keystore[packet['dataname']] = packet['data']

def c_outbound(interface, socket, lock, addr_port, dataname, publicKey):
    lock.acquire()
    packet = {"type": "publicKeyPayload", "data": publicKey, "dataname": dataname}
    print("Sending: ",json.dumps(packet).encode(), addr_port)
    socket.sendto(json.dumps(packet).encode(), tuple(addr_port))
    lock.release()

class CentralNode(Base):
    def __init__(self, id):
        super().__init__(id)
        self.save_public_key(return_type_string=False)

        self.keystore = {} # {<nodeName>: <public key>}

        self.lock = threading.Lock()
        print(self.name)
        #Find network details from json
        index=find_node(self.name)   
        network_details = references[index][self.name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]

        print(self)

    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)
        # creating thread
        t1 = threading.Thread(target=c_inbound, args=(self, s_inbound, s_outbound, self.name, self.lock))
        # t3 = threading.Thread(target=c_update, args=(self.interface,self.router,self.name))

        t1.start()
        # t2.start()
        # t3.start()
        t1.join()
        # t2.join()
        # t3.join()

    def __str__(self):
        return str(self.keystore)
