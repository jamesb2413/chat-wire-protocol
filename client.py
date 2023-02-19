'''
Resources: 
1. python.org Socket Programming HOWTO by Gordon McMillan (https://docs.python.org/3/howto/sockets.html)
2. geeksforgeeks.org Simple Chat Room using Python by Deepak Srivatsav (https://www.geeksforgeeks.org/simple-chat-room-using-python/amp/)
'''
import socket
import sys
import select
import time
import helpers

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
username = ""

# Loops requesting user input until a valid sign in. Returns valid username
def signinLoop():
    existsBool = helpers.existingOrNew()
    if existsBool:
        print("Please log in with your username")
        username = input("Username: ")
        message = "I Existing "
    else:
        print("\nPlease create a new username.")
        username = input("New Username: ")
        message = "I New "
    # Username error check
    if helpers.isValidUsername(username):
        # Remove whitespace
        username = username.split()[0]
        message += username
        s.send(message.encode())
        time.sleep(0.1)
        # Catch errors: Existing: (1) account does not exist, (2) account already logged in elsewhere
        # New: Username already in use by a different account
        read_socks, _, _ = select.select(socks_list,[],[]) 
        for read_sock in read_socks: 
            message = read_sock.recv(2048).decode()
            messageSplit = message.split(' ', 1)
            # Error message from server
            if messageSplit[0] == "I":
                print(messageSplit[1])
            # Unread messages
            else: 
                assert(messageSplit[0] == "You")
                print("\nCongratulations! You have successfully logged in to your account.\n")
                print(messageSplit[0] + ' ' + messageSplit[1])
                return username
    signinLoop()

# Parse input from either command line or server and do the correct action
def messageLoop(username):
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
                send_to_user = input("Which user do you want to message? \n Recipient username: ")
                # Username error checks
                if not helpers.isValidUsername(send_to_user):
                    continue
                if send_to_user == username: 
                    print("Cannot send message to self.\n")
                    continue
                message = input("Type the message you would like to send. \n Message: ")
                complete_msg = "S " + username + " " + send_to_user + " " + message
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
                confirm = False
                confirmInput = input("Are you sure? Deleted accounts are permanently erased, "
                                    "and you will be logged off immediately. [Y/N] ")
                while True:
                    if confirmInput == 'Y' or confirmInput == 'y':
                        confirm = True
                        break
                    elif confirmInput == 'N' or confirmInput == 'n':
                        confirm = False
                        break
                    else:
                        print("Invalid response. Please answer with 'Y' or 'N'.")
                if confirm:
                    complete_msg = "D " + username
                    s.send(complete_msg.encode())
                    print("Deleting account... \n")
                    time.sleep(0.5)
                    print("Goodbye!\n")
                    time.sleep(0.5)
                    return
                else:
                    print("\nCommand: ")
            if command == 'O' or command == 'o':
                complete_msg = "O " + username
                print("complete_msg: ", complete_msg)
                s.send(complete_msg.encode())
                print("Logging out...")
                time.sleep(0.5)
                print("Goodbye!\n")
                time.sleep(0.5)
                return
    messageLoop(username)

# Loop indefinitely so user can start over after logging out.
while True: 
    username = signinLoop()
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
    messageLoop(username)