# auth.py
# ---------------------------
# Handles user registration & login
# ---------------------------

from flask import jsonify
from flask_jwt_extended import create_access_token
from database import get_db


def register_user(email: str, password: str):
    """
    Register a new user. Returns JSON and status code:
      201 — success
      409 — user already exists
    """
    conn = get_db()
    cur  = conn.cursor()

    # check if email already exists
    if cur.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
        return jsonify({"message": "User already exists"}), 409

    # insert new user
    cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    return jsonify({"message": "User registered successfully"}), 201


def login_user(email: str, password: str):
    """
    Verify credentials and return a JWT token.
      200 — success (returns {"access_token": ...})
      401 — invalid credentials
    """
    conn = get_db()
    cur  = conn.cursor()

    row = cur.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    ).fetchone()

    if not row:
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=email)
    return jsonify({"access_token": token}), 200
