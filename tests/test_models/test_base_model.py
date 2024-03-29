#!/usr/bin/python3
"""Testing the `base_model` module."""
import os
import time
import json
import uuid
import unittest
from datetime import datetime
from models import FileStorage
from models.base_model import BaseModel


class TestBase(unittest.TestCase):
    """Test cases for the `Base` class."""

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_initialization_positive(self):
        """Test passing cases `BaseModel` initialization."""
        b1 = BaseModel()
        uid = str(uuid.uuid4())
        b2 = BaseModel(id=uid, name="xxx", email="xxx@gmail.com")
        expected = "<class 'models.base_model.BaseModel'>"
        self.assertEqual(str(type(b1)), expected)
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b2.id, str)
        self.assertEqual(uid, b2.id)
        self.assertEqual(b2.email, "xxx@gmail.com")
        self.assertEqual(b2.name, "xxx")

    def test_dict(self):
        """Test method for dict"""
        b1 = BaseModel()
        uid = str(uuid.uuid4())
        b2 = BaseModel(id=uid, name="xxx", email="xxx@gmail.com")
        b1_dict = b1.to_dict()
        self.assertIsInstance(b1_dict, dict)
        self.assertIn('id', b1_dict.keys())
        self.assertIn('created_at', b1_dict.keys())
        self.assertIn('updated_at', b1_dict.keys())
        self.assertEqual(b1_dict['__class__'], type(b1).__name__)
        with self.assertRaises(KeyError) as e:
            b2.to_dict()

    def test_save(self):
        """Test method for save"""
        b = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        b.save()
        diff = b.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_save_no_args(self):
        """Tests save() with no arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_save_excess_args(self):
        """Tests save() with too many arguments."""
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_str(self):
        """Test method for str representation"""
        b1 = BaseModel()
        string = f"[{type(b1).__name__}] ({b1.id}) {b1.__dict__}"
        self.assertEqual(b1.__str__(), string)


if __name__ == "__main__":
    unittest.main()
