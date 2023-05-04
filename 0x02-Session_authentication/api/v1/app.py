#!/usr/bin/env python3
"""
Main module for the API.
"""

# Importing necessary modules
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


# Creating a Flask instance and registering blueprints
app = Flask(__name__)
app.register_blueprint(app_views)

# Configuring CORS for the API endpoints
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configuring authentication type based on environment variable
auth = None
if os.getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif os.getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()
elif os.getenv("AUTH_TYPE") == "session_exp_auth":
    auth = SessionExpAuth()
elif os.getenv("AUTH_TYPE") == "session_db_auth":
    auth = SessionDBAuth()
elif os.getenv("AUTH_TYPE") == "auth":
    auth = Auth()

# Error handlers
@app.errorhandler(404)
def not_found(error) -> str:
    """ Handler for not found errors.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Handler for unauthorized errors.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Handler for forbidden errors.
    """
    return jsonify({"error": "Forbidden"}), 403

# Before request handler
@app.before_request
def before():
    """ Handler for processing requests before they are executed.
    """
    if auth:
        # Paths that do not require authentication
        paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/',
                 '/api/v1/auth_session/login/']
        # Skipping authentication for unsecured paths
        if not auth.require_auth(request.path, paths):
            return
        # Authenticating requests
        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            abort(401)
        request.current_user = auth.current_user(request)
        if not request.current_user:
            abort(403)

# Main function
if __name__ == "__main__":
    # Running the app
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
