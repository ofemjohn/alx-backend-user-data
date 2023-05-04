#!/usr/bin/env python3
"""
Defines views for User API
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """Fetches all users"""
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str = None) -> str:
    """Fetches a user by ID"""
    if user_id == "me":
        if not request.current_user:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())

    if user_id is None:
        abort(404)

    user = User.get(user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """Deletes a user by ID"""
    if user_id is None:
        abort(404)

    user = User.get(user_id)

    if user is None:
        abort(404)

    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """Creates a new user"""
    error_msg = None
    try:
        request_json = request.get_json()
    except Exception:
        request_json = None

    if request_json is None:
        error_msg = "Invalid JSON"

    if error_msg is None and request_json.get("email", "") == "":
        error_msg = "Missing email"

    if error_msg is None and request_json.get("password", "") == "":
        error_msg = "Missing password"

    if error_msg is None:
        try:
            user = User()
            user.email = request_json.get("email")
            user.password = request_json.get("password")
            user.first_name = request_json.get("first_name")
            user.last_name = request_json.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = f"Could not create user: {e}"

    return jsonify({"error": error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """Updates an existing user"""
    if user_id is None:
        abort(404)

    user = User.get(user_id)

    if user is None:
        abort(404)

    try:
        request_json = request.get_json()
    except Exception:
        request_json = None

    if request_json is None:
        return jsonify({'error': "Invalid JSON"}), 400

    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')

    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200
