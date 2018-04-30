import socket
import time
import random
import threading
from Crypto.Cipher import AES


host = '127.0.0.1'
port = 5000

# list of clients
clients = []

playerCount = 0
sessionKeys = []
state = 0
index = 0

# The players win count and the hands of the players
player1wins = 0
player2wins = 0

player1Hand = []
player2Hand = []
round = 0;
# create a socket using IPV4 and TCP connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to this port
s.bind((host,port))
# s.setblocking(0)

# allow the socket to only listen to 2 connections
s.listen(2)
# decryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')


print("Server Started.")
while True:

        # State 0: Setting up the game, get 2 connections, setup session keys
        if(state == 0):
            # when someone connects to server
            connection, addr = s.accept()
            print("Incoming: ", addr)
            # append the connection for later use
            clients.append(connection)

            # assign clients player ids
            playerid = "Player"
            playerid += str(playerCount+1)

            # welcome the players to game(this triggers event in client)
            connection.send(playerid.encode("utf-8"))
            connection.send(b"Welcome to the Game")

            # receive the session key from the client
            data = connection.recv(1024)
            sessionKeys.append(data)

            # encrypt the data based on session key
            encryption_suite = AES.new(sessionKeys[playerCount], AES.MODE_CFB, 'This is an IV456')
            # send cipher text that server has received session keys
            cipher_text = encryption_suite.encrypt("Session Key was received")
            print("sessionKeys:",sessionKeys[playerCount])
            print(cipher_text)
            # incrmenet the player count
            playerCount += 1
            # send the cipher text to player
            connection.send(cipher_text)

            # once we get both players connected with session keys go to State 1
            if(playerCount == 2):
                state = 1
        # State 1: in charge of generating the players hands
        if(state == 1):
            for client in clients:
                client.send(b"hands")
            #Generate the keys for bt
            for i in range(3):
                player1Hand.append(random.randint(1,15))
                player2Hand.append(random.randint(1,15))

            # join the hand list into one string
            hand = ''.join(str(player1Hand).strip('[]'))
            print(hand)
            # send the hand to player1
            clients[0].send(hand.encode('utf-8'))

            # join the hand list into one string
            hand = ''.join(str(player2Hand).strip('[]'))
            print(hand)
            # send hand to player 2
            clients[1].send(hand.encode('utf-8'))

            # send to state 2
            state = 2
        # state 2- Player1s turn: this is where the choice of player1 is received
        if(state == 2):
            # tell users its players ones turn
            for client in clients:
                client.send(b"turn1")

            # get input choice form player1
            choice1 = ""
            while not choice1:
                choice1 = clients[0].recv(1024)
            state = 3

        # State:3 Player2s turn: this is where the choice of player1 is received
        if(state == 3):
            for client in clients:
                client.send(b"turn2")
            choice2 = ""
            while not choice2:
                choice2 = clients[1].recv(1024)
            state = 4
        if(state == 4):
            print(int(choice1.decode("utf-8")),int(choice2.decode("utf-8")))
            if(int(choice1.decode("utf-8")) > int(choice2.decode("utf-8"))):
                player1wins += 1
            if(int(choice1.decode("utf-8")) < int(choice2.decode("utf-8"))):
                player2wins += 1

            #increment the round
            round += 1

            if(round == 3):
                for client in clients:
                    client.send(b"END")
                if(player1wins > player2wins):
                    for client in clients:
                        client.send(b"Player 1 Wins")
                if(player1wins < player2wins):
                    for client in clients:
                        client.send(b"Player 2 Wins")
                break
            state = 1








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
