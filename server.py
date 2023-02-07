import socket
import select
import sys
from _thread import *

# create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set socket to reuse address
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks for correct number of args
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# get IP address, port number from system
IP_addr = str(sys.argv[1])
port = int(sys.argv[2])

# bind server to IP_addr at port port
server.bind((IP_addr, port))

# max 16 users connected to server at once
server.listen(16)
clients = []

# listens and broadcasts messages to chat room
def clientthread(conn, addr):
    # send welcome message to client when they connect
    conn.send("Welcome to the chat!")

    #server runs constantly
    while True:
        try:
            # get essage from client, max length 280 chars
            message = conn.recv(280).decode()

            # print user who sent message and message on server terminal
            if message:
                print("<" + addr[0] + ">: " + message)
                
                # broadcast message to all users in chat
                broadcast_message = "<" + addr[0] + ">: " + message
                broadcast(broadcast_message)
            
            # message has no content, remove connection
            else:
                remove(conn)

        except:
            continue

# broadcast message to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            remove(client)

# removes specified client from chat
def remove(client):
    if client in clients:
        clients.remove(client)

# run server indefinitely
while True:

    # accepts connection requests, conn is socket object for 
    # user that is connecting, addr is IP address of user
    conn, addr = server.accept()
    clients.append(conn)

    # notify server a client has connected
    print(addr[0] + " connected")

    # spin off thread for new connection
    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()






