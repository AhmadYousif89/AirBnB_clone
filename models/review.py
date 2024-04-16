#!/usr/bin/python3
"""Define the Review class module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """The Review class"""

    place_id = ""  # it will be the Place.id later
    user_id = ""  # it will be the User.id later
    text = ""
