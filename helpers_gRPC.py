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

# Create new user with input username. Returns (errorFlag, errorMsg).
def addUser(username, clientDict):
    # If username is already taken, notify user and request new username
    if username in clientDict:
        return (True, "This username is already taken by another account. Please " +
                      "try again with a different username.\n")
    # If username is valid, create new user in userDict
    clientDict[username] = [True, []]
    return (False, "")

# Sign in to existing account. Returns (errorFlag, message).
def signInExisting(username, clientDict):
    try:
        # From clientDict: [loggedOnBool, messageQueue]
        userAttributes = clientDict[username]
        # If user is already logged in, return error
        if userAttributes[0] == True:
            return (True, "This user is already logged in on another device. Please " +
                          "log out in the other location and try again.\n")
        # Set user as logged in and update socket object
        else:
            userAttributes[0] = True
    except:
        # If account does not exist
        return (True, "No users exist with this username. Please double check that you typed correctly " +
                      "or create a new account with this username.\n")
    unreadsLst = userAttributes[1]
    unreadsNum = str(len(unreadsLst))
    unreads = "You have " + unreadNum + " unread messages:\n\n"
    for msg in unreadsLst:
        unreads += msg + "\n\n"
    # Reset unreads queue
    userAttributes[1] = []
    return (False, unreads)
    

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