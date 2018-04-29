import socket
import time
import threading
from Crypto.Cipher import AES


host = '127.0.0.1'
port = 5000

# list of clients
clients = []

gameStates = ['start','key1','key2','turn1','turn2']
playerCount = 0
sessionKeys = []
state = gameStates[0]
index = 0

# create a socket using IPV4 and TCP connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to this port
s.bind((host,port))
# s.setblocking(0)

# allow the socket to only listen to 2 connections
s.listen(2)
# decryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')




# def handler(connection,addr):
#     global clients
#     global playerCount
#     global state
#     while True:
        # if(state == gameStates[0]):
        #     connection.send(b"1")
        #     data = connection.recv(1024)
        #     sessionKeys[index] = data
        #     print(data)
        #     if not data:
        #         clients.remove(connection)
        #         connection.close()
        #         print("Disconnected",addr)
        #         playerCount -= 1
        #         break
        # if(len(sessionKeys) == 2):
        #     state = "turn1"



print("Server Started.")
while True:
        # on a connection retreve the connection and the address
        if(state == gameStates[0]):
            connection, addr = s.accept()
            print("Incoming: ", addr)
            # cThread = threading.Thread(target=handler, args=(connection,addr))
            # # allows program to close even if threads are running
            # cThread.daemon = True
            # cThread.start()
            clients.append(connection)
            playerid = "Player"
            playerid += str(playerCount+1)

            connection.send(playerid.encode("utf-8"))
            connection.send(b"Welcome to the Game")

            data = connection.recv(1024)

            sessionKeys.append(data)
            encryption_suite = AES.new(sessionKeys[playerCount], AES.MODE_CFB, 'This is an IV456')
            cipher_text = encryption_suite.encrypt("Session Key was received")
            print(cipher_text)

            playerCount += 1
            connection.send(cipher_text)
            if(playerCount == 2):
                state = gameStates[1]

        # if(state == gameStates[1]):
        #     data = clients[0].recv(1024)
        #     if data:
        #         sessionKeys.append(data)
        #         print(sessionKeys)
        #         state = gameStates[2]
        # if(state == gameStates[2]):
        #     data = clients[1].recv(1024)
        #     if data:
        #         sessionKeys.append(data)
        #         print(sessionKeys)
        #         state = gameStates[2]
        # else:
        #     connection, addr = s.accept()
        #     print("Denying: ", addr)
        #     connection.send(b"Max number of players in game")
        #     connection.close()

        # print(clients)
        # plain_text = decryption_suite.decrypt(data)
        # print(plain_text.decode("utf-8"))

        # if addr not in clients:
        #     clients.append(connection)
        #     print("Client",addr," joined the game")



        # for client in clients:
        #     print("Sending",plain_text)
        #     s.sendto(plain_text, client)
    # except:
    #     pass
s.close()
