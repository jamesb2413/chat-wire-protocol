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
clientSockLst = []
userDict = {}

def addUser(username, clientSock):
    userDict[username] = [clientSock, True, []]
    return userDict[username]

def signIn(message, clientSock):
    # Sign in / create account
    thisUser = []
    username = message[2]
    if message[1] == "Existing":
        try:
            thisUser = userDict[username]
        except:
            # TODO: Send message to user with username error
            pass
    else:
        thisUser = addUser(username, clientSock)
    # Unread messages 
    unreads = userDict[username][2]
    print(unreads)
    unreadNum = len(unreads)
    unreadAlert = "You have " + unreadNum + " unread messages:\n\n"
    for msg in unreads:
        unreadAlert += msg + "\n\n"
    clientSock.sendall(unreadAlert.encode())

def parse(message, clientSock):
    message = message.split()
    if message[0] == "Signin":
        signIn(message, clientSock)
    else:
        pass
        
        


# listens and broadcasts messages to chat room
def client_thread(clientSock, ip):
    #server runs constantly
    while True:
        try:
            # get message from client, max length 280 chars
            message = clientSock.recv(280).decode()

            parse(message, clientSock)

            # print user who sent message and message on server terminal
            if message:
                print("<" + ip[0] + ">: " + message)
                
                # broadcast message to all users in chat
                broadcast_message = "<" + ip[0] + ">: " + message
                broadcast(broadcast_message, clientSock)
            
            # message has no content, remove connection
            else:
                remove(clientSock)

        except:
            continue

# broadcast message to all clients
def broadcast(message, sender):
    for clientSock in clientSockLst:
        print(clientSock)
        if clientSock != sender:
            try:
                clientSock.send(message.encode())
            except:
                clientSock.close()
                remove(clientSock)

# removes specified client from chat
def remove(client):
    if clientSock in clientSockLst:
        clientSockLst.remove(clientSock)

# run server indefinitely
while True:

    # accepts connection requests. clientSock is socket object for 
    # connecting user, ip is IP address of connecting user
    clientSock, ip = server.accept()
    clientSockLst.append(clientSock)

    # notify server a client has connected
    print(ip[0] + " connected")

    # spin off thread for new connection
    start_new_thread(client_thread, (clientSock, ip))






