from models import db
from models.user import User
from models.lost_item import LostItem
from models.found_item import FoundItem

db.init_app(app)

with app.app_context():
    db.create_all()