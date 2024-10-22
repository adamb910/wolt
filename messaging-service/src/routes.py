from flask import Blueprint, jsonify, request

from services import user_service, message_service

api = Blueprint('api', __name__)

@api.route('/')
def hello():
    return "hello", 200

# USER section
#TODO: Could use blueprints and seperate files for different routes

@api.route('/users', methods=["GET"])
def get_users():
    email = request.args.get('email')  # Get email from query parameter
    
    users = user_service.get_users(email_filter=email)

    if users:
        return jsonify([user.to_dict() for user in users]), 200
    
    return jsonify({"error": "No users found"}), 404

@api.route('/users/<id>', methods=["DELETE"])
def delete_user(id: str):
    try:
        user_service.delete_user(int(id))
    except Exception as e: #TODO: could catch specific exceptions to return specific http codes, eg bad request..
        print(e)
        return jsonify("An error occured while deleting user"), 500
    return "ok", 200

@api.route('/users', methods=["POST"])
def create_user():
    body = request.json
    user = user_service.create_user(body.get("name"), body.get("email"))
    return user.to_dict(), 200

@api.route('/users/<id>', methods=["PUT"])
def update_user(id: str):
    body = request.json
    user = user_service.update_user(int(id), body.get("name"), body.get("email"))
    return user.to_dict(), 200


# MESSAGE section

@api.route('/messages/<id>', methods=["DELETE"])
def delete_message(id: str):
    try:
        message_service.delete_message(int(id))
    except: #TODO: could catch specific exceptions to return specific http codes, eg bad request..
        return jsonify("An error occured while deleting message"), 500
    return "ok", 200

@api.route('/messages', methods=["POST"])
def create_message():
    body = request.json
    message = message_service.create_message(body.get("message"), body.get("sender"))
    return message.to_dict(), 200

@api.route('/messages', methods=["GET"])
def get_message():
    sender_id = request.args.get('sender')  #TODO: Get sender from query parameter. Here we are just using the ID, we could use the email in the API and fetch the ID to make it more elegant
    messages = message_service.get_messages_from_user(int(sender_id))
    return [message.to_dict() for message in messages], 200
