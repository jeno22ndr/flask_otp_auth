import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # SQLite database file 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_super_secret_key_here' # For JWT and session management 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another_secret_key_for_jwt'
    OTP_EXPIRY_MINUTES = 5 # OTP expiry time