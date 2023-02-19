## Used in client
# TODO: Unit test
def isValidUsername(username):
    usernameWords = username.split()
    # If user inputs empty string, whitespace, or multiple words as username
    if len(usernameWords) != 1:
        print("Usernames can only be one word containing letters, numbers, and special characters. " 
              "Please try again with a different username.\n")
        return False
    return True

def existingOrNew():
    print("Sign In: ")
    # Determine if user has account or needs to sign up
    existsInput = input("Do you already have an account? [Y/N] ")
    if existsInput == 'Y' or existsInput == 'y':
        return True
    elif existsInput == 'N' or existsInput == 'n':
        return False
    else:
        print("Invalid response. Please answer with 'Y' or 'N'.")
        return existingOrNew()


## Used in server
def enqueueMsg(message, recipient, clientDict):
    clientDict[recipient][2].append(message)
    return clientDict[recipient][2][-1]

def addUser(username, clientSock, clientDict):
    # If username is already taken, notify user and request new username
    if username in clientDict:
        collideAlert = ("I This username is already taken by another account. Please " 
                        "try again with a different username.\n")
        try:
            clientSock.sendall(collideAlert.encode())
        except:
            pass
        return -1
    # If username is valid, create new user in userDict
    clientDict[username] = [clientSock, True, []]
    return clientDict[username]
    
# Sign in to existing account OR create new account via call to addUser
def signIn(message, clientSock, clientDict):
    # Catching username errors
    try:
        username = message[2].lower()
    except:
        print("Critical Signin Error")
        return -1

    # From clientDict: [socketObj, loggedOnBool, messageQueue]
    userAttributes = []

    if message[1] == "Existing":
        try:
            userAttributes = clientDict[username]
            # If user is already logged in, deny access
            if userAttributes[1] == True:
                doubleLogAlert = ("I This user is already logged in on another device. Please " 
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
            dneAlert = ("I No users exist with this username. Please double check that you typed correctly "
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
    sender = message[1]
    recipient = message[2]

    # Error handling message 
    error_handle = "Error sending message to " + recipient + ": "

    raw_msg = " ".join(message[3:])

    # Get recipient
    try:
        recipientAttributes = clientDict[recipient]
        loggedIn = recipientAttributes[1]
    except:
        error_handle += "User does not exist.\n"
        try:
            clientSock.sendall(error_handle.encode())
        except:
            pass
        return -1

    # Send message to recipient
    try:
        payload = "\nFrom " + sender + ": " + raw_msg + "\n"
        # print("payload is: " + payload)

        # If user is logged in, send the message
        if loggedIn:
            try:
                recipientSock = recipientAttributes[0]
                recipientSock.sendall(payload.encode())
            except:
                pass
        # If user is logged out, add to their queue
        else:
            enqueueMsg(payload, recipient, clientDict)
        
        # Notify sender that message has been sent.
        senderNote = "Message sent.\n"
        try:
            clientSock.sendall(senderNote.encode())
        except:
            pass

        return 1

    except:
        error_handle += "Recipient connection error"
        try:
            clientSock.sendall(error_handle.encode())
        except:
            pass
        return -2
    
def sendUserlist(message, clientSock, clientDict):
    wildcard = message[1].lower()
    allUsers, matches = list(clientDict.keys()), list(clientDict.keys())

    # return list of all users
    if wildcard == "":
        pass

    # return list of qualifying users
    elif "*" in wildcard:
        starIdx = wildcard.find("*")
        for u in allUsers:
            # Chars before star (if any) must match exactly
            if u[0:starIdx] != wildcard[0:starIdx]:
                matches.remove(u)
            # Any number of chars match star. 
            # Chars after star must match exactly.
            if starIdx < len(wildcard) - 1:
                afterStar = wildcard[starIdx + 1:]
                if len(u) < len(afterStar):
                    matches.remove(u)
                else:
                    uAfterStar = u[-len(afterStar):]
                    print(afterStar)
                    print(uAfterStar)
                    if afterStar != uAfterStar:
                        matches.remove(u)
        
    # return list of specific user
    else:
        matches = []
        for u in allUsers:
            if u == wildcard:
                matches.append(u)

    # build formatted message for client
    userListMsg = "---------------\n"
    userListMsg += "Matching users: \n"
    for user in matches:
        userListMsg += user + "\n"
    userListMsg += "---------------\n"
    try:
        clientSock.sendall(userListMsg.encode())
    except:
        pass
    return matches

def deleteAcct(message, clientDict):
    toDelete = message[1]
    clientDict.pop(toDelete)
    return toDelete

def logOut(message, clientDict):
    toLogOut = message[1]
    clientDict[toLogOut][1] = False
    return toLogOut