#!/usr/bin/python3
"""Users endpoints"""

from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_cors import cross_origin
from flasgger.utils import swag_from
from . import app_views
from models import storage
from models.user import User


# -------------------- GET all users --------------------
@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    all_users = storage.session.query(User).all()
    return jsonify([u.to_dict() for u in all_users]), 200


# -------------------- GET user by ID --------------------
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml')
def get_user(user_id):
    user = storage.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


# -------------------- DELETE user --------------------
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml')
def delete_user(user_id):
    user = storage.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


# -------------------- REGISTER user --------------------
@app_views.route('/users/register', methods=['POST'], strict_slashes=False)
@cross_origin()
def register_user():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON or Content-Type'}), 400

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not password:
        return jsonify({'error': 'missing data: email or password'}), 400

    # Verificar duplicados
    if storage.session.query(User).filter_by(email=email).first():
        return jsonify({'error': 'user already exists'}), 409

    # Crear nuevo usuario
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_user=True
    )
    user.set_password(password)

    try:
        storage.new(user)
        storage.save()
    except Exception as e:
        storage.session.rollback()
        return jsonify({'error': 'Database error', 'detail': str(e)}), 500

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'user created',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201


# -------------------- LOGIN --------------------
@app_views.route('/users/login', methods=['POST'], strict_slashes=False)
@cross_origin()
@swag_from('documentation/user/login_user.yml')
def login():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON or Content-Type'}), 400
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'missing data'}), 400

    user = storage.session.query(User).filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'user authenticated',
        'is_user': user.is_user,
        'access_token': access_token
    }), 200


# -------------------- LOGOUT --------------------
@app_views.route('/logout', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/logout.yml')
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


# -------------------- UPDATE user --------------------
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml')
def update_user(user_id):
    """Actualizar los datos de un usuario existente"""
    user = storage.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON or Content-Type'}), 400

    # Campos permitidos para actualizar
    allowed_fields = {'email', 'first_name', 'last_name', 'password'}

    for key, value in data.items():
        if key in allowed_fields:
            if key == 'password':
                user.set_password(value)
            else:
                setattr(user, key, value)

    try:
        storage.save()
    except Exception as e:
        storage.session.rollback()
        return jsonify({'error': 'Database error', 'detail': str(e)}), 500

    return jsonify({
        'message': 'user updated',
        'user': user.to_dict()
    }), 200
