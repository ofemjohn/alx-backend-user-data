#!/usr/bin/env python3
"""Module containing Index views."""

from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Route to get API status.

    Returns:
        str: JSON representation of API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Route to get number of each object.

    Returns:
        str: JSON representation of number of each object.
    """
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """Route to abort with 401 Unauthorized status.

    Returns:
        str: Aborts with 401 status.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """Route to abort with 403 Forbidden status.

    Returns:
        str: Aborts with 403 status.
    """
    abort(403)
