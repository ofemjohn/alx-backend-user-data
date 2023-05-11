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


@app.route('/reset_password', methods=['POST'])
def reset_password_token() -> str:
    '''
    Handle the POST /reset_password route.
    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond
    with a 200 HTTP status and JSON payload.
    '''
    try:
        email = request.form.get('email')
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
