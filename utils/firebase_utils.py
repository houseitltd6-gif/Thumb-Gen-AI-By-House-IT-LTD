import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

def init_firebase():
    if not firebase_admin._apps:
        try:
            if "gcp_service_account" in st.secrets:
                service_account_info = st.secrets["gcp_service_account"]
                
                # ডিকশনারি বা স্ট্রিং চেক
                if isinstance(service_account_info, str):
                    key_dict = json.loads(service_account_info)
                else:
                    key_dict = dict(service_account_info)
                
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            else:
                st.error("Firebase secrets not found!")
                return None
        except Exception as e:
            st.error(f"Initialization failed: {e}")
            return None
    return firestore.client()

def get_user_role(db, uid):
    user_ref = db.collection('users').document(uid).get()
    if user_ref.exists:
        return user_ref.to_dict().get('role', 'user')
    return 'user'

def log_generation(db, uid, metadata):
    db.collection('projects').add({
        'uid': uid,
        'timestamp': firestore.SERVER_TIMESTAMP,
        **metadata
    })

def get_admin_stats(db):
    users = len(list(db.collection('users').stream()))
    projects = len(list(db.collection('projects').stream()))
    return {'total_users': users, 'total_generations': projects}
