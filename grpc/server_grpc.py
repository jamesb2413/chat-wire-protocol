from concurrent import futures
import logging

import grpc
import chat_pb2
import chat_pb2_grpc
import helpers_grpc

class ChatServicer(chat_pb2_grpc.ChatServicer):

    def __init__(self):
        # {username : [loggedOnBool, [messageQueue]]}
        self.clientDict = {}

    def SignInExisting(self, username, context):
        eFlag, msg = helpers_grpc.signInExisting(username.name, self.clientDict)
        return chat_pb2.Unreads(errorFlag=eFlag, unreads=msg)
    
    def AddUser(self, username, context):
        eFlag, msg = helpers_grpc.addUser(username.name, self.clientDict)
        return chat_pb2.Unreads(errorFlag=eFlag, unreads=msg)

    def Send(self, sendRequest, context):
        response = helpers_grpc.sendMsg(sendRequest.sender.name, sendRequest.recipient.name, 
                                        sendRequest.sentMsg.msg, self.clientDict)
        return chat_pb2.Payload(msg=response)

    # usernameStream only comes from logged-in user
    def Listen(self, username, context):
        while True:
            # If any messages are queued
            if len(self.clientDict[username.name][1]) > 0:
                # Yield first message
                yield chat_pb2.Payload(msg=self.clientDict[username.name][1].pop(0))
            # Stop stream if user logs out
            if self.clientDict[username.name][0] == False:
                break

    def List(self, wildcard, context):
        payload = helpers_grpc.sendUserlist(wildcard.msg, self.clientDict)
        return chat_pb2.Payload(msg=payload)

    def Logout(self, username, context):
        self.clientDict[username.name][0] = False
        return chat_pb2.Payload(msg="Goodbye!\n")

    def Delete(self, username, context):
        self.clientDict.pop(username.name)
        return chat_pb2.Payload(msg="Goodbye!\n")


def serve():
    ip = '10.250.31.89'
    port = '8080'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"{ip}:{port}")
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()