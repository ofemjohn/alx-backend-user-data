#!/usr/bin/env python3

"""
This module defines the User and UserSession classes.
"""

import hashlib
from models.base import Base


class User(Base):
    """
    Represents a user in the system.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """
        Gets the encrypted password of the user.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """
        Sets a new password for the user and encrypts it using SHA256.
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """
        Validates a given password against the user's password.
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """
        Returns the user's display name based on email/first_name/last_name.
        """
        if self.email is None and self.first_name\
                is None and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)


class UserSession(Base):
    """
    Represents a user session in the system.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
