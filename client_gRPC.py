import grpc
import chat_pb2
import chat_pb2_grpc
import helpers 
import helpers_gRPC

def signinLoop():
    existsBool = helpers.existingOrNew()
    if existsBool:
        print("Please log in with your username")
        username = input("Username: ")
        # Username error check
        if helpers.checkValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.SignInExisting(chat_pb2.Username(name=username))
    else:
        print("\nPlease create a new username.")
        username = input("New Username: ")
        # Username error check
        if helpers.checkValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.SignInNews(chat_pb2.Username(name=username))

    signinLoop()

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("Congratulations! You have connected to the chat server.\n")

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
        

        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
