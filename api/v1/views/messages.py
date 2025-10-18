#!/usr/bin/python3
"""Messages endpoints for API v1"""

from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger.utils import swag_from
from . import app_views
from models import storage
from models.messages import Message

FORBIDDEN_WORDS = {"badword1", "badword2"}
VALID_SENDERS = {"user", "system"}


def contains_forbidden(text: str) -> bool:
    """Check if text contains forbidden words."""
    t = (text or "").lower()
    return any(w in t for w in FORBIDDEN_WORDS)


# -------------------- CREATE MESSAGE --------------------
@app_views.route('/messages', methods=['POST'], strict_slashes=False)
@jwt_required()
@swag_from('documentation/messages/post_messages.yml')
def create_message():
    """Create a new message with validation and metadata."""
    data = request.get_json(force=True)
    session_id = data.get("session_id")
    content = data.get("content")
    sender = data.get("sender", "user")

    if not session_id or not content:
        return jsonify({
            "status": "error",
            "error": {"code": "MISSING_FIELDS", "message": "Missing session_id or content"}
        }), 400

    if len(content) > 512:
        return jsonify({
            "status": "error",
            "error": {"code": "CONTENT_TOO_LONG", "message": "Content exceeds 512 characters"}
        }), 400

    if sender not in VALID_SENDERS:
        return jsonify({
            "status": "error",
            "error": {"code": "INVALID_SENDER", "message": "Sender must be 'user' or 'system'"}
        }), 400

    if contains_forbidden(content):
        return jsonify({
            "status": "error",
            "error": {"code": "FORBIDDEN_CONTENT", "message": "Message contains forbidden words"}
        }), 400

    try:
        timestamp = datetime.fromisoformat(data.get("timestamp", "").replace("Z", "+00:00")) \
            if data.get("timestamp") else datetime.utcnow()
    except Exception:
        return jsonify({
            "status": "error",
            "error": {"code": "INVALID_TIMESTAMP", "message": "Invalid timestamp format"}
        }), 400

    current_user_id = get_jwt_identity()
    msg = Message(session_id=session_id, user_id=current_user_id, content=content, timestamp=timestamp)

    storage.new(msg)
    storage.save()

    metadata = {
        "word_count": len(content.split()),
        "character_count": len(content),
        "processed_at": datetime.utcnow().isoformat() + "Z"
    }

    response = msg.to_dict()
    response["metadata"] = metadata

    return jsonify({"status": "success", "data": response}), 201


# -------------------- GET MESSAGES --------------------
@app_views.route('/messages', methods=['GET'], strict_slashes=False)
@jwt_required()
@swag_from('documentation/messages/get_messages.yml')
def get_messages():
    """Retrieve messages filtered by session_id and/or user_id with pagination."""
    session_id = request.args.get("session_id")
    user_id = request.args.get("user_id")
    try:
        limit = min(int(request.args.get("limit", 100)), 100)
        offset = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        return jsonify({
            "status": "error",
            "error": {"code": "INVALID_PAGINATION", "message": "Limit and offset must be integers"}
        }), 400

    query = storage.session.query(Message)
    if session_id:
        query = query.filter_by(session_id=session_id)
    if user_id:
        query = query.filter_by(user_id=user_id)

    messages = query.order_by(Message.timestamp).offset(offset).limit(limit).all()
    return jsonify({
        "status": "success",
        "data": [m.to_dict() for m in messages]
    }), 200


# -------------------- PUT MESSAGE --------------------
@app_views.route('/messages/<message_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@swag_from('documentation/messages/put_messages.yml')
def update_message(message_id):
    """Update an existing message."""
    msg = storage.session.query(Message).filter_by(id=message_id).first()
    if not msg:
        return jsonify({"status": "error", "error": {"code": "NOT_FOUND", "message": "Message not found"}}), 404

    data = request.get_json(force=True)
    content = data.get("content")
    if content:
        if contains_forbidden(content):
            return jsonify({"status": "error", "error": {"code": "FORBIDDEN_CONTENT", "message": "Message contains forbidden words"}}), 400
        msg.content = content

    storage.save()
    return jsonify({"status": "success", "data": msg.to_dict()}), 200


# -------------------- DELETE MESSAGE --------------------
@app_views.route('/messages/<message_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@swag_from('documentation/messages/delete_messages.yml')
def delete_message(message_id):
    """Delete a message by ID."""
    msg = storage.session.query(Message).filter_by(id=message_id).first()
    if not msg:
        return jsonify({"status": "error", "error": {"code": "NOT_FOUND", "message": "Message not found"}}), 404

    storage.delete(msg)
    storage.save()
    return jsonify({"status": "success", "message": "Message deleted"}), 200
