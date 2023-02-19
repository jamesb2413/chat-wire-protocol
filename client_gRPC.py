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
        if helpers.checkValidUsername(username):

        signinLoop()

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("Congratulations! You have connected to the chat server.\n")

        existsBool = signinLoop()
        if existsBool:
            print("Please log in with your username")
            username = input("Username: ")
            unreadsOrError = stub.SignInExisting(chat_pb2.Username(name=username))

        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
