from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password_hash = db.Column(db.String(128)) # Optional, depending on if you'd ever use password login
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    otps = db.relationship('OTP', backref='user', lazy=True) # Relationship to OTPs

    def __repr__(self):
        return f'<User {self.email}>'

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False) # Assuming 6-digit OTP
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f'<OTP {self.otp_code} for user {self.user_id}>'