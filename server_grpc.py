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
        eFlag, msg = helpers_grpc.signInExisting(username.name, self.clientDict)
        return chat_pb2.UnreadsOrError(errorFlag=eFlag, unreads=msg)
    
    def AddUser(self, username, context):
        eFlag, msg = helpers_grpc.addUser(username.name, self.clientDict)
        return chat_pb2.UnreadsOrError(errorFlag=eFlag, unreads=msg)

    def Send(self, sender, recipient, request, context):
        response = helpers_grpc.sendMsg(sender.name, recipient.name, request.msg, self.clientDict)
        return chat_pb2.Payload(msg=response)

    # usernameStream only comes from logged-in user
    def Listen(self, usernameStream, context):
        for username in usernameStream:
            # Message queued
            if len(self.clientDict[username][1]) > 0:
                # Yield first message
                yield chat_pb2.Payload(msg=self.clientDict[username][1].pop(0))


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