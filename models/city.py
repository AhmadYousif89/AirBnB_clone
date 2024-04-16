#!/usr/bin/python3
"""Define the City class module"""
from models.base_model import BaseModel


class City(BaseModel):
    """The City class with name and state_id"""

    name = ""
    state_id = ""  # it will be the State.id later
