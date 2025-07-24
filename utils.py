import random
import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_otp():
    """Generates a 6-digit numeric OTP."""
    return str(random.randint(100000, 999999)) # 

def send_mock_email(to_email, otp_code):
    """Mocks sending an email by printing to console."""
    print(f"--- MOCK EMAIL ---")
    print(f"To: {to_email}")
    print(f"Subject: Your OTP for login")
    print(f"OTP: {otp_code}") # 
    print(f"------------------")

def generate_jwt_token(user_id, email):
    """Generates a JWT token for the user."""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1) # Token expires in 1 hour 
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256') # 

def decode_jwt_token(token):
    """Decodes a JWT token."""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None # Token has expired
    except jwt.InvalidTokenError:
        return None # Invalid token