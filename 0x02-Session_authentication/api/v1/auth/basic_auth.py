#!/usr/bin/env python3

"""
Basic auth class that extends Auth class.
"""

import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that extends Auth class.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts Base64 Authorization header.
        """
        if not authorization_header or not isinstance(
                authorization_header,
                str) or not authorization_header.startswith("Basic "):
            return
        return "".join(authorization_header.split(" ")[1:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes Base64 Authorization header.
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return
        try:
            b64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(b64_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> str:
        """
        Extracts user credentials from Base64 Authorization header.
        """
        if not decoded_base64_authorization_header or not isinstance(
                decoded_base64_authorization_header,
                str) or ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, pwd = decoded_base64_authorization_header.split(':')
        return (email, pwd)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Retrieves User object from email and password.
        """
        if not user_email or not isinstance(
                user_email,
                str) or not user_pwd or not isinstance(
                user_pwd,
                str):
            return
        user = None
        try:
            user = User.search({"email": user_email})
        except Exception:
            return
        if not user:
            return
        for u in user:
            if u.is_valid_password(user_pwd):
                return u

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns current User instance based on user credentials.
        """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(*user_creds)
