'''
Resources: 
1. python.org Socket Programming HOWTO by Gordon McMillan (https://docs.python.org/3/howto/sockets.html)
2. geeksforgeeks.org Simple Chat Room using Python by Deepak Srivatsav (https://www.geeksforgeeks.org/simple-chat-room-using-python/amp/)
'''
import socket
import sys
import select
import time

ip = ''
port = -1
if len(sys.argv) != 3: 
    print("Connect to Chat:")
    ip = input("Input server socket IP address: ")
    port = int(input("Input server socket port number: "))
else:
    ip = str(sys.argv[1]) 
    port = int(sys.argv[2]) 
# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server at the given IP address and port
s.connect((ip, port))
socks_list = [sys.stdin, s] 
read_socks = []

print("Congratulations! You have connected to the chat server.\n")

def signinLoop():
    print("Sign In: ")
    # Determine if user has account or needs to sign up
    existsBool = False
    while True:
        existsInput = input("Do you already have an account? [Y/N] ")
        if existsInput == 'Y' or existsInput == 'y':
            existsBool = True
            break
        elif existsInput == 'N' or existsInput == 'n':
            existsBool = False
            break
        else:
            print("Invalid response. Please answer with 'Y' or 'N'.")
    if existsBool:
        print("Please log in with your username and password.")
        username = input("Username: ")
        message = "I Existing " + username
        s.send(message.encode())
        time.sleep(0.1)
        # Catch errors: (1) account does not exist, (2) account already logged in elsewhere
        read_socks, _, _ = select.select(socks_list,[],[]) 
        for read_sock in read_socks: 
            message = read_sock.recv(2048).decode()
            messageSplit = message.split(' ', 1)
            # Error message from server
            if messageSplit[0] == "S":
                print(messageSplit[1])
            # Unread messages
            elif messageSplit[0] == "You":
                print("\nCongratulations! You have successfully logged in to your account.\n")
                print(messageSplit[0] + ' ' + messageSplit[1])
                return
            else:
                return
        signinLoop()
    else:
        print("\nPlease create a new username.")
        newUsername = input("New Username: ")
        message = "I New " + newUsername
        s.send(message.encode())
        time.sleep(0.1)
        # Catch errors: username already in use by a different account
        read_socks, _, _ = select.select(socks_list,[],[])  
        for read_sock in read_socks: 
            message = read_sock.recv(2048).decode()
            messageSplit = message.split(' ', 1)
            # Error message from server
            if messageSplit[0] == "S":
                print(messageSplit[1])
            # Unread messages
            elif messageSplit[0] == "You":
                print("\nCongratulations! You have successfully logged in to your account.\n")
                print(messageSplit[0] + ' ' + messageSplit[1])
                return
        signinLoop()

# Parse input from either command line or server and do the correct action
def messageLoop():
    read_socks, _, _ = select.select(socks_list,[],[]) 

    for read_sock in read_socks: 
        # Incoming message
        if read_sock == s: 
            message = read_sock.recv(2048).decode()
            print(message) 
            print("Command:")
            # TODO: close user connection, terminate program if server sends back that account was deleted
        # Input from user
        else: 
            command = sys.stdin.readline()
            command = command.strip()
            if command == 'S' or command == 's':
                # TODO: Make sure send_to_user is a valid username
                send_to_user = input("Which user do you want to message? \n Recipient username: ")
                message = input("Type the message you would like to send. \n Message: ")
                complete_msg = "S " + send_to_user + " " + message
                s.send(complete_msg.encode())
            if command == 'L' or command == 'l':
                complete_msg = "L "
                wildcard = input("Optional text wildcard: ")
                if wildcard == "":
                    wildcard = "*"
                complete_msg += wildcard
                s.send(complete_msg.encode())
                print("Fetching users... \n")
            if command == 'D' or command == 'd':
                delete = False
                deleteInput = input("Are you sure? Deleted accounts are permanently erased, and you will be logged off immediately. [Y/N] ")
                while True:
                    if deleteInput == 'Y' or deleteInput == 'y':
                        delete = True
                        break
                    elif deleteInput == 'N' or deleteInput == 'n':
                        delete = False
                        break
                    else:
                        print("Invalid response. Please answer with 'Y' or 'N'.")
                if delete:
                    complete_msg = "D"
                    s.send(complete_msg.encode())
                    print("Deleting account... \n")
                    time.sleep(0.5)
                    print("Goodbye!\n")
                    time.sleep(0.5)
                    return
                else:
                    print("\nCommand: ")
            if command == 'O' or command == 'o':
                complete_msg = "O"
                s.send(complete_msg.encode())
                print("Logging out...")
                time.sleep(0.5)
                print("Goodbye!\n")
                time.sleep(0.5)
                return
    messageLoop()

# Loop indefinitely so user can start over after logging out.
while True: 
    signinLoop()
    # Now, the user is logged in. Notify the user of possible functions
    # Check: Will there be problems if a message arrives between login and beginning of while loop?
    print("If any messages arrive while you are logged in, they will be immediately displayed.\n")
    print("Use the following commands to interact with the chat app: \n")
    # if numMessages > 0:
        # print("R: Read new messages")
    print(" -----------------------------------------------")
    print("|L: List all accounts that exist on this server.|")
    print("|S: Send a message to another user.             |")
    print("|O: Log Out.                                    |")
    print("|D: Delete account.                             |")
    print(" ----------------------------------------------- \n")
    print("Command: ")
    # Wait for input from either command line or server
    messageLoop()