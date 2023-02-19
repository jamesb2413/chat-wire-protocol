import grpc
import chat_pb2
import chat_pb2_grpc

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
    return existsBool

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("Congratulations! You have connected to the chat server.\n")

        existsBool = signinLoop()
        if existsBool:
            print("Please log in with your username and password.")
            username = input("Username: ")
            unreads = stub.SignInExisting(chat_pb2.Username(name=username))
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
