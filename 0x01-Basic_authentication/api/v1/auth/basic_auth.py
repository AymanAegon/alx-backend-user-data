#!/usr/bin/env python3
"""
The Basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """returns the Base64 part of the
        Authorization header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header[0:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):  # type: ignore
        """returns the user email and pwd from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        s = decoded_base64_authorization_header
        return tuple([s.split(':')[0], ':'.join(s.split(':')[1:])])

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):  # type: ignore
        """returns the User instance based on his email and password"""
        if type(user_email) != str or type(user_pwd) != str:
            return None
        user_list = User.search({'email': user_email})
        if len(user_list) == 0:
            return None
        if not user_list[0].is_valid_password(user_pwd):
            return None
        return user_list[0]

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """overloads Auth and retrieves the User instance for a request"""
        authorization_header = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(authorization_header)
        decoded = self.decode_base64_authorization_header(b64)
        user_cred = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(user_cred[0], user_cred[1])
        return user
