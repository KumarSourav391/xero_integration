from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy

from models import db
from config import Config
from routes.xero_routes import xero_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")  # PostgreSQL URI
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(xero_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)