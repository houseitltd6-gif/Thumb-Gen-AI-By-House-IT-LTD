import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st
import json

def init_firebase():
    if not firebase_admin._apps:
        # Fetching GCP Service Account JSON key from st.secrets
        try:
            # Check if secrets contain firebase config
            if "firebase" in st.secrets:
                key_dict = json.loads(st.secrets["firebase"]["service_account"])
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            else:
                st.error("Firebase secrets not found in st.secrets")
                return None
        except Exception as e:
            st.error(f"Firebase initialization failed: {e}")
            return None
    return firestore.client()

def get_user_role(db, uid):
    try:
        user_ref = db.collection('users').document(uid)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict().get('role', 'user')
    except Exception as e:
        # Handle PermissionDenied or connection errors gracefully
        return 'user'
    return 'user'

def ensure_user_profile(db, uid, email):
    """
    Checks if a user exists in Firestore. If not, creates a new profile.
    """
    try:
        user_ref = db.collection('users').document(uid)
        doc = user_ref.get()
        if not doc.exists:
            user_ref.set({
                'email': email,
                'role': 'user',
                'created_at': firestore.SERVER_TIMESTAMP
            })
            return True
    except Exception as e:
        return False
    return False

def log_generation(db, uid, metadata):
    try:
        db.collection('projects').add({
            'uid': uid,
            'timestamp': firestore.SERVER_TIMESTAMP,
            **metadata
        })
    except Exception:
        pass

def get_admin_stats(db):
    try:
        users = db.collection('users').stream()
        projects = db.collection('projects').stream()
        return {
            'total_users': len(list(users)),
            'total_generations': len(list(projects))
        }
    except Exception:
        return {'total_users': 0, 'total_generations': 0}
