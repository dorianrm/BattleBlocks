import socket
import pickle

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

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


