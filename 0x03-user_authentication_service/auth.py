#!/usr/bin/env python3
'''auth route that handles authentications'''
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    '''method hashes password using bycrypt'''
    salted = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salted)
    return hashed_password


def _generate_uuid(self) -> str:
    '''
    Generate a new UUID and return it as a string representation.
    '''
    UUID = uuid.uuid4()
    return str(UUID)


class Auth:
    '''
    Auth class to interact with the authentication database.
    '''

    def __init__(self):
        '''instantiates the database'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register the user with the given email and password'''
        try:
            self._db.find_user_by(email=email)
            if User.email is not None:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        '''
        Check if the provided email and password are valid for login.
        Returns True if valid, False otherwise.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if user and bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        else:
            return False
