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
    #TODO: make sure username doesn't already exist
    userDict[username] = [clientSock, True, []]
    return userDict[username]

def signIn(message, clientSock):
    # Sign in / create account
    thisUser = []
    username = message[2]
    if message[1] == "Existing":
        try:
            thisUser = userDict[username]
            # TODO: If user is already logged in, deny access
            print(thisUser)
        except:
            # TODO: Send message to user with username error
            pass
    else:
        thisUser = addUser(username, clientSock)
    unreads = userDict[username][2]
    unreadNum = str(len(unreads))
    unreadAlert = "<<ALERT>> You have " + unreadNum + " unread messages:\n\n"
    for msg in unreads:
        unreadAlert += msg + "\n\n"
    clientSock.sendall(unreadAlert.encode())

def enqueueMsg(message, recipient):
    userDict[recipient][2].append(message)


def getClientUsername(clientSock):
    # get sender username
    # its not pretty but it works, refactor if possible
    for key in userDict.keys():
        if userDict[key][0] == clientSock:
            return key
    print("CRITICAL ERROR: USER SENDING DOES NOT EXIST")

def sendMsg(message, clientSock):
    sender = getClientUsername(clientSock)
    recipient = message[1]
    raw_msg = " ".join(message[2:])

    # Error handling message 
    error_handle = "Error sending message to " + recipient + ": "
    
    # Getting socket of user message was sent to
    try:
        recipientSock = userDict[recipient][0]
        loggedIn = userDict[recipient][1]
    except:
        error_handle += "User does not exist"
        clientSock.sendall(error_handle.encode())
        return

    # Send message to recipient
    try:
        payload = "From " + sender + ": " + raw_msg
        print("payload is: " + payload)
        # If user is logged in, send the message
        if loggedIn:
            recipientSock.sendall(payload.encode())
        # If user is logged out, add to their queue
        # NOTE Not sure if this works since no log out function yet to set 
        # bool to false
        else:
            enqueueMsg(payload, recipient)
            loggedOutMsg = "User " + recipient + " is currently offline. They will recieve your message when they next log in."
            clientSock.sendall(loggedOutMsg.encode())
    except:
        recipient.close()
        remove(recipient)
        error_handle += "Recipient connection error"
        clientSock.sendall(error_handle.encode())
    return

def sendUserlist(clientSock):
    preamble = "Current users: \n\n"
    for user in userDict.keys():
        preamble += user + "\n"
    clientSock.sendall(preamble.encode())

def deleteAcct(clientSock):
    toDelete = getClientUsername(clientSock)
    userDict.pop(toDelete)
    deleteConfirmation = "Account successfully deleted. Logging out..."
    clientSock.sendall(deleteConfirmation.encode())
    #TODO: Implement function which logs out user, closes out of program on client side


def parse(message, clientSock):
    message = message.split()
    operation = message[0]
    if operation == "Signin":
        signIn(message, clientSock)
    elif operation == "Send":
        sendMsg(message, clientSock)
    elif operation == "Userlist":
        sendUserlist(clientSock)
    elif operation == "Delete":
        deleteAcct(clientSock)
    else:
        pass


        
        


# listens and broadcasts messages to chat room
def client_thread(clientSock, ip):
    #server runs constantly
    while True:
        try:
            # get message from client, max length 280 chars
            message = clientSock.recv(280).decode()
            

            # print user who sent message and message on server terminal
            if message:
                print("<" + ip[0] + ">: " + message)
                
                # broadcast message to all users in chat
                # broadcast_message = "<" + ip[0] + ">: " + message
                parse(message, clientSock)
            
            # message has no content, remove connection
            else:
                remove(clientSock)

        except:
            continue

# broadcast message to all clients
def broadcast(message, sender):
    for clientSock in clientSockLst:
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






