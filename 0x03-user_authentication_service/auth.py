#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password,
     hashed with bcrypt.hashpw"""
    return hashpw(password.encode("utf-8"), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Takes mandatory email and password string
        arguments and return a User object"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
    
    def valid_login(self, email: str, password: str) -> bool:
        """It should expect email and password required
        arguments and return a boolean"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if checkpw(password.encode("utf-8"), user.hashed_password):
            return True
        return False
        
