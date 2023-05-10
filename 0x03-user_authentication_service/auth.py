#!/usr/bin/env python3
'''auth route that handles authentications'''
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''method hashes password using bycrypt'''
    salted = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salted)
    return hashed_password


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