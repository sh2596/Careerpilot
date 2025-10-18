# backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-careerpilot')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/careerpilot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False