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
        negative_val = '{"set":"sleep_time", "val":-1}'
        non_json = "sleep_time = 42"

        self.assertRaises(InvalidCommandException, self.pci.interpret_command, empty_set)
        self.assertRaises(InvalidCommandException, self.pci.interpret_command, wrong_set)
        self.assertRaises(InvalidCommandException, self.pci.interpret_command, wrong_val)
        self.assertRaises(InvalidCommandException, self.pci.interpret_command, negative_val)
        self.assertRaises(ValueError, self.pci.interpret_command, non_json)

    def test_daemon(self):
        self.assertEqual(self.mock_daemon.sleep_time, 0)

        command  = '{"set":"sleep_time", "val":1}'
        self.assertTrue(self.pci.interpret_command(command))
        self.assertEqual(self.mock_daemon.sleep_time, 1)

        float_command = '{"set":"sleep_time", "val":3.14}'
        self.assertTrue(self.pci.interpret_command(float_command))
        self.assertEqual(self.mock_daemon.sleep_time, 3.14)

        fractional_command = '{"set":"sleep_time", "val":0.42}'
        self.assertTrue(self.pci.interpret_command(fractional_command))
        self.assertEqual(self.mock_daemon.sleep_time, 0.42)

        # Like above but values are quoted
        qcommand = '{"set":"sleep_time", "val":"1"}'
        self.assertTrue(self.pci.interpret_command(qcommand))
        self.assertEqual(self.mock_daemon.sleep_time, 1)

        qfloat_command = '{"set":"sleep_time", "val":"3.14"}'
        self.assertTrue(self.pci.interpret_command(qfloat_command))
        self.assertEqual(self.mock_daemon.sleep_time, 3.14)

        qfractional_command = '{"set":"sleep_time", "val":".42"}'
        self.assertTrue(self.pci.interpret_command(qfractional_command))
        self.assertEqual(self.mock_daemon.sleep_time, 0.42)

if __name__ == "__main__":
    unittest.main()
