from app import app
from models import db, User, LostItem

with app.app_context():
    user = User.query.first()

    if user:
        print(f"User: {user.name}")
        print(user.lost_items)

        item = LostItem.query.filter_by(user_id=user.id).first()

        if item:
            print(item.item_name)
            print(item.user.name)
    else:
        print("No users found.")