#!/usr/bin/env python3
'''Basic Authentication'''

from typing import TypeVar
from base64 import b64decode
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    '''Authentication Class'''

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts Base64 Authorization Header

        :param authorization_header: Authorization header to extract from
        :type authorization_header: str
        :return: Base64 encoded string
        :rtype: str
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        encoded = authorization_header.split(' ', 1)[1]

        return encoded

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        '''
        Decodes the value of a base64 string

        :param base64_authorization_header: Base64 encoded string
        :type base64_authorization_header: str
        :return: Decoded string
        :rtype: str
        '''
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> str:
        '''
        Extracts user email and password from the Base64 decoded value

        :param decoded_base64_authorization_header: Decoded Base64 string
        :type decoded_base64_authorization_header: str
        :return: Tuple containing user email and password
        :rtype: tuple
        '''
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)

        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        Returns the User instance based on email and password

        :param user_email: User email
        :type user_email: str
        :param user_pwd: User password
        :type user_pwd: str
        :return: User instance
        :rtype: User
        '''
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Overloads Auth and retrieves the User instance for a request

        :param request: HTTP request
        :type request: Request
        :return: User instance
        :rtype: User
        '''
        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)

        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)

        return user