#!/usr/bin/env python3
from . import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"}), 200
