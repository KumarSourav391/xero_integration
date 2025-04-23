from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class XeroToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    tenant_id = db.Column(db.String, nullable=False)

class ClientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    xero_id = db.Column(db.String)