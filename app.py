#!/usr/bin/env python3
"""Flask Application - Main entry point"""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from models import storage
from api.v1 import app_views
from os import environ

# --- Initialize Flask app ---
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'

# --- Register Blueprint ---
app.register_blueprint(app_views)

# --- Configure CORS ---
CORS(app, resources={r"/api/v1/*": {"origins": "*"}}, supports_credentials=True)

# --- Configure Swagger ---
app.config['SWAGGER'] = {'title': 'Chat RESTful API', 'uiversion': 3}
swagger = Swagger(app)

# --- Initialize JWT ---
jwt = JWTManager(app)

# --- Close DB session on teardown ---
@app.teardown_appcontext
def close_db(error):
    storage.close()

# --- Error handlers ---
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)

# --- Run the app ---
if __name__ == "__main__":
    host = environ.get('CHAT_API_HOST', '0.0.0.0')
    port = environ.get('CHAT_API_PORT', '5001')
    print(f" Server running at http://{host}:{port}")
    app.run(host=host, port=port, threaded=True, debug=True)
