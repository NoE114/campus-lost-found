from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    pw = generate_password_hash(data['password'])
    new_user = User(name=data['name'], email=data['email'], password=pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token}), 200
    return jsonify({"msg": "Bad email or password"}), 401