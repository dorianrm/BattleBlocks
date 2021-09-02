import socket
import pickle
HEADERSIZE = 10

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.72" #local
        # self.server = "98.155.155.206" #public 
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        # print("pos set: ", self.pos) use to debug server connection
        
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            #get player number when connect to server
            #decoding player number
            return self.client.recv(2048).decode() 
        except:
            pass

    # def send(self, data):
    #     try:
    #         self.client.send(str.encode(data))
    #         return pickle.loads(self.client.recv(8192))
    #     except socket.error as e:
    #         print(e)
    
    # this is the function you should use, it uses a receive function that has a buffer
    # and ensures that you receive ALL the information that you sent without throwing errors
    def send(self, data):
        data_to_send = pickle.dumps(data)
        data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
        try:
            self.client.send(data_size + data_to_send)
            
            package = self.receive_data()
            return package
        except socket.error as e:
            print(e)
    
    def receive_data(self):
        full_msg = b''
        new_msg = True
        while True:
            msg = self.client.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
                
            full_msg += msg
    
            if len(full_msg)-HEADERSIZE == msglen:
                data = pickle.loads(full_msg[HEADERSIZE:])
                break
    
        return data


