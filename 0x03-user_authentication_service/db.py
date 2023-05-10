#!/usr/bin/env python3
'''
DB module for database connections.
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User

from user import Base


class DB:
    '''
    DB class for sqlalchemy database connections.
    '''

    def __init__(self):
        '''
        Initialize a new DB instance
        '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        '''
        Memoized session object
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        method that add user to the
        database and returns a User object
        '''
        user = User(email=email, hashed_password=hashed_password)
        session = self.__session.add(user)
        session.commit()
        return user
