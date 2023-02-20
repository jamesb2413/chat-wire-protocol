import grpc
import chat_pb2
import chat_pb2_grpc
import helpers 
import helpers_grpc
import logging

def signinLoop(stub):
    existsBool = helpers.existingOrNew()
    if existsBool:
        print("Please log in with your username")
        username = input("Username: ")
        # Username error check
        if helpers.isValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.SignInExisting(chat_pb2.Username(name=username))
            eFlag, msg = unreadsOrError.errorFlag, unreadsOrError.unreads
    else:
        print("\nPlease create a new username.")
        username = input("New Username: ")
        # Username error check
        if helpers.isValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.AddUser(chat_pb2.Username(name=username))
            eFlag, msg = unreadsOrError.errorFlag, unreadsOrError.unreads
    if eFlag:
        print(msg)
        return signinLoop()
    else:
        print("\nCongratulations! You have successfully logged in to your account.\n")
        print(msg)
        return username

def messageLoop(username, stub):
    serverStream(stub)
    command = sys.stdin.readline().strip()
    if command == 'S' or command == 's':
        while True:
            send_to_user = input("Which user do you want to message? \n Recipient username: ")
            # Username error checks
            if not helpers.isValidUsername(send_to_user):
                continue
            if send_to_user == username: 
                print("Cannot send message to self.\n")
                continue
            break
        message = input("Type the message you would like to send. \n Message: ")
        # Send sender username, recipient username, and message to the server & store confirmation response
        senderResponse = stub.Send(chat_pb2.Username(name=username), 
                                   chat_pb2.Username(name=send_to_user), 
                                   chat_pb2.RequestMessage(payload=message))
        

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("Congratulations! You have connected to the chat server.\n")

        while True:
            username = signinLoop(stub)
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
            # Establish bi-directional stream to receive messages from server
            responseStream = stub.Listen(chat_pb2.Username(name=username))
            # Wait for input from command line
            messageLoop(username, stub)
        

        # response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))


if __name__ == '__main__':
    logging.basicConfig()
    run()
