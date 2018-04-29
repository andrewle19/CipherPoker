import socket
import threading
import time
from Crypto.Cipher import AES
import os

# tLock = threading.Lock()
# shutdown = False
#
# def receving(name, sock):
#     while not shutdown:
#         try:
#             tLock.acquire()
#             while True:
#                 data, addr = sock.recvfrom(1024)
#                 print str(data)
#         except:
#             pass
#         finally:
#             tLock.release()

gameStates = ['start','key1','key2','turn1','turn2']

id = -1
host = '127.0.0.1'
port = 0

# address of server
server = ('127.0.0.1',5000)



# Encryption
random_key = os.urandom(16)
print("random key",random_key,"\n")
encryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')



# print(cipher_text)
# # Decryption
# plain_text = decryption_suite.decrypt(cipher_text)
# print(plain_text.decode("utf-8"))

# socket.AF_INET = IPv4, SOCK_DGRAM = UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendMsg():
    global s
    while True:
        message = input("")
        encryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')
        cipher_text = encryption_suite.encrypt(message)

        s.sendto(cipher_text, server)



#bind the socket to the address and random open port since port is set to 0
s.bind((host, port))

# sets to socket non blocking mode meaning if send / recv call receives/sends no data it wont raise error
# s.setblocking(0)

s.connect(server)

# ithread = threading.Thread(target=sendMsg)
# ithread.daemon = True
# ithread.start()
state = 0
while True:
    data = s.recv(1024)


    if not data:
        break



    if(state == 0):
        if(data.decode("utf-8") == "Player1"):
            id = 0
            print(data.decode("utf-8"))
        if(data.decode("utf-8") == "Player2"):
            id = 1
            print(data.decode("utf-8"))

        if(data.decode("utf-8") == "Welcome to the Game"):
            print(data.decode("utf-8"))
            s.sendto(random_key,server)
            state = 1
    if(state == 1):
        decryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
        plain_text = decryption_suite.decrypt(data)
        print("decrypt",plain_text)


#
# rT = threading.Thread(target=receving, args=("RecvThread",s))
# rT.start()

# encryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')
# message = raw_input("cmd-> ")
# cipher_text = encryption_suite.encrypt(message)

# s.sendto(cipher_text, server)

# quitting = False
# while not quitting:
#     try:
#
#         data, addr = s.recvfrom(1024)
#         print("Incoming: ", data, addr)
#
#         if(data):
#             message = raw_input("cmd-> ")
#             cipher_text = encryption_suite.encrypt(message)
#             s.sendto(cipher_text, server)
#         if message == 'q':
#             quitting = True
#
#     except:
#         pass

#
# while message != 'q':
#     if message != '':
#         cipher_text = encryption_suite.encrypt(message)
#         s.sendto(cipher_text, server)
#     tLock.acquire()
#     message = raw_input("cmd-> ")
#     tLock.release()
#
#     time.sleep(0.2)

# shudown = True
# rT.join()

# s.sendto(random_key,server)

s.close()
