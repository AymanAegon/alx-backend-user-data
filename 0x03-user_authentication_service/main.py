#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)
print(user)

session_id = auth.create_session(email)
print(session_id)

auth.destroy_session(user.id)
print(user.session_id)

