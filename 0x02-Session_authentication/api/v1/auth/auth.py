#!/usr/bin/env python3
""" Auth module.
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """ Auth class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of
            paths that do not require authentication.

        Returns:
            bool: True if the path requires
            authentication, False otherwise.
        """
        if not path or not excluded_paths:
            return True
        path = path + '/' if path[-1] != '/' else path
        has_wildcard = any(x.endswith("*") for x in excluded_paths)
        if not has_wildcard:
            return path not in excluded_paths
        for e in excluded_paths:
            if e.endswith("*"):
                if path.startswith(e[:-1]):
                    return False
            if path == e:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the Authorization header from a request.

        Args:
            request: The request to get the header from.

        Returns:
            str: The value of the Authorization header,
            or None if it is not present.
        """
        if request:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from a request.

        Args:
            request: The request to get the user from.

        Returns:
            User: The current user, or None if there is no authenticated user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Gets the session cookie from a request.

        Args:
            request: The request to get the session cookie from.

        Returns:
            str: The value of the session cookie, or None if it is not present.
        """
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookies.get(session_name, None)
