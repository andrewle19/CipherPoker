import socket
import threading
import time
from Crypto.Cipher import AES
import os


# servers public key
publicKey = b"-ZA\xa1\x8f\x13*v\xae\x13p\xbd\xbd\xce\x9d\xd0"

# The current player ID
id = -1
host = '127.0.0.1'
port = 0

# address of server
server = ('127.0.0.1',5000)

# Encryption
session_key = os.urandom(16)


print("Session Key:",session_key)

# Encrypt the session key using servers public key before sending out
encryption_suite = AES.new(publicKey, AES.MODE_CFB, 'This is an IV456')
encryptedKey = encryption_suite.encrypt(session_key)
print("Encrypted Session Key:",encryptedKey,"\n")

# socket.AF_INET = IPv4, SOCK_DGRAM = UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#bind the socket to the address and random open port since port is set to 0
s.bind((host, port))

# start by connecting to the server
s.connect(server)

state = 0
# Make a Decryptiona and encryption Suite
decryption_suite = AES.new(session_key, AES.MODE_CFB, 'This is an IV456')
encryption_suite = AES.new(session_key, AES.MODE_CFB, 'This is an IV456')


while True:

    # Sends the Session Keys
    if(state == 0):
        # receive data from server
        data = s.recv(1024)

        # If data is Player1 or Player 2Identifies the player on connection
        if(data.decode("utf-8") == "Player1"):
            id = 0
            print(data.decode("utf-8"))
        if(data.decode("utf-8") == "Player2"):
            id = 1
            print(data.decode("utf-8"))


        # When you receive the Welcome Send The Session Keys
        if(data.decode("utf-8") == "Welcome to the Game"):

            print(data.decode("utf-8"))
            s.sendto(encryptedKey,server)
            state = 1

    # state 1 is about confirming the server has received session keys
    if(state == 1):
        data = s.recv(1024)
        # Decrypts the msg
        plain_text = decryption_suite.decrypt(data)
        print(plain_text.decode("utf-8"))
        print("\n")
        state = 2

    # in state 2 we receive our hands
    if(state == 2):

        try:
            # Grab the hands of the players
            data = s.recv(1024)

            # decrypt the encrypted hands, the format is card , card , card
            print("Encrypted Hand:",data)
            decryption_suite = AES.new(session_key, AES.MODE_CFB, 'This is an IV456')
            cards = decryption_suite.decrypt(data)
            print("Decrypted Hand:",cards)

            # Split the cards into a list
            hand = (cards.decode('utf-8').split(","))
            print("hand:",hand)

        except UnicodeError:
            pass
        # once the players receive their hands move to state 3
        state = 3
    # State 3 is the Game
    if(state == 3):

        # receive turn signal from server(3 signals: END, turn1, turn2)
        turn = s.recv(1024)

        try:
            encryption_suite = AES.new(session_key, AES.MODE_CFB, 'This is an IV456')

            # when the end signal is received move to State 4 the results stage
            if(turn.decode("utf-8") == "END"):
                state = 4

            # if signal is turn1 means its player 1 turn
            if(turn.decode('utf-8') == "turn1"):
                print("\nPlayer 1's Turn")
                if(id == 0):
                    print("Index : Card")
                    for i in range(len(hand)):
                        print(str(i)+")"+str(hand[i]))
                    choice = int(input("Choose Card for Round(use the index): "))
                    # input validation
                    while(choice < 0 or choice > len(hand)):
                        print("Invalid Choice Choose Again")
                        choice = int(input("Choose Card for Round(use the index): "))
                    #encrypt the card choice and send to server remove it from hand
                    encryptedChoice = encryption_suite.encrypt(hand[choice].encode("utf-8"))
                    s.sendto(encryptedChoice,server)
                    hand.pop(choice)

            # if signal is turn2 means its player 1 turn
            if(turn.decode('utf-8') == "turn2"):
                print("\nPlayer 2's Turn")

                if(id == 1):
                    # user chooses the card
                    print("Index : Card")
                    for i in range(len(hand)):
                        print(str(i)+")"+str(hand[i]))
                    choice = int(input("Choose Card for Round(use the index): "))
                    #input validation
                    while(choice < 0 or choice > len(hand)):
                        print("Invalid Choice Choose Again")
                        choice = int(input("Choose Card for Round(use the index): "))
                    #encrypt the card choice and send to server remove it from hand
                    encryptedChoice = encryption_suite.encrypt(hand[choice].encode("utf-8"))
                    s.sendto(encryptedChoice,server)
                    hand.pop(choice)

        except UnicodeError:
            pass

    # Get the results
    if(state == 4):
         # receive the results from the server and print them
         results = s.recv(1024)
         print('\nRESULTS:\n')
         print(results.decode("utf-8"))
         print("Destroying Session Keys and ")
         print("Exiting Program")
         break

# close the socket
s.close()
