#!/usr/bin/env python3
""" Module of SessionAuth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login """
    email = request.form.get("email")
    if email is None or len(email) == 0:
        return jsonify({ "error": "email missing" }), 400
    password = request.form.get("password")
    if password is None or len(password) == 0:
        return jsonify({ "error": "password missing" }), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie("_my_session_id", session_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """ DELETE /api/v1/auth_session/logout """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
