<h1> Cipher Poker </h1>

<h2>Authors</h2>
<ul>
  <li>Andrew Le</li>
 
<p>The Cipher Poker program is a secure internet poker program modeled with a server and client. The central server hosts the games between two clients. Each client  generates a session key and sends it to the server which the server uses to encrypt messages sent from the server to the client. The house then generates 3 numbers for each client and the clients choose between each number. The server compares the numbers in each round and the client with the highest number wins the round. The client that wins at least two rounds wins the game. The client Communication is all through TCP and using AES over the plaintext to achieve confidentiality. 
</p>
<h2> Requirements:</h2>
<ul>
  <li>Python 3</li>
  <li>PyCrypto Library : pip install pycrypto </li>
</ul>

<h2>Commands to Run Code</h2>
- Run the server: python3 server.py
- Run the client: python3 client.py
- NOTE: NEED TO RUN TWO CLIENTS TO PLAY
