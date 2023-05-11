#!/usr/bin/env python3
'''A basic flask application'''
from flask import Flask, jsonify, request
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')
