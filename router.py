import json

class Router:
    def __init__(self, name):
        self.multi_request = 0
        self.name = name  # device name
        self.cs = dict()  # name: data: freshness # content store
        self.pit = list(tuple())  # (name, interest_sender_address (addr, listen_port), req_name, is_data_ready=False) # Pending interest table
        self.fib = list(tuple())  # prefix, ip address, ongoing interface # Forwarding information base
        self.location = tuple() #name, address, listen port, send port # stores its own location in the network
        self.centralNodes = list(tuple()) # (address, listen port) # Stores the information of the central nodes

        with open("interfaces.json", 'r') as load_f:
            load_dict = json.load(load_f)

        #Set location and get the current device's neighbours
        neighbours_list = list()
        for i in range(len(load_dict)):
            nodeName = list(load_dict[i].keys())[0]
            if(name == nodeName):
                details = load_dict[i][name]
                self.setLocation(name, details[0]["address"], details[0]["listen port"],
                                  details[0]["send port"])
                neighbours_dict = load_dict[i][name][1]  # neighbours dictionary
                neighbours_list = neighbours_dict[list(neighbours_dict.keys())[0]]  # neighbours list
            elif(nodeName.split('/')[0] == 'centralNodes'):
                self.centralNodes.append((load_dict[i][nodeName][0]['address'], load_dict[i][nodeName][0]['listen port']))

        # add neighbours into the current fib
        for neighbour_name in neighbours_list:
            for i in range(len(load_dict)):
                device_name = list(load_dict[i].keys())[0]
                if device_name == neighbour_name:
                    device_detail = load_dict[i][device_name][0]
                    listen_port = device_detail[list(device_detail.keys())[0]]
                    addr = device_detail[list(device_detail.keys())[2]]
                    self.setFib(device_name, addr, listen_port)

        # add sensor
        for i in range(len(load_dict)):
            sensor_name = list(load_dict[i].keys())[0]
            if sensor_name != name:
                if sensor_name.startswith(name):
                    sensor_list = load_dict[i][sensor_name][0]
                    listen_port = list(sensor_list.values())[0]
                    addr = list(sensor_list.values())[2]
                    self.setFib(sensor_name, addr, listen_port)
        print(self)

    def __str__(self):
        return '\n'+'*'*5 + f'\nPrinting router for node {self.name}\ncontent store: '+ str(self.cs) \
        +f'\npit table: '+str(self.pit) \
        +f'\nfib table: '+str(self.fib) \
        +'\n'+'*'*5 + '\n'

    def getName(self):
        return self.name

    def getCS(self):
        return self.cs

    # cache new data
    def setCS(self, name, data, freshness):
        self.cs[name] = [data,freshness]

    def getPit(self):
        return self.pit

    # record the incoming interface of Interest Packet
    def setPit(self, name, interest_sender_address, requester_name, is_data_ready=False):  # incoming interface
        if (name, interest_sender_address, requester_name, False) not in self.pit:
            self.pit.append((name, interest_sender_address, requester_name, is_data_ready))

    def popPit(self,name, interest_sender_address):
        for i in self.pit:
            if(i[0] == name and i[1]==interest_sender_address):
                ret = i[2]
                self.pit.remove(i)
                return ret

    def getFib(self):
        return self.fib

    def setLocation(self, name, address, listen_port,send_port):
        self.location = (name,address,listen_port,send_port)

    def getLocation(self):
        return self.location
    
    def getAddress(self,name):
        # print("name:", name)
        for address in self.fib:
            # print("address:", address)
            if name == address[0]:
                return(address[1],address[2])

    # for scalable ????
    def setFib(self, prefix, addr, interface):  # ongoing interface
        t = (prefix, addr, interface)
        self.fib.append(tuple(t))

    def setMultiRequest(self):
        self.multi_request = 0

    def updateMultiRequest(self):
        self.multi_request +=1

    def getMultiRequest(self):
        return self.multi_request

    
    # The longest match between the name of the matched interest packet and the prefix in the fib,
    # returned with the fib storage format, and not contains urls that do not match at all
    def longestPrefix(self,str_packet):
        match_fib = dict()
        resorted = list()
        # split the url with '/'
        packet_len = len(str_packet.split('/'))
        # print(str_packet)
        print("in logestPrefix- router: ", str(self))

        # match how many strings between the packet name and fib
        for k in range(len(self.fib)):
            fib_len = len(self.fib[k][0].split('/'))
            # get the length of the shorter string
            loop_len = fib_len if packet_len > fib_len else packet_len
            prefix_len = 0
            # print(loop_len)
            for i in range(loop_len):
                if str_packet.split('/')[i] == self.fib[k][0].split('/')[i]:
                    prefix_len += 1
                else:
                    break
            # set the largest level if match completely
            if str_packet == self.fib[k][0]:
                loop_len = 9999
                # print(0)
                # print(self.fib[k])
                return [list(self.fib[k])]
            # If matches more than one string, it is added to the dictionary
            if prefix_len > 1:
                match_fib[self.fib[k][0]] = loop_len
        # print("match_fib: ", match_fib)
        # rank the dictionary
        resorted = sorted(match_fib.items(), key=lambda x: x[1], reverse=True)
        # print("resorted: ", resorted)
        # return the data has the same format with fib table
        resorted_fib = list(tuple())
        for i in range(len(resorted)):
            for k in self.fib:
                if (resorted[i][0] == k[0]) & (len(k[0].split('/')) != 4):
                    resorted_fib.append(k)
        # print("resorted_fib:", resorted_fib)
        return resorted_fib
