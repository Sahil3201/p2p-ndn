import interfaces
import threading
import UDPNode1

def c_inbound():
    while(True):
        bytesAddressPair = socket.recvfrom(bufferSize)
        print(f"\nRECEIVED DATA: {bytesAddressPair}")
        lock.acquire()
        message = bytesAddressPair[0]
        handle_packet(router, message, socket)
        lock.release()

class CentralNode(Base):
    def __init__(self, id):
        super().__init__(id)
        self.save_public_key()

        self.keystore = {} # {<nodeName>: <public key>}

    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)
        # creating thread
        t1 = threading.Thread(target=c_inbound, args=(s_inbound,self.name,self.lock,self.router))
        t2 = threading.Thread(target=c_outbound, args=(s_outbound,self.router,self.lock, (self.address, self.listen_port)))
        t3 = threading.Thread(target=c_update, args=(self.interface,self.router,self.name))

        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
