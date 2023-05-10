#!/usr/bin/env python3
'''A basic flask application'''
from flask import Flask
from flask import jsonify


app = Flask(__name__)

app.route('/', methods=['GET'], strict_slashes=False)


def welcome() -> str:
    '''A simple route'''
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
