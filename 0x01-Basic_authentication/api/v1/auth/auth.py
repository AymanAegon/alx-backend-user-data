#!/usr/bin/env python3
"""
The auth module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returs False"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns None"""
        return None
