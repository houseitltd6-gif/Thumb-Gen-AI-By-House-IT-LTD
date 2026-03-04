import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st
import json
def init_firebase():
    if not firebase_admin._apps:
        # Fetching GCP Service Account from st.secrets
        try:
            if "gcp_service_account" in st.secrets:
                service_account_info = st.secrets["gcp_service_account"]
                
                # Check if it's a string (JSON) or a dictionary
                if isinstance(service_account_info, str):
                    key_dict = json.loads(service_account_info)
                else:
                    key_dict = dict(service_account_info)
                
                # Initialize Firebase with the key
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            else:
                st.error("Firebase secrets not found in st.secrets")
                return None
        except Exception as e:
            st.error(f"Firebase initialization failed: {e}")
            return None
    return firestore.client()
