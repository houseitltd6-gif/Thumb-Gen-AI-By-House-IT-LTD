import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Fetching from Streamlit Secrets
            secret_info = st.secrets["service_account"]
            
            cred_dict = {
                "type": secret_info["type"],
                "project_id": secret_info["project_id"],
                "private_key_id": secret_info["private_key_id"],
                "private_key": secret_info["private_key"].replace('\\n', '\n'),
                "client_email": secret_info["client_email"],
                "client_id": secret_info["client_id"],
                "auth_uri": secret_info["auth_uri"],
                "token_uri": secret_info["token_uri"],
                "auth_provider_x509_cert_url": secret_info["auth_provider_x509_cert_url"],
                "client_x509_cert_url": secret_info["client_x509_cert_url"],
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Firebase Init Error: {e}")
            return None
    return firestore.client()

def ensure_user_profile(db, user_data):
    """Automatically creates a user profile in Firestore if it doesn't exist."""
    if not db: return
    try:
        user_ref = db.collection('users').document(user_data['uid'])
        if not user_ref.get().exists:
            user_ref.set({
                'email': user_data['email'],
                'role': 'user',
                'created_at': firestore.SERVER_TIMESTAMP
            })
    except Exception as e:
        print(f"Error creating profile: {e}")

def get_user_role(db, uid):
    """Retrieves user role with error handling."""
    if not db: return 'user'
    try:
        user_ref = db.collection('users').document(uid).get()
        if user_ref.exists:
            return user_ref.to_dict().get('role', 'user')
    except Exception:
        pass
    return 'user'
