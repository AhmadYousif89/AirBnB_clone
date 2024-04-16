#!/usr/bin/python3
"""Define the Place class module"""
from models.base_model import BaseModel


class Place(BaseModel):
    """The Place class"""

    city_id = ""  # it will be the City.id later
    user_id = ""  # it will be the User.id later
    name = ""
    description = ""
    number_rooms = 0  # integer - 0
    number_bathrooms = 0  # integer - 0
    max_guest = 0  # integer - 0
    price_by_night = 0  # integer - 0
    latitude = 0.0  # float - 0.0
    longitude = 0.0  # float - 0.0
    amenity_ids = []  # it will be the list of Amenity.id later
