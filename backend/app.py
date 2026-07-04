import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from models.user import User
from models.lost_item import LostItem
from models.found_item import FoundItem
from routes.auth import auth_bp
from routes.lost import lost_bp

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(lost_bp, url_prefix='/lost')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() in ["true", "1"]
    app.run(debug=debug_mode)