#!/usr/bin/env python3
""" Flask app Module """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user():
    """Creating new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "{}".format(email), "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """create a new session for the user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    res = jsonify({"email": email, "message": "logged in"})
    session_id = AUTH.create_session(email)
    res.set_cookie("session_id", session_id)
    return res


@app.route("/sessions", methods=["DELETE"])
def logout():
    """deletes a session of a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
