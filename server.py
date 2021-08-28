import socket
from _thread import *
import pickle
from game import Game
import json


# server = "192.168.1.72" #local
server = "192.168.7.137" #local ohio
# server = "98.155.155.206" #public
# server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("[STARTED] Server Started -----")
print("[WAITING] Waiting for a connection...")

#hold player objects
# players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]
games = {}
idCount = 0
HEADERSIZE = 10
COL_NAME = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

def receive_data(sock):
    full_msg = b''
    new_msg = True
    while True:
        msg = sock.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            data = pickle.loads(full_msg[HEADERSIZE:])
            break

    return data

def send_data(clientsocket, data):
    data_to_send = pickle.dumps(data)
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
    try:
        clientsocket.send(data_size + data_to_send)
        
    except socket.error as e:
        print(e)

'''
List of string msg's sent:
'ready' - player locked in block placements
'get' - get game catalyst
'(x,y)' - a player sends coords for guess

'''

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p))) #send curr player number
    reply = ""
    while True:
        try:
            # data = conn.recv(8192).decode() #server recieves str data from client
            data = receive_data(conn)
            
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data[0] == "r":
                        print("[INFO] player " + str(p) + " is ready!")
                        game.pLock[p] = True
                        data = data[1:]
                        data = json.loads(data)
                        game.coords[p] = data
                        if game.pLock[0] and game.pLock[1]:
                            game.inProgress = True
                        print(game.coords)
                    elif data != "get":
                        # game is being played
                        # coords = list( map(int, data.split(",")) )
                        # print("[INFO] player " + str(p) + " coords: (" + str(coords[0]) + " , " + COL_NAME[coords[1]] + ")")
                        print("[INFO] coords: ", data)
                        # Change player turn
                        game.Turn[p] = False
                        if p == 0: game.Turn[p+1] = True
                        else: game.Turn[p-1] = True
                    reply = game
                    # conn.sendall(pickle.dumps(reply))
                    send_data(conn, reply)
            else:
                break
        except Exception as e:
            print("Failed try")
            print(e)
            break

    print("Lost connection")
    print("Closing Game", gameId)
    try:
        del games[gameId]
    except:
        pass
    idCount -= 1
    conn.close()




while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2 #increment games for every 2 players 
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
    
    start_new_thread(threaded_client, (conn, p, gameId))
