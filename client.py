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
    elif existsInput == 'N' or existsInput == 'N':
        existsBool = False
        break
    else:
        print("Invalid response. Please answer with 'Y' or 'N'.")
# If user has account, log in
if existsBool:
    print("Please log in with your username and password.")
    username = input("Username: ")
    # TODO: Call server function to find username or notify user if username does not exist
# If user does not have account, sign up
else:
    print("Please create your username and password.")
    newUsername = input("New Username: ")
    # TODO: Call server function to store username or notify user if username is taken

# Now, the user is logged in. Notify the user of possible functions.
print("Congratulations! You have successfully logged in to your account.")
# TODO: Call server function to determine number of new messages
# print("Since you last logged in, you have received ", numMessages, "messages.")
# Check: Will there be problems if a message arrives between login and beginning of while loop?
print("If a message arrives while you are logged in, it will be immediately displayed.")
print("Use the following commands to interact with the chat app:")
# if numMessages > 0:
    # print("R: Read new messages")
print("L: List all accounts that exist on this server.")
print("S: Send a message to another user.")
print("D: Delete account.")

# Wait for input from either client or server
while True:
    socks_list = [sys.stdin, s] 

    read_socks, _, _ = select.select(socks_list,[],[]) 

    for read_sock in read_socks: 
        # Incoming message
        if read_sock == s: 
            message = read_sock.recv(2048).decode()
            print(message) 
        # Input from user
        else: 
            # print("inside else")
            command = sys.stdin.readline() 
            # print("command read: '", command, "'")
            # if command == ' S\n ' or command == ' s\n ':
            
            message = input("Type the message you would like to broadcast.")
            s.send(message.encode())
            print("Message sent.")  
s.close() 