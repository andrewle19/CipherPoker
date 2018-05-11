import socket
import time
import random
import threading
from Crypto.Cipher import AES


publicKey = b"-ZA\xa1\x8f\x13*v\xae\x13p\xbd\xbd\xce\x9d\xd0"

host = '127.0.0.1'
port = 5000

# list of clients
clients = []

# stores session keys of each player
sessionKeys = []

# IMPORTANT: keeps track of state of the game
state = 0

# keeps track of player count
playerCount = 0

# The players win count and the hands of the players
player1wins = 0
player2wins = 0

# store players hands as list just used to send out list
player1Hand = []
player2Hand = []

# keeps track of number of rounds of game
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
            time.sleep(0.2)
            connection.send(b"Welcome to the Game")

            # receive the encrypted session key using server public key from the client
            data = connection.recv(1024)
            # print("Encrypted Session Key:",data)

            # decrypt the session key and store it in list
            decryption_suite = AES.new(publicKey, AES.MODE_CFB, 'This is an IV456')
            data = decryption_suite.decrypt(data)
            sessionKeys.append(data)



            # encrypt the data based on session key
            encryption_suite = AES.new(sessionKeys[playerCount], AES.MODE_CFB, 'This is an IV456')
            # send cipher text that server has received session keys
            cipher_text = encryption_suite.encrypt("Session Key was received")
            print("SessionKey:",sessionKeys[playerCount])
            # incrmenet the player count
            playerCount += 1
            # send the cipher text to player
            connection.send(cipher_text)

            # once we get both players connected with session keys go to State 1
            if(playerCount == 2):
                state = 1

        # State 1: in charge of generating the players hands
        if(state == 1):

            #Generate the keys for bt
            for i in range(3):
                player1Hand.append(random.randint(1,15))
                player2Hand.append(random.randint(1,15))

            # join the hand list into one string
            hand = ''.join(str(player1Hand).strip('[]'))
            # send the hand to player1
            encryption_suite = AES.new(sessionKeys[0], AES.MODE_CFB, 'This is an IV456')
            hand = encryption_suite.encrypt(hand)
            print("Sending hand1:",hand)
            clients[0].send(hand)


            # join the hand list into one string
            hand = ''.join(str(player2Hand).strip('[]'))
            encryption_suite = AES.new(sessionKeys[1], AES.MODE_CFB, 'This is an IV456')
            hand = encryption_suite.encrypt(hand)
            print("Sending hand2:",hand)
            # send hand to player 2
            clients[1].send(hand)

            # send to state 2 sleep to make sure there is no race condition
            time.sleep(0.2)
            state = 2
        # state 2- Player1s turn: this is where the choice of player1 is received
        if(state == 2):
            print("\nRound %s\n" % str(round+1))
            # tell users its players ones turn
            for client in clients:
                client.send(b"turn1")

            # get input choice form player1
            choice1 = ""
            while not choice1:
                decryption_suite = AES.new(sessionKeys[0], AES.MODE_CFB, 'This is an IV456')
                choice1 = clients[0].recv(1024)
                print("Encrypted Player 1's Choice:", choice1)
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
                print("Encrypted Player 2's Choice:", choice2)
                choice2 = decryption_suite.decrypt(choice2)

            state = 4

        # State 4 is where we compare the choices of the player and then determine outcome
        # This state can also end the game and announce a winner
        if(state == 4):

            #increment the round
            round += 1

            print("Player 1 Choice:",int(choice1))
            print("Player 2 Choice:",int(choice2))

            # Main game logic compares player's cards to determine winner
            if(int(choice1) > int(choice2)):
                print("\nPlayer1 wins Round %s" % str(round))
                player1wins += 1
            elif(int(choice1) < int(choice2)):
                print("\nPlayer2 wins Round %s" % str(round))
                player2wins += 1
            else:
                print("\nRound Tie")

            # go back to turn 1
            state = 2

            # if its the third round then we end the game
            # we send the results to the players
            if(round == 3):

                print("\nRESULTS:\n")

                for client in clients:
                    client.send(b"END")

                # sends the results to all playersdepending on outcome
                if(player1wins > player2wins):
                    print("Player 1 Wins!!!")
                    for client in clients:
                        client.send(b"Player 1 Wins!!!")
                elif(player1wins < player2wins):
                    print("Player 2 Wins!!!")
                    for client in clients:
                        client.send(b"Player 2 Wins!!!")
                else:
                    print("Tie Game")
                    for client in clients:
                        client.send(b"Tie Game")

                # Set up for the next game
                print("Destroying Session Keys")
                print("\nWaiting for New Players")
                del player1Hand[:]
                del player2Hand[:]
                del sessionKeys[:]
                del clients[:]
                playerCount = 0
                state = 0
                round = 0
                player1wins = 0
                player2wins = 0




# close the socket
s.close()
