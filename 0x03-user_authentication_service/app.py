#!/usr/bin/env python3
'''A basic flask application'''
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    '''A simple route'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_users() -> str:
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'message': 'missing email or password'}), 400

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400

    return jsonify({'email': email, 'message': 'user created'})


@app.route('/sessions', methods=['POST'])
def login():
    '''creates a new session for the given user'''
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = make_response(
                jsonify({"email": email, "message": "logged in"}))
            response.set_cookie('session_id', session_id)
            return response
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''get user with the session id and delete'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    '''check user profile'''
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    '''reset password route'''
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(400)

    response = {
        "email": email,
        "message": "Password updated"
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
