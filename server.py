import socket
import select
import sys
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
# Map of existing users and their messages { username : [socketObj, loggedOnBool, messageQueue ] }
userDict = {}

## Helper functions
# Store messages while user is logged off
def enqueueMsg(message, recipient):
    userDict[recipient][2].append(message)

# Get username from client socket object
def getClientUsername(clientSock):
    print("----------")
    print("getClientUsername clientSock: ", clientSock)
    print("----------")
    for key in userDict.keys():
        if userDict[key][0] == clientSock:
            return key
    print("CRITICAL ERROR: Operating on nonexistent user")

## Key functions
# Create new account
def addUser(username, clientSock):
    # If username is already taken, notify user and request new username
    if username in userDict:
        collideAlert = ("S This username is already taken by another account. Please " 
                        "try again with a different username.\n")
        clientSock.sendall(collideAlert.encode())
        return
    # If username is valid, create new user in userDict
    userDict[username] = [clientSock, True, []]
    return userDict[username]

# Sign in to existing account OR create new account via call to addUser
def signIn(message, clientSock):
    thisUser = []
    try:
        username = message[2]
    except:
        print("2")
        # If user inputs ' ' as username
        invalidMsg = "S This username is invalid. Please try again with a different username.\n"
        clientSock.sendall(invalidMsg.encode())
        return

    # If user inputs more than one word
    if len(message) > 3:
        oneWordMsg = "S Your username can only be one word. Please try again."
        clientSock.sendall(oneWordMsg.encode())
        return

    if message[1] == "Existing":
        try:
            thisUser = userDict[username]
            # If user is already logged in, deny access
            if thisUser[1] == True:
                doubleLogAlert = ("S This user is already logged in on another device. Please " 
                                  "log out in the other location and try again.\n")
                clientSock.sendall(doubleLogAlert.encode())
                return
            else:
                thisUser[1] = True
                thisUser[0] = clientSock
        except:
            # If account does not exist
            dneAlert = ("S No users exist with this username. Please double check that you typed correctly "
                        "or create a new account with this username.\n")
            clientSock.sendall(dneAlert.encode())
            return
    # Create new user with input username
    else:
        # TODO: Make sure username is valid, i.e. at least one non-whitespace character
        thisUser = addUser(username, clientSock)
        # Handle collisions
        if thisUser is None:
            return
    # TODO: Change this to not conflict with create acct errors
    unreads = userDict[username][2]
    unreadNum = str(len(unreads))
    unreadAlert = "You have " + unreadNum + " unread messages:\n\n"
    for msg in unreads:
        unreadAlert += msg + "\n\n"
    userDict[username][2] = []
    clientSock.sendall(unreadAlert.encode())

def sendMsg(message, clientSock):
    sender = getClientUsername(clientSock)
    recipient = message[1]

    # Error handling message 
    error_handle = "Error sending message to " + recipient + ": "

    if recipient == sender:
        error_handle += "Cannot send message to self\n"
        clientSock.sendall(error_handle.encode())
        return

    raw_msg = " ".join(message[2:])

    # Getting socket of user message was sent to
    try:
        recipientSock = userDict[recipient][0]
        loggedIn = userDict[recipient][1]
    except:
        error_handle += "User does not exist\n"
        clientSock.sendall(error_handle.encode())
        return

    # Send message to recipient
    try:
        payload = "\nFrom " + sender + ": " + raw_msg + "\n"
        senderNote = "Message sent.\n"
        print("payload is: " + payload)
        # If user is logged in, send the message
        if loggedIn:
            recipientSock.sendall(payload.encode())
        # If user is logged out, add to their queue
        # NOTE Not sure if this works since no log out function yet to set 
        # bool to false
        else:
            enqueueMsg(payload, recipient)
        clientSock.sendall(senderNote.encode())
    except:
        recipient.close()
        remove(recipient)
        error_handle += "Recipient connection error"
        clientSock.sendall(error_handle.encode())
    return

def sendUserlist(clientSock):
    userListMsg = "---------------\n"
    userListMsg += "Current users: \n"
    for user in userDict.keys():
        userListMsg += user + "\n"
    userListMsg += "---------------\n"
    clientSock.sendall(userListMsg.encode())

def deleteAcct(clientSock):
    toDelete = getClientUsername(clientSock)
    userDict.pop(toDelete)

def logOut(clientSock):
    toLogOut = getClientUsername(clientSock)
    userDict[toLogOut][1] = False


# Parse message according to wire protocol to determine which function to call
def parse(message, clientSock):
    message = message.split()
    operation = message[0]
    if operation == "I":
        signIn(message, clientSock)
    elif operation == "S":
        sendMsg(message, clientSock)
    elif operation == "L":
        sendUserlist(clientSock)
    elif operation == "D":
        deleteAcct(clientSock)
    elif operation == "O":
        logOut(clientSock)
    else:
        pass

## Chat loops
# Listens for messages from this client and parses to perform necessary functions
def client_thread(clientSock, ip):
    # Server listens indefinitely
    while True:
        # print('inside thread: ', clientSock)
        try:
            # Get message from client, max length 280 chars
            message = clientSock.recv(280).decode()
            
            # print IP address of user who sent message and message on server terminal
            # TODO: Do we want to print message to server?
            if message:
                print("<" + ip[0] + ">: " + message)
                
                # Determine necessary function based on wire protocol
                parse(message, clientSock)
            
            # Message has no content, remove connection
            else:
                logOut(clientSock)
                remove(clientSock)
                return
        except:
            continue

# removes specified client from chat
def remove(clientSock):
    print("removed!")
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
    print('clientSockLst: \n')
    for clientSock in clientSockLst:
        print(clientSock, "\n")





