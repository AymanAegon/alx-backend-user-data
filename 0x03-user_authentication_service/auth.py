#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed with bcrypt.hashpw"""
    return hashpw(password.encode("utf-8"), gensalt())
