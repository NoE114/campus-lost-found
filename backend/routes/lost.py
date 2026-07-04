from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, LostItem

lost_bp = Blueprint('lost', __name__)

@lost_bp.route('/', methods=['POST'])
@jwt_required()
def add_item():
    data = request.json
    uid = get_jwt_identity()
    new_item = LostItem(user_id=uid, item_name=data['item_name'], category=data['category'], location=data['location'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"msg": "Item reported"}), 201

@lost_bp.route('/', methods=['GET'])
def get_items():
    category = request.args.get('category')
    query = LostItem.query
    if category:
        query = query.filter_by(category=category)
    return jsonify([i.to_dict() for i in query.all()])