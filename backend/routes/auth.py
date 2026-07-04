from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    
    # Input validation
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
            
    name = data['name'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password cannot be empty"}), 400
        
    # Duplicate email handling
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400
        
    role = 'user'  # Hardcoded to prevent admin privilege escalation

    pw_hash = generate_password_hash(password)
    new_user = User(name=name, email=email, password=pw_hash, role=role)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred during registration"}), 500
        
    return jsonify({"msg": "Registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    
    # Input validation
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
        
    user = User.query.filter_by(email=email.strip().lower()).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token}), 200
        
    return jsonify({"error": "Bad email or password"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id_str = get_jwt_identity()
    try:
        user_id = int(user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid token identity"}), 401
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200