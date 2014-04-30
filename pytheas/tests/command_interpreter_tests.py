from pytheas.command_interpreter import PytheasCommandInterpreter
from pytheas.errors import InvalidCommandException
from pytheas.sfdaemon import Pytheas

import unittest

def spam():
    return True

class CommandInterpreterTests(unittest.TestCase):
    
    def test_validation(self):
        empty_set = '{}'
        wrong_set = '{"set":"nonexistent", "val":1}'
        wrong_val = '{"set":"sleep_time", "val":"wrong"}'

        pci = PytheasCommandInterpreter(None)

        self.assertRaises(InvalidCommandException, pci.interpret_command, empty_set)
        self.assertRaises(InvalidCommandException, pci.interpret_command, wrong_set)
        self.assertRaises(InvalidCommandException, pci.interpret_command, wrong_val)

if __name__ == "__main__":
    unittest.main()
