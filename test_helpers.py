import unittest
import helpers

# TO RUN THESE TESTS: python -m unittest test_helpers.py

class TestServer(unittest.TestCase):

    def test_getClientUsername(self):
        # get username of a client
        self.assertEqual(helpers.ServerHelpers.getClientUsername(1, {"test1": [1, True, []]}), "test1")

    def test_enqueueMsg(self):
        # add message to user's queue
        self.assertEqual(helpers.ServerHelpers.enqueueMsg("test message appended", "test1", {"test1": [1, True, ["wrong", "wrong", "wrong"]]}), "test message appended")
    
    def test_addUser(self):
        test_dict = {}
        # add user to dictionary
        self.assertEqual(helpers.ServerHelpers.addUser("test1", 1, test_dict), [1, True, []])
        # ensure same user cannot be added twice
        self.assertEqual(helpers.ServerHelpers.addUser("test1", 1, test_dict), -1)
    
    def test_signIn(self):
        test_dict = {"test1":[1, True, []], "test2":[2, False, []]}
        faulty_message_1 = ["I", "Existing"]
        faulty_message_2 = ["I", "Existing", "test1", " "]
        faulty_message_3 = ["I", "Existing", "test1"]
        faulty_message_4 = ["I", "Existing", "test"]
        faulty_message_5 = ["I", "New", "test1"]
        good_message_1 = ["I", "Existing", "test2"]
        good_message_2 = ["I", "New", "test3"]
        # login attempt to existing user, no username provided
        self.assertEqual(helpers.ServerHelpers.signIn(faulty_message_1, 1, test_dict), -1)
        # login attempt to existing user, username is too long
        self.assertEqual(helpers.ServerHelpers.signIn(faulty_message_2, 1, test_dict), -2)
        # login attempt to existing user, user already logged in
        self.assertEqual(helpers.ServerHelpers.signIn(faulty_message_3, 1, test_dict), -3)
        # login attempt to existing user, username dne
        self.assertEqual(helpers.ServerHelpers.signIn(faulty_message_4, 1, test_dict), -4)
        # login attempt to new user, existing username provided
        self.assertEqual(helpers.ServerHelpers.signIn(faulty_message_5, 1, test_dict), -5)
        # login attempt to existing user
        self.assertEqual(helpers.ServerHelpers.signIn(good_message_1, 2, test_dict), 1)
        # login attempt to new user
        self.assertEqual(helpers.ServerHelpers.signIn(good_message_2, 3, test_dict), 1)

    def test_sendMsg(self):
        test_dict = {"test1":[1, True, []], "test2":[2, True, []]}
        faulty_message_1 = ["S", "test1"]
        faulty_message_2 = ["S", "test3"]
        good_message_1 = ["S", "test2", "hello", "world"]
        # client attempts to send message to themselves
        self.assertEqual(helpers.ServerHelpers.sendMsg(faulty_message_1, 1, test_dict), -1)
        # client attempts to send message to someone who isnt in database
        self.assertEqual(helpers.ServerHelpers.sendMsg(faulty_message_2, 1, test_dict), -2)
        # message sent from one client to another
        self.assertEqual(helpers.ServerHelpers.sendMsg(good_message_1, 1, test_dict), 1)

    def test_sendUserlist(self):
        test_dict = {"test1":[1, True, []], "test2":[2, True, []], "test3":[3, True, []], "test4":[4, True, []], "foo":[4, True, []]}
        good_message_1 = ["L", ""]
        good_message_2 = ["L", "t*"]
        good_message_3 = ["L", "test3"]
        good_message_4 = ["L", "*"]
        # user enters nothing after list command
        self.assertEqual(helpers.ServerHelpers.sendUserlist(good_message_1, 1, test_dict), ["test1", "test2", "test3", "test4", "foo"])
        # user uses wildcard and characters
        self.assertEqual(helpers.ServerHelpers.sendUserlist(good_message_2, 1, test_dict), ["test1", "test2", "test3", "test4"])
        # user specifies specific user
        self.assertEqual(helpers.ServerHelpers.sendUserlist(good_message_3, 1, test_dict), ["test3"])
        # user uses wildcard only
        self.assertEqual(helpers.ServerHelpers.sendUserlist(good_message_4, 1, test_dict), ["test1", "test2", "test3", "test4", "foo"])

    def test_deleteAcct(self):
        test_dict = {"test1":[1, True, []], "test2":[2, True, []]}
        # delete user from database 
        self.assertEqual(helpers.ServerHelpers.deleteAcct(1, test_dict), "test1")
    
    def test_logOut(self):
        test_dict = {"test1":[1, True, []], "test2":[2, True, []]}
        # log user out 
        self.assertEqual(helpers.ServerHelpers.logOut(1, test_dict), "test1")
