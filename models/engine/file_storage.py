#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os

HBNB_ENV = os.getenv("HBNB_ENV", "dev")
HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER", "dev")
HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD", "dev")
HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST", "dev")
HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB", "dev")
HBNB_TYPE_STORAGE = os.getenv("HBNB_TYPE_STORAGE", "dev")


class FileStorage:
    """
    Manage serialization and deserialization of class instances.

    Attributes:
    -   __file_path (str): The path to the Json file.
    -   __objects (dict): A dictionary containing every class instance.
    """

    __file_path = 'hbnb.json'
    __objects = {}

    def all(self):
        """
        Returns A dictionary containing all instances stored in __objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key "<className>.id"

        Args:
        -   obj (BaseModel): The object to be added.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.all()[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            _dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(_dict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel,
            'Amenity': Amenity,
            'Review': Review,
            'Place': Place,
            'State': State,
            'City': City,
            'User': User,
        }

        try:
            _dict = {}
            with open(FileStorage.__file_path) as f:
                _dict = json.load(f)
                for key, val in _dict.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
