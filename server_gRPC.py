from concurrent import futures
import logging

import grpc
import chat_pb2
import chat_pb2_grpc
import helpers
import helpers_grpc

class ChatServicer(chat_pb2_grpc.ChatServicer):

    def __init__(self):
        self.clientDict = {}

    def SignInExisting(self, username, context):
        eFlag, msg = helpers_grpc.signInExisting(username, self.clientDict)
        return chat_pb2.UnreadsOrError(errorFlag = eFlag, message = msg)
    
    def AddUser(self, username, context):
        eFlag, msg = helpers_grpc.addUser(username, self.clientDict)
        return chat_pb2.UnreadsOrError(errorFlag = eFlag, message = msg)

    # def SayHello(self, request, context):
    #     return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()