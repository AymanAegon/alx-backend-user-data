#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password,
     hashed with bcrypt.hashpw"""
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """takes an email string argument and
        returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_id=user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """takes a single session_id string argument and
        returns the corresponding User or None"""
        if type(session_id) != str:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """takes a single user_id integer argument and returns None
        updates the corresponding user’s session ID to None"""
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Finds the user corresponding to the email
        generate a UUID and update the user's reset_token database field.
        Return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token
