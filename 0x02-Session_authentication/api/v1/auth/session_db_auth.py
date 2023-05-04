#!/usr/bin/env python3

"""
SessionDBAuth module - implements SessionExpAuth
and stores sessions in the database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class - extends SessionExpAuth
    and stores sessions in the database
    """

    def create_session(self, user_id=None) -> str:
        """
        Create a new session for a user and store it in the database
        :param user_id: the user ID for which to create a session
        :return: the session ID if successful, otherwise None
        """
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        new_user = UserSession(user_id=user_id, session_id=session_id)
        new_user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Get the user ID associated with a session from the database
        :param session_id: the session ID for which to get the user ID
        :return: the user ID if the session is
        valid and not expired, otherwise None
        """
        if not session_id:
            return None
        try:
            us_list = UserSession.search({session_id: session_id})
            for us in us_list:
                created_at = us.get('created_at', None)
                if not created_at:
                    return None
                if (datetime.now() > created_at +
                        timedelta(seconds=self.session_duration)):
                    return None
                return us.get('user_id', None)
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Destroy a session and remove it from the database
        :param request: the request object from which to get the session ID
        :return: True if successful, otherwise False
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if super().destroy_session(request):
            try:
                us_list = UserSession.search({session_id: session_id})
                for us in us_list:
                    us.remove()
                    return True
            except Exception:
                return False
        return False
