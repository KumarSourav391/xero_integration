import requests
from datetime import datetime, timedelta
from config import Config
from models import XeroToken, ClientData, db


def get_authorization_url():
    params = {
        "response_type": "code",
        "client_id": Config.CLIENT_ID,
        "redirect_uri": Config.REDIRECT_URI,
        "scope": "offline_access accounting.contacts.read",
        "state": "secure_random_state"
    }
    import urllib.parse
    return f"{Config.XERO_AUTH_URL}?" + urllib.parse.urlencode(params)


def exchange_code_for_token(code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.REDIRECT_URI,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET
    }
    response = requests.post(Config.XERO_TOKEN_URL, data=data).json()
    if "access_token" not in response:
        print("Error from Xero during token exchange:", response)
        raise Exception("Token exchange failed. Response: " + str(response))
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    expires_in = response["expires_in"]
    tenant_id = get_tenant_id(access_token)

    token = XeroToken(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=expires_in),
        tenant_id=tenant_id
    )
    db.session.add(token)
    db.session.commit()


def get_tenant_id(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.xero.com/connections", headers=headers).json()
    return response[0]["tenantId"]


def fetch_clients_from_xero():
    token = XeroToken.query.first()
    if not token:
        return {"error": "Not authenticated"}, 401

    if token.expires_at < datetime.utcnow():
        refresh_access_token(token)

    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "Xero-tenant-id": token.tenant_id,
        "Accept": "application/json"
    }
    response = requests.get(f"{Config.XERO_BASE_URL}/Contacts", headers=headers).json()
    for contact in response.get("Contacts", []):
        client = ClientData(
            name=contact.get("Name"),
            email=contact.get("EmailAddress"),
            xero_id=contact.get("ContactID")
        )
        db.session.add(client)
    db.session.commit()
    return {"message": "Clients imported successfully"}


def refresh_access_token(token):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token.refresh_token,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET
    }
    response = requests.post(Config.XERO_TOKEN_URL, data=data).json()
    token.access_token = response["access_token"]
    token.refresh_token = response["refresh_token"]
    token.expires_at = datetime.utcnow() + timedelta(seconds=response["expires_in"])
    db.session.commit()