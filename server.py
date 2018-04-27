import socket
import time
from Crypto.Cipher import AES


host = '127.0.0.1'
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

decryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')

quitting = False
print "Server Started."

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        print("Incoming: ", data, addr)
        plain_text = decryption_suite.decrypt(data)
        print(plain_text.decode("utf-8"))

        if "Quit" in str(plain_text):
            quitting = True
        if addr not in clients:
            clients.append(addr)
            print("here")
            print("Client",addr," joined the game")


        for client in clients:
            print("Sending",plain_text)
            s.sendto(plain_text, client)
    except:
        pass
s.close()
