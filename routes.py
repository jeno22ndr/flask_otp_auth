from flask import Blueprint, request, jsonify, current_app
from models import db, User, OTP
from utils import generate_otp, send_mock_email, generate_jwt_token
from datetime import datetime, timedelta
import re

api_bp = Blueprint('api', __name__)

@api_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required."}), 400

    # Validate email format 
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400

    # Check for duplicate email 
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered."}), 409

    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful. Please verify your email."}), 201 # 

@api_bp.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # Return a generic message to prevent user enumeration
        return jsonify({"message": "If this email is registered, an OTP has been sent."}), 200

    # Implement basic rate limiting (e.g., allow OTP request every 60 seconds) 
    last_otp = OTP.query.filter_by(user_id=user.id).order_by(OTP.created_at.desc()).first()
    if last_otp and (datetime.utcnow() - last_otp.created_at).total_seconds() < 60:
        return jsonify({"message": "Please wait before requesting another OTP."}), 429 # Too Many Requests

    otp_code = generate_otp() # 
    expires_at = datetime.utcnow() + timedelta(minutes=current_app.config['OTP_EXPIRY_MINUTES']) # 

    new_otp = OTP(user_id=user.id, otp_code=otp_code, expires_at=expires_at)
    db.session.add(new_otp)
    db.session.commit()

    send_mock_email(email, otp_code) # 

    return jsonify({"message": "OTP sent to your email."}), 200 # 

@api_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp_input = data.get('otp')

    if not email or not otp_input:
        return jsonify({"message": "Email and OTP are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid email or OTP."}), 401

    # Get the latest, unused OTP for the user 
    otp_record = OTP.query.filter_by(user_id=user.id, otp_code=otp_input, is_used=False)\
                         .order_by(OTP.created_at.desc()).first()

    if not otp_record or otp_record.is_expired(): # 
        return jsonify({"message": "Invalid or expired OTP."}), 401

    # Mark OTP as used 
    otp_record.is_used = True
    db.session.commit()

    # Generate JWT token [cite: 20, 21, 31]
    token = generate_jwt_token(user.id, user.email)

    return jsonify({"message": "Login successful.", "token": token}), 200 #