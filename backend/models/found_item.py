from .db import db
from datetime import datetime

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {"id": self.id, "item_name": self.item_name, "category": self.category, "location": self.location, "image": self.image}
