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
    unreads = "You have " + unreadsNum + " unread messages:\n\n"
    for msg in unreadsLst:
        unreads += msg + "\n\n"
    # Reset unreads queue
    userAttributes[1] = []
    return (False, unreads)
    
# Returns error message or sender confirmation & enqueues message for recipient
def sendMsg(sender, recipient, message, clientDict):
    # Error handling message 
    error_handle = "Error sending message to " + recipient + ": "

    # Get recipient data
    try:
        recipientAttributes = clientDict[recipient]
        loggedIn = recipientAttributes[1]
    except:
        error_handle += "User does not exist\n"
        return error_handle

    # Send message to recipient
    try:
        recipientMsg = "\nFrom " + sender + ": " + message + "\n"
        senderNote = "Message sent.\n"
        # print("payload is: " + payload)

        # Enqueue the message
        clientDict[recipient][1].append(recipientMsg)
        return senderNote
    except:
        error_handle += "Recipient connection error"
        return error_handle
    
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