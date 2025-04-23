# 🧾 Xero Integration Backend

This project allows users to securely authenticate and fetch client data from Xero accounting software using OAuth 2.0.

## 🔧 Features
- OAuth 2.0 based Xero login
- Secure token handling and refresh
- Fetch and store client data
- RESTful API endpoints for frontend integration

## 🚀 Setup
1. **Clone the repo** and `cd` into the project.
2. Create a `.env` file using the provided format.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python app.py
   ```

## 📬 API Endpoints
| Method | Endpoint                 | Description                   |
|--------|--------------------------|-------------------------------|
| GET    | `/xero/auth/initiate`    | Redirects to Xero login       |
| GET    | `/xero/auth/callback`    | Handles OAuth callback        |
| GET    | `/xero/fetch/clients`    | Imports clients from Xero     |

## 📚 Resources
- [Xero Developer Guide](https://developer.xero.com/documentation/getting-started-guide/)