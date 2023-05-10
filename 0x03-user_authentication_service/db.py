#!/usr/bin/env python3
'''
DB module for database connections.
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


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
    def _session(self) -> Session:
        '''
        Memoized session object
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        method that add user to thec
        database and returns a User object
        '''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        '''
        Returns the first row found in the users table
        as filtered by the method's input arguments.

        Raises:
        - NoResultFound: when no results are found
        - InvalidRequestError: when wrong query arguments are passed
        '''
        if not kwargs:
            columns = User.__table__.columns.keys()
            for key in columns.keys():
                if key not in columns:
                    raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        update user with given user_id,
        using the provided keyword arguments.
        '''
        try:
            #find the user with the given user_id
            user = self.find_user_by(id=user_id)
            #update the user with the updated user_id
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            raise ValueError