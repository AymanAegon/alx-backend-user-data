#!/usr/bin/env python3
"""
The Basic auth module
"""
from api.v1.auth.auth import Auth
import base64


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
