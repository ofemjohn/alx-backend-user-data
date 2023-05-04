#!/usr/bin/env python3

"""
SessionAuth module
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class.
    """
    # Store user_id mapped to session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a given user ID.
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user ID associated with a given session ID.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current authenticated user based on the session ID in the
        request cookie.
        """
        if request:
            session_cookie = self.session_cookie(request)
            if session_cookie:
                user_id = self.user_id_for_session_id(session_cookie)
                return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Remove the session ID from the user ID map.
        """
        if not request:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        SessionAuth.user_id_by_session_id.pop(session_cookie, None)
        return True
