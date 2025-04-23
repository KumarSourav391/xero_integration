from flask import Blueprint, redirect, request, jsonify
from services.xero_service import get_authorization_url, exchange_code_for_token, fetch_clients_from_xero

xero_bp = Blueprint("xero", __name__)

@xero_bp.route("/xero/auth/initiate")
def initiate_auth():
    return redirect(get_authorization_url())

@xero_bp.route("/xero/auth/callback")
def auth_callback():
    code = request.args.get("code")
    exchange_code_for_token(code)
    return "Authentication successful! You can now fetch client data."

@xero_bp.route("/xero/fetch/clients")
def fetch_clients():
    return jsonify(fetch_clients_from_xero())