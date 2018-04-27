import socket
import threading
import time
from Crypto.Cipher import AES
import os




tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print str(data)
        except:
            pass
        finally:
            tLock.release()



host = '127.0.0.1'
port = 0

# address of server
server = ('127.0.0.1',5000)



# Encryption
random_key = os.urandom(16)
# print("random key",random_key,"\n")
encryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')


# print(cipher_text)
# # Decryption
# decryption_suite = AES.new(random_key, AES.MODE_CFB, 'This is an IV456')
# plain_text = decryption_suite.decrypt(cipher_text)
# print(plain_text.decode("utf-8"))

# socket.AF_INET = IPv4, SOCK_DGRAM = UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#bind the socket to the address and random open port since port is set to 0
s.bind((host, port))

# sets to socket non blocking mode meaning if send / recv call receives/sends no data it wont raise error
s.setblocking(0)

# 
# rT = threading.Thread(target=receving, args=("RecvThread",s))
# rT.start()

encryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')
message = raw_input("cmd-> ")

while message != 'q':
    if message != '':
        cipher_text = encryption_suite.encrypt(message)
        s.sendto(cipher_text, server)
    tLock.acquire()
    message = raw_input("cmd-> ")
    tLock.release()

    time.sleep(0.2)

shudown = True
# rT.join()
s.close()
