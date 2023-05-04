#!/usr/bin/env python3

"""
Authentication Views
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Logs in a user via session authentication.
    POST /auth_session/login

    Returns:
      - Response containing a user JSON representation if login was successful
      - Response containing an error message if login failed
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not user_email:
        return jsonify(error="email missing"), 400
    if not user_pwd:
        return jsonify(error="password missing"), 400
    try:
        user = User.search({"email": user_email})
    except Exception:
        return jsonify(error="no user found for this email"), 404
    if not user:
        return jsonify(error="no user found for this email"), 404
    for u in user:
        if u.is_valid_password(user_pwd):
            user_id = u.id
            from api.v1.app import auth
            session_id = auth.create_session(user_id)
            response = jsonify(u.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
    return jsonify(error="wrong password"), 401


@app_views.route('/auth_session/logout', methods=['DELETE'])
def logout() -> str:
    """Logs out a user via session authentication.
    DELETE /auth_session/logout

    Returns:
      - Empty Response with status code 200 if logout was successful
      - Aborts with status code 404 if logout failed
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
