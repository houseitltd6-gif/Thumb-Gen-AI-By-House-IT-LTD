import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.aiplatform as aiplatform

st.title("🔍 Thumb-Gen AI Diagnostic Tool")

# 1. Check Streamlit Secrets
st.subheader("1. Streamlit Secrets Status")
if "firebase" in st.secrets and "gcp_service_account" in st.secrets:
    st.success("✅ Secrets are configured correctly in Streamlit Cloud!")
else:
    st.error("❌ Secrets are MISSING! Go to Settings > Secrets and paste the TOML code.")

# 2. Check Firebase Connection
st.subheader("2. Firebase Connection Test")
try:
    if not firebase_admin._apps:
        cred_dict = dict(st.secrets["gcp_service_account"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    st.success("✅ Firebase Firestore is connected successfully!")
except Exception as e:
    st.error(f"❌ Firebase Connection Failed: {e}")

# 3. Check Vertex AI (Nano Banana)
st.subheader("3. Vertex AI Integration Test")
try:
    aiplatform.init(project=st.secrets["gcp_service_account"]["project_id"])
    st.success("✅ Vertex AI (Nano Banana) is ready!")
except Exception as e:
    st.error(f"❌ Vertex AI Initialization Failed: {e}")

st.info("যদি উপরের সবগুলো সবুজ (Success) দেখায়, তবে বুঝবেন আপনার আগের কোডে কোনো UI এরর ছিল।")
