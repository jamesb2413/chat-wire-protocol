def enqueueMsg(message, recipient, clientDict):
        clientDict[recipient][2].append(message)
        return clientDict[recipient][2][-1]

# Get username from client socket object
def getClientUsername(clientSock, clientDict):
    print("----------")
    print("getClientUsername clientSock: ", clientSock)
    print("----------")
    for key in clientDict.keys():
        if clientDict[key][0] == clientSock:
            return key
    print("CRITICAL ERROR: Operating on nonexistent user")

def addUser(username, clientSock, clientDict):
    # If username is already taken, notify user and request new username
    if username in clientDict:
        collideAlert = ("S This username is already taken by another account. Please " 
                        "try again with a different username.\n")
        try:
            clientSock.sendall(collideAlert.encode())
        except:
            pass
        return -1
    # If username is valid, create new user in userDict
    clientDict[username] = [clientSock, True, []]
    return clientDict[username]

def clientSignIn(username):
    # If user inputs '' or ' ' as username
    if not username or not username.strip():
        return "This username is invalid. Please try again with a different username.\n"


# Sign in to existing account OR create new account via call to addUser
def signIn(username, clientDict):
    # If user inputs '' or ' ' as username
    if not username or not username.strip():
        return "This username is invalid. Please try again with a different username.\n"

    userAttributes = []

    # If user inputs more than one word
    if len(message) > 3:
        oneWordMsg = "S Your username can only be one word. Please try again."
        try:
            clientSock.sendall(oneWordMsg.encode())
        except:
            pass
        return -2

    if message[1] == "Existing":
        try:
            userAttributes = clientDict[username]
            # If user is already logged in, deny access
            if userAttributes[1] == True:
                doubleLogAlert = ("S This user is already logged in on another device. Please " 
                                "log out in the other location and try again.\n")
                try:
                    clientSock.sendall(doubleLogAlert.encode())
                except:
                    pass
                return -3
            # Set user as logged in and update socket object
            else:
                userAttributes[1] = True
                userAttributes[0] = clientSock
        except:
            # If account does not exist
            dneAlert = ("S No users exist with this username. Please double check that you typed correctly "
                        "or create a new account with this username.\n")
            try:
                clientSock.sendall(dneAlert.encode())
            except:
                pass
            return -4
    # Create new user with input username
    else:
        userAttributes = addUser(username, clientSock, clientDict)
        # Handle collisions
        if userAttributes == -1:
            return -5
    unreads = clientDict[username][2]
    unreadNum = str(len(unreads))
    unreadAlert = "You have " + unreadNum + " unread messages:\n\n"
    for msg in unreads:
        unreadAlert += msg + "\n\n"
    clientDict[username][2] = []
    try:
        clientSock.sendall(unreadAlert.encode())
    except:
        pass
    return 1

def sendMsg(message, clientSock, clientDict):
    sender = getClientUsername(clientSock, clientDict)
    recipient = message[1]

    # Error handling message 
    error_handle = "Error sending message to " + recipient + ": "

    if recipient == sender:
        error_handle += "Cannot send message to self\n"
        try:
            clientSock.sendall(error_handle.encode())
        except:
            pass
        return -1

    raw_msg = " ".join(message[2:])

    # Getting socket of user message was sent to
    try:
        recipientSock = clientDict[recipient][0]
        loggedIn = clientDict[recipient][1]
    except:
        error_handle += "User does not exist\n"
        try:
            clientSock.sendall(error_handle.encode())
        except:
            pass
        return -2

    # Send message to recipient
    try:
        payload = "\nFrom " + sender + ": " + raw_msg + "\n"
        senderNote = "Message sent.\n"
        print("payload is: " + payload)
        # If user is logged in, send the message
        if loggedIn:
            try:
                recipientSock.sendall(payload.encode())
            except:
                pass
        # If user is logged out, add to their queue
        # NOTE Not sure if this works since no log out function yet to set 
        # bool to false
        else:
            enqueueMsg(payload, recipient, clientDict)
        try:
            clientSock.sendall(senderNote.encode())
        except:
            pass
        return 1
    except:
        recipient.close()
        error_handle += "Recipient connection error"
        try:
            clientSock.sendall(error_handle.encode())
        except:
            pass
        return -3
    
def sendUserlist(message, clientSock, clientDict):
    wildcard = message[1]
    matches, res = list(clientDict.keys()), list(clientDict.keys())

    # return list of all users
    if wildcard == "":
        pass

    # return list of qualifying users
    elif "*" in wildcard:
        starIdx = wildcard.find("*")
        for u in matches:
            if u[0:starIdx] != wildcard[0:starIdx]:
                res.remove(u)
    
    # return list of specific user
    else:
        res = []
        for u in matches:
            if u == wildcard:
                res.append(u)

    # build formatted message for client
    userListMsg = "---------------\n"
    userListMsg += "Matching users: \n"
    for user in res:
        userListMsg += user + "\n"
    userListMsg += "---------------\n"
    try:
        clientSock.sendall(userListMsg.encode())
    except:
        pass
    return res

def deleteAcct(clientSock, clientDict):
    toDelete = getClientUsername(clientSock, clientDict)
    clientDict.pop(toDelete)
    return toDelete

def logOut(clientSock, clientDict):
    toLogOut = getClientUsername(clientSock, clientDict)
    clientDict[toLogOut][1] = False
    return toLogOut