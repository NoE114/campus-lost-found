import os

class Config:
    SECRET_KEY = "change-me"
    JWT_SECRET_KEY = "change-me-too"

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024