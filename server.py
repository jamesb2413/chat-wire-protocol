import socket
import select
import sys
import helpers
from _thread import *

## Chat functionality
# Create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket to reuse address
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Checks for correct number of args
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
ip_addr = str(sys.argv[1])
port = int(sys.argv[2])

server.bind((ip_addr, port))

# Max 16 users connected to server at once
server.listen(16)
# List of connected sockets
clientSockLst = []
# Map of existing users and their messages { username : [socketObj, loggedOnBool, messageQueue] }
clientDict = {}

# Parse message according to wire protocol to determine which function to call
def parse(message, clientSock):
    message = message.split()
    operation = message[0]
    if operation == "I":
        helpers.signIn(message, clientSock, clientDict)
    elif operation == "S":
        helpers.sendMsg(message, clientSock, clientDict)
    elif operation == "L":
        helpers.sendUserlist(message, clientSock, clientDict)
    elif operation == "D":
        helpers.deleteAcct(message, clientDict)
    elif operation == "O":
        helpers.logOut(message, clientDict)
    else:
        pass

## Chat loops
# Listens for messages from this client and parses to perform necessary functions
def client_thread(clientSock, ip):
    # Server listens indefinitely
    while True:
        try:
            # Get message from client, max length 280 chars
            message = clientSock.recv(280).decode()
            
            # print IP address of user who sent message and message on server terminal
            if message:
                print("<" + ip[0] + ">: " + message)
                
                # Determine necessary function based on wire protocol
                parse(message, clientSock)
            
            # Message has no content, remove connection
            else:
                if helpers.getClientUsername(clientSock, clientDict) != "None":
                    helpers.logOut(clientSock, clientDict)
                remove(clientSock)
                return
        except:
            continue

# removes specified client from chat
def remove(clientSock):
    if clientSock in clientSockLst:
        clientSockLst.remove(clientSock)

# Run server indefinitely
while True:
    # Accept connection requests. ClientSock connecting user's socket object.
    clientSock, ip = server.accept()
    clientSockLst.append(clientSock)

    # Print new client's IP address to server when a client has connected
    print(ip[0] + " connected")

    start_new_thread(client_thread, (clientSock, ip))