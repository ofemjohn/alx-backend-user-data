#!/usr/bin/env python3

""" UserSession module.

This module defines the UserSession class, which represents a user's session.

Classes:
    UserSession: A class representing a user's session.

"""

from models.base import Base


class UserSession(Base):
    """ A class representing a user's session.

    Attributes:
        id (str): The ID of the user session.
        created_at (datetime.datetime): The date and
        time the user session was created.
        updated_at (datetime.datetime): The date and
        time the user session was last updated.
        user_id (str): The ID of the user
        associated with the session.
        session_id (str): The ID of the session.

    Methods:
        __init__(*args: list, **kwargs: dict):
        Initializes a UserSession instance.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initializes a UserSession instance.

        Args:
            *args (list): List of arguments.
            **kwargs (dict): Dictionary of keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
