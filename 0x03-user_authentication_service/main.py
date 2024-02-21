#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Registres a new user"""
    payload = {"email": email, "password": password}
    requests.post("http://0.0.0.0:5000/users", data=payload)


def log_in_wrong_password(email: str, password: str) -> None:
    """log_in_wrong_password"""
    payload = {"email": email, "password": password}
    requests.post("http://0.0.0.0:5000/sessions", data=payload)


def log_in(email: str, password: str) -> str:
    """log_in"""
    payload = {"email": email, "password": password}
    res = requests.post("http://0.0.0.0:5000/sessions", data=payload)
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """profile_unlogged"""
    requests.get("http://0.0.0.0:5000/profile")


def profile_logged(session_id: str) -> None:
    """profile_logged"""
    payload = {"session_id": session_id}
    requests.get("http://0.0.0.0:5000/profile", cookies=payload)


def log_out(session_id: str) -> None:
    """log_out"""
    payload = {"session_id": session_id}
    requests.delete("http://0.0.0.0:5000/sessions", cookies=payload)


def reset_password_token(email: str) -> str:
    """reset_password_token"""
    payload = {"email": email}
    res = requests.post("http://0.0.0.0:5000/reset_password", data=payload)
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update_password"""
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    requests.put("http://0.0.0.0:5000/reset_password", data=payload)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
