#!/usr/bin/env python3
"""Defines a Base class for all models in our AirBnB clone"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


# Timestamp format to be used across all objects
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Global dictionary to store all objects by class name and id
# Example: {'Base': {'42b7f46d-f1c5-44f1-a059-d0f0ee58fbf6': <Base object>}}
storage = {}


class Base:
    """Base class for all models in our AirBnB clone"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance"""

        # Store the name of the object's class
        class_name = str(self.__class__.__name__)

        # If the class is not yet in storage, add it with an empty dictionary
        if storage.get(class_name) is None:
            storage[class_name] = {}

        # Set the object's ID to a new UUID if not provided in kwargs
        self.id = kwargs.get('id', str(uuid.uuid4()))

        # Set the object's created_at datetime to the provided value or current
        # UTC time
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()

        # Set the object's updated_at datetime to the provided value or current
        # UTC time
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Checks if two Base objects are equal"""

        # Check if the other object is of the same type and is an instance of
        # the Base class
        if not isinstance(self, type(other)):
            return False
        if not isinstance(Base):
            return False

        # Check if the objects have the same ID
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Converts the object to a JSON dictionary"""

        # Initialize an empty dictionary for the object's attributes
        result = {}

        # Iterate over the object's attributes and add them to the dictionary
        for key, value in self.__dict__.items():

            # Skip attributes that are private (start with '_') if not
            # serializing for storage
            if not for_serialization and key[0] == '_':
                continue

            # Format datetime attributes as strings
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value

        return result

    @classmethod
    def load_from_file(cls):
        """Loads all objects from file"""

        # Get the name of the class
        class_name = cls.__name__

        # Set the storage dictionary for the class to an empty dictionary
        storage[class_name] = {}

        # Define the file path to load from based on the class name
        file_path = ".db_{}.json".format(class_name)

        # If the file does not exist, return
        if not path.exists(file_path):
            return

        # Otherwise, open the file and load the objects
        with open(file_path, 'r') as f:
            objs_json = json
