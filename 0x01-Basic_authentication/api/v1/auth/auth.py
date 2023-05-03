#!/usr/bin/env python3
''' Module for API Authentication '''

from typing import List, TypeVar
from flask import request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Auth:
    ''' Class to manage API authentication '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        Method for validating if endpoint requires authentication.

        :param path: Endpoint path.
        :type path: str
        :param excluded_paths: List of excluded endpoint paths.
        :type excluded_paths: List[str]
        :return: True if endpoint requires authentication, False otherwise.
        :rtype: bool
        '''
        # Validate input
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Check if endpoint path ends with a slash
        slash_path = True if path[-1] == '/' else False

        # Append slash to endpoint path if it doesn't end with one
        tmp_path = path if slash_path else path + '/'

        # Check if endpoint path is excluded
        for exc in excluded_paths:
            # Check if excluded path ends with a wildcard
            if exc[-1] == '*':
                # Check if endpoint path matches excluded path without wildcard
                if exc[:-1] == path[:len(exc)-1]:
                    return False
            else:
                # Check if endpoint path matches excluded path exactly
                if tmp_path == exc:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
        Method that handles authorization header.

        :param request: Flask request object.
        :type request: flask.request
        :return: Authorization header value.
        :rtype: str
        '''
        # Validate input
        if request is None:
            logger.error("Request object is None.")
            return None

        # Get Authorization header value
        auth_header = request.headers.get("Authorization", None)

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Validates current user.

        :param request: Flask request object.
        :type request: flask.request
        :return: Current user.
        :rtype: TypeVar('User')
        '''
        # Validate input
        if request is None:
            logger.error("Request object is None.")
            return None

        # TODO: Implement current_user method

        return None