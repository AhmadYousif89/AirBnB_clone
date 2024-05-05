#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand, error_messages
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review,
}


class TestConsoleExitOp(unittest.TestCase):
    """Testing the exit methods of the console."""

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("quit")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("EOF")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


if __name__ == "__main__":
    unittest.main()
