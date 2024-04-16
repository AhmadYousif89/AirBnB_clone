#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    The base class for all models in the application.

    Attributes:
    -   id (str): A unique identifier for the model instance.
    -   created_at (datetime): Timestamp representing the creation date.
    -   updated_at (datetime): Timestamp representing the last update date.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance. If keyword arguments are provided
        it populates the instance attributes with the values.
        If no arguments, it generates a new unique id and sets the
        created_at and updated_at timestamps,
        finally it save the instances in the storage file.

        Args:
        -   *args: Variable length argument list.
        -   **kwargs: Arbitrary keyword arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            del kwargs['__class__']
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """
        A string representation of the BaseModel instance.

        Returns:
        -   str: A string representation of the model instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the attribute (updated_at) timestamp and saves
        the class instance to the storage file.
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        A dictionary representation of the BaseModel instance.

        Returns:
        -   _dict: A dictionary representation of the model instance.
        """
        _dict = self.__dict__.copy()
        _dict["__class__"] = self.__class__.__name__
        _dict['created_at'] = _dict['created_at'].isoformat()
        _dict['updated_at'] = _dict['updated_at'].isoformat()
        return _dict
