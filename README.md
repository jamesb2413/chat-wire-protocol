# chat-wire-protocol
In /custom_wire_protocol: A simple client/server chat application implemented with a custom wire protocol

In /grpc: A simple client/server chat application implemented using gRPC

Sections:
1. Setup (pull from github, required libraries, etc.)
2. Startup
3. Operation - Custom Wire Protocol
4. Operation - gRPC
5. Operation - Unit tests

-----------------------------------------------------------------------------------------------------------------------------------------------
Overview.

This application is a simple chat room that implements client/server connection and one-to-one client communication. It can be run on a single 
machine, as well as between multiple different machines. There are other functionalities in addition to sending messsages, which include listing 
all or a subset of users who exist in the server, login/logout, and deleting one's account. There are two implementations of this application, one 
which uses a custom wire protocol to allow communication between the client and server, and another leveraging gRPC to avoid needing to define a 
custom wire protocol. There are also unit tests for each implementation.

In order to run any FILE.py, in the terminal, enter "python FILE.py".

-----------------------------------------------------------------------------------------------------------------------------------------------
1. Setup

The files for these applications are stored in a public GitHub repo, which can be accessed at https://github.com/jamesb2413/chat-wire-protocol.
To get the files from this repository to your local machine, run the following command in the terminal when in the desired location for the files 
to be downloaded to:

    git clone https://github.com/jamesb2413/chat-wire-protocol

Now, you should have all of the files necessary to run the applications. There are a couple python libraries that are required to run these 
programs. You will need the socket library in addition to the unittest library to run the tests, both of which are built into the standard python 
library.

gRPC install and setup instructions can be found in the gRPC documentation Python Quick Start guide: 
https://grpc.io/docs/languages/python/quickstart/. This will require installation of grpcio and grpcio-tools using pip or anaconda.

-----------------------------------------------------------------------------------------------------------------------------------------------
2. Startup

***Note. the custom wire protocol server only works with the custom wire protocol client and vice versa, and same for the gRPC client and server***

The first step to using the custom wire protocol chat application is to run the program. Because this application is a client/server application, 
the server must be running at all times in order for clients to be able to connect to it, save their data on it, and access all the features the 
application has to offer. So, we first want to start up the server. To do this, run:

    python server.py IP_ADDRESS PORT_NO

Where IP_ADDRESS is the IP address which you want to run the server on and PORT_NO is an empty port to allow users to connect to. If you are 
running the application on just one machine, use IP address 127.0.0.1 (localhost), otherwise you will need to look up your IPv4 (on Mac, Settings ->
Network -> Advanced -> TCP/IP, listed as IPv4), start the server using this address, and give this address to each client that wishes to connect to 
the chat server. As for the port number, 8080 works well for both one and multiple machines. 

To set up the server using gRPC, there is no need to specify the IP and port. Simply enter

    python server.py

Now that the server is running, clients can begin to connect to it. For the custom wire protocol version, run

    python client.py IP_ADDRESS PORT_NO

to start the client. 

For gRPC, run

    python client.py
    
Congratulations! At this point, you should connect to the server and recieve a welcome message. 

-----------------------------------------------------------------------------------------------------------------------------------------------
3. Operation - All operations are identical for the gRPC and custom wire protocol applications.

Now that the server is running and clients are connected, you will be asked if you already have a username. If so, enter 'y', else 'n'. If 'y' 
is entered, you will be prompted for your username, and if it matches a username in the database, you will be logged in. If 'n', then you will 
be asked to create a username. The username must be a single string with no spaces, greater than 0 characters. It also must be unique, so 
entering a username that someone else already has will trigger an error.

Once you are logged in, you will be given a several different operations that you can request the server to do. If you already had an account 
and messages were sent to you when you were logged out, they will be instantly printed for you when you logged in the order in which they were 
recieved. At this point, you can list all or a subset of accounts, send a message to another user, log out, or delete your account by entering 
'l', 's', 'o', or 'd', respectively. Each of these operations are detailed below:

'l': list all accounts: You will be prompted for an optional parameter which allows you to enter in a specific username or some characters and a 
wildcard ('\*') to filter down results. If nothing or '\*' is entered as this parameter, a list of all users will be displayed. If a specific username is 
entered, any user that exists within the database will be displayed. If a combination of characters and a wildcard is entered, all names which have 
the same characters in the same positions preceding and following the wildcard will be returned. In other words, the '\*' character signifies any
number of arbitrary characters.

's': send a message: You will be prompted for the username of the user you want to send a message to. You can only send a message to one user at 
a time, and cannot send a message to yourself. If a username that exists within the database is entered, then you will be prompted for the message 
you wish to send. If that user is logged out, the message will be stored in their message queue, otherwise it will be delivered to them immediately.

'o': log out: You will be logged out and returned to the login screen.

'd': delete account: You will be asked to confirm that you wish to delete your account, as deleted accounts cannot be recovered. Enter 'y' for yes 
and 'n' for no. If 'n', you will be returned to the operations menu. If 'y', your account will be removed from the database and you will be 
returned to the login screen. 

-----------------------------------------------------------------------------------------------------------------------------------------------
4. Operation - Unit Tests

The unit tests for the custom wire protocol and gRPC applications can be found in test_helpers.py and test_helpers_gRPC.py. To run the tests in 
test_helpers.py, in the terminal run:

    python -m unittest test_helpers.py

And to run the tests in test_helpers_gRPC.py, run:

    python -m unittest test_helpers_gRPC.py


