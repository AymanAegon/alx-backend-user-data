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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for e in excluded_paths:
            p = ''
            s = ''
            if path[-1] == '/' and e[-1] != '/':
                s = '/'
            if path[-1] != '/' and e[-1] == '/':
                p = '/'
            if path + p == e + s:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns None"""
        return None
