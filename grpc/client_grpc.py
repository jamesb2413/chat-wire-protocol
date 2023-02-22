import logging
import sys
from _thread import *
import time

import grpc
import chat_pb2
import chat_pb2_grpc
import helpers_grpc

def signinLoop(stub):
    existsBool = helpers_grpc.existingOrNew()
    if existsBool:
        print("Please log in with your username")
        username = input("Username: ")
        # Username error check
        if helpers_grpc.isValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.SignInExisting(chat_pb2.Username(name=username))
            eFlag, msg = unreadsOrError.errorFlag, unreadsOrError.unreads
    else:
        print("\nPlease create a new username.")
        username = input("New Username: ")
        # Username error check
        if helpers_grpc.isValidUsername(username):
            # Remove whitespace
            username = username.strip().lower()
            unreadsOrError = stub.AddUser(chat_pb2.Username(name=username))
            eFlag, msg = unreadsOrError.errorFlag, unreadsOrError.unreads
    if eFlag:
        print(msg)
        return signinLoop(stub)
    else:
        print("\nCongratulations! You have successfully logged in to your account.\n")
        print(msg)
        return username

def messageLoop(username, stub):
    command = sys.stdin.readline().strip()
    if command == 'S' or command == 's':
        while True:
            send_to_user = input("Which user do you want to message? \n Recipient username: ")
            # Username error checks
            if not helpers_grpc.isValidUsername(send_to_user):
                continue
            if send_to_user == username: 
                print("Cannot send message to self.\n")
                continue
            break
        message = input("Type the message you would like to send. \n Message: ")
        # Send sender username, recipient username, and message to the server & store confirmation response
        sender = chat_pb2.Username(name=username)
        recipient = chat_pb2.Username(name=send_to_user)
        payload = chat_pb2.Payload(msg=message)
        senderResponse = stub.Send(chat_pb2.SendRequest(sender=sender, recipient=recipient, sentMsg=payload))
        print(senderResponse.msg)
        print("Command:")
    if command == 'L' or command == 'l':
        wildcard = input("Optional text wildcard: ")
        if wildcard == "":
            wildcard = "*"
        listResponse = stub.List(chat_pb2.Payload(msg=wildcard))
        print("Fetching users... \n")
        print(listResponse.msg)
        print("Command:")
    if command == 'O' or command == 'o':
        logoutResponse = stub.Logout(chat_pb2.Username(name=username))
        print("Logging out...")
        time.sleep(0.2)
        print(logoutResponse.msg)
        time.sleep(0.2)
        return
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
            deleteResponse = stub.Delete(chat_pb2.Username(name=username))
            print("Deleting account... \n")
            time.sleep(0.2)
            print(deleteResponse.msg)
            time.sleep(0.2)
            return
        else:
            print("\nCommand: ")
    messageLoop(username, stub)

# Listens for messages from server's Listen response stream
def listen_thread(username, stub, responseStream):
    while True:
        try:
            response = next(responseStream)
            print(response.msg)
        except:
            return

def run():
    ip = '10.250.31.89'
    port = '8080'
    with grpc.insecure_channel('{}:{}'.format(ip, port)) as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("Congratulations! You have connected to the chat server.\n")

        while True:
            username = signinLoop(stub)
            # Now, the user is logged in. Notify the user of possible functions
            # Check: Will there be problems if a message arrives between login and beginning of while loop?
            print("If any messages arrive while you are logged in, they will be immediately displayed.\n")
            print("Use the following commands to interact with the chat app: \n")
            print(" -----------------------------------------------")
            print("|L: List all accounts that exist on this server.|")
            print("|S: Send a message to another user.             |")
            print("|O: Log Out.                                    |")
            print("|D: Delete account.                             |")
            print(" ----------------------------------------------- \n")
            print("Command: ")
            # Establish response stream to receive messages from server
            # responseStream is a generator of chat_pb2.Payload
            responseStream = stub.Listen(chat_pb2.Username(name=username))
            start_new_thread(listen_thread, (username, stub, responseStream))
            # Wait for input from command line
            messageLoop(username, stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
