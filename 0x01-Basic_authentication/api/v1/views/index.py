#!/usr/bin/env python3
'''Module containing Index views for API v1.'''

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_api_status() -> str:
    '''
    GET /api/v1/status
    Returns:
        - JSON object containing the status of the API
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def get_api_stats() -> str:
    '''
    GET /api/v1/stats
    Returns:
        - JSON object containing the number of each object in the API
    '''
    from models.user import User
    stats_view = {}
    stats_view['users'] = User.count()
    return jsonify(stats_view)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    '''GET /api/v1/unauthorized
    Raises:
        - 401 error using Flask's abort function
    '''
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    '''
    GET /api/v1/forbidden
    Raises:
        - 403 error using Flask's abort function
    '''
    abort(403)
