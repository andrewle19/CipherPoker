Cipher Poker 
=======
Author: Andrew Le  
Email: andrewle19@gmail.com

## Introduction
The Cipher Poker program is a secure internet poker program modeled with a server and client. The central server hosts the games between two clients. Each client  generates a session key and sends it to the server which the server uses to encrypt messages sent from the server to the client. The house then generates 3 numbers for each client and the clients choose between each number. The server compares the numbers in each round and the client with the highest number wins the round. The client that wins at least two rounds wins the game. The client Communication is all through TCP and using AES over the plaintext to achieve confidentiality. 

## Requirements:
  * Python 3
  * PyCrypto Library : pip install pycrypto

## Commands to Run Code
  1. Run the server: python3 server.py
  2. Run the client: python3 client.py  
  NOTE: NEED TO RUN TWO CLIENTS TO PLAY
