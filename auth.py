# auth.py
import streamlit as st
from google_auth_oauthlib.flow import Flow
import os
import json

# Permitir HTTP para localhost (só em desenvolvimento)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_google_flow():
    # Carregar client_secret.json
    with open("client_secret.json", "r") as f:
        client_config = json.load(f)["web"]
    
    return Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"],
        redirect_uri="http://localhost:8501"
    )

def login():
    flow = get_google_flow()
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.markdown(f'<a href="{auth_url}" target="_self" style="display: inline-block; background-color: #4285F4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🔐 Login com Google</a>', unsafe_allow_html=True)

def handle_redirect():
    if "code" in st.query_params:
        flow = get_google_flow()
        flow.fetch_token(code=st.query_params["code"])
        creds = flow.credentials
        
        # Obter informações do usuário
        from google.auth.transport.requests import Request
        request = Request()
        id_info = creds.id_token
        # Para obter nome/email, use:
        import requests
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {creds.token}"}
        )
        user_info = resp.json()
        
        st.session_state.user = {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        }
        st.query_params.clear()
        st.rerun()