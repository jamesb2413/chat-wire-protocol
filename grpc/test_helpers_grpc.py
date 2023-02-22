import unittest
import helpers_grpc

# TO RUN THESE TESTS: python -m unittest test_helpers_grpc.py

class TestgRPCHelpers(unittest.TestCase):

    def test_isValidUsername(self):
        # get username of a client
        self.assertEqual(helpers_grpc.isValidUsername("test1"), True)
        # client does not enter valid username
        self.assertEqual(helpers_grpc.isValidUsername(""), False)

    def test_addUser(self):
        test_dict = {"test1" : [True, []], "test2" : [True, []]}
        # add user to dictionary
        self.assertEqual(helpers_grpc.addUser("test3", test_dict), (False, ""))
        # ensure same user cannot be added twice
        self.assertEqual(helpers_grpc.addUser("test1", test_dict), (True, "This username is already taken by another account. Please " +
                      "try again with a different username.\n"))
    
    def test_signInExisting(self):
        test_dict = {"test1":[True, []], "test2":[False, []]}
        faulty_message_1 = "test1"
        faulty_message_2 = ""
        faulty_message_3 = "test3"
        good_message_1 = "test2"
        # login attempt to existing user, already logged in
        self.assertEqual(helpers_grpc.signInExisting(faulty_message_1, test_dict), (True, "This user is already logged in on another device. Please " +
                          "log out in the other location and try again.\n"))
        # login attempt to existing user, empty string
        self.assertEqual(helpers_grpc.signInExisting(faulty_message_2, test_dict), (True, "No users exist with this username. Please double check that you typed correctly " +
                      "or create a new account with this username.\n"))
        # login attempt to existing user, username does not exist 
        self.assertEqual(helpers_grpc.signInExisting(faulty_message_3, test_dict), (True, "No users exist with this username. Please double check that you typed correctly " +
                      "or create a new account with this username.\n"))
        # login attempt to existing user
        self.assertEqual(helpers_grpc.signInExisting(good_message_1, test_dict), (False, 'You have 0 unread messages:\n\n'))
    
    def test_sendMsg(self):
        test_dict = {"test1":[True, []], "test2":[True, []], "test3":[False, []]}
        # client attempts to send message to someone not in database
        self.assertEqual(helpers_grpc.sendMsg("test1", "test", "hello world", test_dict), "Error sending message to test: User does not exist\n")
        # message sent from one client to another logged in user
        self.assertEqual(helpers_grpc.sendMsg("test1", "test2", "hello world", test_dict), "Message sent.\n")
        # message sent from one client to another logged out user
        self.assertEqual(helpers_grpc.sendMsg("test1", "test3", "hello world", test_dict), "Message sent.\n")
    
    # test_dict = {"test1":[True, []], "test2":[True, []], "test3":[True, []], "test4":[True, []], "foo":[True, []]}
    #     good_message_1 = ["L", ""]
    #     good_message_2 = ["L", "t*"]
    #     good_message_3 = ["L", "test3"]
    #     good_message_4 = ["L", "*"]
    #     bad_message_1 = ["L", "*st1"]
    #     # user enters nothing after list command
    #     self.assertEqual(helpers_grpc.sendUserlist(good_message_1, 1, test_dict), ["test1", "test2", "test3", "test4", "foo"])
    #     # user uses wildcard and characters
    #     self.assertEqual(helpers_grpc.sendUserlist(good_message_2, 1, test_dict), ["test1", "test2", "test3", "test4"])
    #     # user specifies specific user
    #     self.assertEqual(helpers_grpc.sendUserlist(good_message_3, 1, test_dict), ["test3"])
    #     # user uses wildcard only
    #     self.assertEqual(helpers_grpc.sendUserlist(good_message_4, 1, test_dict), ["test1", "test2", "test3", "test4", "foo"])
    #     # user uses wildcard only
    #     self.assertEqual(helpers_grpc.sendUserlist(bad_message_1, 1, test_dict), -1)