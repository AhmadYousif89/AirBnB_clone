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


class TestBaseModel(unittest.TestCase):
    """Testing the BaseModel"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls._cls = "BaseModel"
        cls.file = "hbnb.json"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.file):
            os.remove(cls.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self._cls}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self._cls}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self._cls} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self._cls} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self._cls} {obj.id} name \"x\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_extra_attrs(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self._cls} {obj.id} age \"20\" name \"x\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self._cls} {obj.id} {{\"email\": \"x@g.c\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "x@g.c")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self._cls}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self._cls} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self._cls} {obj.id} ''")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self._cls} {obj.id} name")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self._cls}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self._cls]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self._cls} {obj.id}")
        self.assertNotIn(f"{self._cls}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self._cls}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self._cls} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestBaseModelDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls._cls = "BaseModel"
        cls.file = "hbnb.json"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.file):
            os.remove(cls.file)

    def test_invalid_method(self):
        """Test invalid method output message"""
        method_name = "invalid_method_name"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.{method_name}()")
            )
        output = mock_stdout.getvalue().strip()
        self.assertEqual(
            output, f'{error_messages["no_method"]}: {method_name} **'
        )

    def test_create(self):
        """Test the create method using the <class>.<method>() formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.create()"))
        output = mock_stdout.getvalue().strip()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self._cls}.{output}", storage.all().keys())

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd("base.create()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.show({obj.id})")
            )
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd("base.show()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.show()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.show(123)"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self._cls}.update({obj.id}, name \"x\")"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_extra_attrs(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self._cls}.update({obj.id}, age \"20\", name \"x\")"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("age", obj.__dict__.keys())
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")
        self.assertEqual(obj.__dict__["name"], "x")

    def test_update_with_dict(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self._cls}.update({obj.id}, {{\"email\": \"x@g.c\"}})"
            self.console.onecmd(self.console.precmd(cmd))
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "x@g.c")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"base.update()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.update()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.update(123, age 20)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.update({obj.id}, '')")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.update({obj.id}, age)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.count()"))
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self._cls]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self._cls]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.destroy({obj.id})")
            )
        self.assertNotIn(f"{self._cls}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"base.destroy()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(self.console.precmd(f"{self._cls}.destroy()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(
                self.console.precmd(f"{self._cls}.destroy(123)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
