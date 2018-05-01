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
            # incrmenet the player count
            playerCount += 1
            # send the cipher text to player
            connection.send(cipher_text)

            # once we get both players connected with session keys go to State 1
            if(playerCount == 2):
                state = 1
        # State 1: in charge of generating the players hands
        if(state == 1):
            # for client in clients:
            #     client.send(b"hands")
            #Generate the keys for bt
            for i in range(3):
                player1Hand.append(random.randint(1,15))
                player2Hand.append(random.randint(1,15))

            # join the hand list into one string
            hand = ''.join(str(player1Hand).strip('[]'))
            # send the hand to player1
            encryption_suite = AES.new(sessionKeys[0], AES.MODE_CFB, 'This is an IV456')
            decryption_suite = AES.new(sessionKeys[0], AES.MODE_CFB, 'This is an IV456')
            hand = encryption_suite.encrypt(hand)


            print("hand:",hand)
            clients[0].send(hand)


            # join the hand list into one string
            hand = ''.join(str(player2Hand).strip('[]'))
            encryption_suite = AES.new(sessionKeys[1], AES.MODE_CFB, 'This is an IV456')
            hand = encryption_suite.encrypt(hand)
            print("hand:",hand)
            # send hand to player 2
            clients[1].send(hand)

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
                decryption_suite = AES.new(sessionKeys[0], AES.MODE_CFB, 'This is an IV456')
                choice1 = clients[0].recv(1024)
                choice1 = decryption_suite.decrypt(choice1)

            state = 3

        # State:3 Player2s turn: this is where the choice of player1 is received
        if(state == 3):
            for client in clients:
                client.send(b"turn2")
            choice2 = ""
            while not choice2:
                decryption_suite = AES.new(sessionKeys[1], AES.MODE_CFB, 'This is an IV456')
                choice2 = clients[1].recv(1024)
                choice2 = decryption_suite.decrypt(choice2)

            state = 4
        if(state == 4):
            print(int(choice1))
            print(choice2)
            if(int(choice1) > int(choice2)):
                print("player1 win")
                player1wins += 1
            if(int(choice1) < int(choice2)):
                print("player2 win")
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
                del sessionKeys[:]
                del clients[:]

                break
            state = 1

s.close()
