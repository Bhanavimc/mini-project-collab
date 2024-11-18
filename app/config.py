# app/config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Database file in the current directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
