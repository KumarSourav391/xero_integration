import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    XERO_BASE_URL = os.getenv("XERO_BASE_URL")
    XERO_AUTH_URL = os.getenv("XERO_AUTH_URL")
    XERO_TOKEN_URL = os.getenv("XERO_TOKEN_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")