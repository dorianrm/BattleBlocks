import socket
from _thread import *
import pickle
from game import Game


server = "192.168.1.72" #local
# server = "98.155.155.206" #public
# server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("[STARTED] Server Started -----")
print("[WAITING] Waiting for a connection...")

#hold player objects
# players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]
games = {}
idCount = 0

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
            data = conn.recv(4096).decode() #server recieves str data from client
            
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "ready":
                        game.pLock[p] = True
                    elif data != "get":
                        #guess
                        game.play(p, data)
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
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
