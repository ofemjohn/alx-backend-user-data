#!/usr/bin/env python3
"""
This module defines the routes for the API.
"""

from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """Handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Handler for 401 errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """Handler for 403 errors."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """Handler for requests before they are processed.
    Validates requests and checks for authentication."""
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
