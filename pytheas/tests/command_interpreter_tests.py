from pytheas.command_interpreter import PytheasCommandInterpreter
from pytheas.errors import InvalidCommandException
from pytheas.sfdaemon import Pytheas

import unittest

class MockDaemon(object):
    
    def __init__(self):
        self.sleep_time = 0

class CommandInterpreterTests(unittest.TestCase):
    
    def setUp(self):
        self.mock_daemon = MockDaemon()
        self.pci = PytheasCommandInterpreter(self.mock_daemon)
    
    def test_validation(self):
        empty_set = '{}'
        wrong_set = '{"set":"nonexistent", "val":1}'
        wrong_val = '{"set":"sleep_time", "val":"wrong"}'

        self.assertRaises(InvalidCommandException, self.pci.interpret_command, empty_set)
        self.assertRaises(InvalidCommandException, self.pci.interpret_command, wrong_set)
        self.assertRaises(InvalidCommandException, self.pci.interpret_command, wrong_val)

if __name__ == "__main__":
    unittest.main()
