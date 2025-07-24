from flask import Flask
from models import db
from routes import api_bp # We'll define api_bp in routes.py
import config

app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app) # Initialize SQLAlchemy with the Flask app

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return "User Authentication API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables if they don't exist
    app.run(debug=True) # Run in debug mode for development