import socket
import threading
import time
from Crypto.Cipher import AES
import os

# The current player ID
id = -1
host = '127.0.0.1'
port = 0

# address of server
server = ('127.0.0.1',5000)



# Encryption
random_key = os.urandom(16)
print("random key",random_key,"\n")
encryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')


# socket.AF_INET = IPv4, SOCK_DGRAM = UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#bind the socket to the address and random open port since port is set to 0
s.bind((host, port))



# start by connecting to the server
s.connect(server)

state = 0
decryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
encryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
while True:
    # receive data from server


    # if u disconnect break the loop
    # if not data:
    #     break

    # state 0 is just staring the game off
    # Sends the Session Keys
    if(state == 0):
        data = s.recv(1024)
        # Identifies the player on connection
        if(data.decode("utf-8") == "Player1"):
            id = 0
            print(data.decode("utf-8"))
        if(data.decode("utf-8") == "Player2"):
            id = 1
            print(data.decode("utf-8"))
        data = s.recv(1024)
        # When you receive the Welcome Send The Session Keys
        if(data.decode("utf-8") == "Welcome to the Game"):
            print(data.decode("utf-8"))
            s.sendto(random_key,server)
            state = 1
    if(state == 1):
        # confirms with server it has received its keys
        data = s.recv(1024)
        plain_text = decryption_suite.decrypt(data)
        print(plain_text)
        state = 2

    # in state 2 we receive our hands
    if(state == 2):
        data = s.recv(1024)
        try:
            if(data.decode('utf-8')=="hands"):
                data = s.recv(1024)
                print("cards:",data)
                decryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
                cards = decryption_suite.decrypt(data)
                print("decrypt",cards)
                hand = (cards.decode('utf-8').split(","))
                print("hand",hand)
        except UnicodeError:
            pass
        state = 3
    if(state == 3):

        turn = s.recv(1024)

        try:
            if(turn.decode("utf-8") == "END"):
                state = 4

            if(turn.decode('utf-8') == "turn1"):
                print("Player 1's Turn")
                if(id == 0):
                    print("Index : Card")
                    for i in range(len(hand)):
                        print(i,":",hand[i])
                    choice = int(input("Choose Card for Round: "))
                    encryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
                    encryptedChoice = encryption_suite.encrypt(hand[choice].encode("utf-8"))
                    s.sendto(encryptedChoice,server)
                    hand.pop(choice)

            if(turn.decode('utf-8') == "turn2"):
                print("Player 2's Turn")
                if(id == 1):

                    for i in range(len(hand)):
                        print(i,":",hand[i])
                    choice = int(input("Choose Card for Round:"))
                    encryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
                    encryptedChoice = encryption_suite.encrypt(hand[choice].encode("utf-8"))
                    s.sendto(encryptedChoice,server)
                    hand.pop(choice)
        except UnicodeError:
            pass


    if(state == 4):
         results = s.recv(1024)
         print('\nRESULTS:\n')
         print(results.decode("utf-8"))
         break


s.close()
