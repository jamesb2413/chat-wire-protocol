'''
Resources: 
1. python.org Socket Programming HOWTO by Gordon McMillan (https://docs.python.org/3/howto/sockets.html)
2. geeksforgeeks.org Simple Chat Room using Python by Deepak Srivatsav (https://www.geeksforgeeks.org/simple-chat-room-using-python/amp/)
'''
import socket
import sys
import select

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
# TODO: Add exception handling

print("Congratulations! You have connected to the chat server.")

# Determine if user has account or needs to sign up
existsBool = False
while True:
    existsInput = input("Do you already have an account? [Y/N]")
    if existsInput == 'Y' or existsInput == 'y':
        existsBool = True
        break
    elif existsInput == 'N' or existsInput == 'n':
        existsBool = False
        break
    else:
        print("Invalid response. Please answer with 'Y' or 'N'.")
# If user has account, log in
if existsBool:
    print("Please log in with your username and password.")
    username = input("Username: ")
    message = "Signin Existing " + username
    s.send(message.encode())
# If user does not have account, sign up
else:
    # Watch out for usernames that already exist
    print("Please create your username and password.")
    newUsername = input("New Username: ")
    message = "Signin New " + newUsername
    s.send(message.encode())


# Now, the user is logged in. Notify the user of possible functions.
print("Congratulations! You have successfully logged in to your account.")

# Check: Will there be problems if a message arrives between login and beginning of while loop?
print("If any messages arrive while you are logged in, they will be immediately displayed.")
print("Use the following commands to interact with the chat app: \n")
# if numMessages > 0:
    # print("R: Read new messages")
print(" -----------------------------------------------")
print("|L: List all accounts that exist on this server.|")
print("|S: Send a message to another user.             |")
print("|D: Delete account.                             |")
print(" ----------------------------------------------- \n")

# Unread msgs will display here

# Wait for input from either client or server
while True:
    socks_list = [sys.stdin, s] 

    read_socks, _, _ = select.select(socks_list,[],[]) 

    for read_sock in read_socks: 
        # Incoming message
        if read_sock == s: 
            message = read_sock.recv(2048).decode()
            print(message) 
            # TODO: close user connection, terminate program if server sends back that account was deleted
        # Input from user
        else: 
            # print("inside else")
            command = sys.stdin.readline()
            print("command: " + command)
            command = command.strip()
            # print("command read: '", command, "'")
            if command == 'S' or command == 's':
                send_to_user = input("Which user do you want to message? ")
                message = input("Type the message you would like to send. ")
                complete_msg = "Send " + send_to_user + " " + message
                s.send(complete_msg.encode())
                print("Message sent.")  
            if command == 'L' or command == 'l':
                complete_msg = "Userlist"
                s.send(complete_msg.encode())
                print("Fetching users... \n")
            if command == 'D' or command == 'd':
                delete = False
                while True:
                    deleteInput = input("Are you sure? Deleted accounts are permanently erased, and you will be logged off immediately. [Y/N] ")
                    if deleteInput == 'Y' or deleteInput == 'y':
                        delete = True
                        break
                    elif deleteInput == 'N' or deleteInput == 'n':
                        delete = False
                        break
                    else:
                        print("Invalid response. Please answer with 'Y' or 'N'.")
                if delete:
                    complete_msg = "Delete"
                    s.send(complete_msg.encode())
                    print("Deleting account... \n")

s.close() 