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


def _generate_uuid() -> str:
    '''
    Generate a new UUID and return
    it as a string representation.
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

    def create_session(self, email: str) -> str:
        '''
        Create a new session for the user corresponding to the provided email.
        Returns the session ID as a string.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
            Retrieve the User object corresponding to the provided session ID.
            Returns the User object if found, otherwise returns None.
        '''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
