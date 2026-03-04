import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.aiplatform as aiplatform

st.set_page_config(page_title="Status Check", layout="wide")

st.title("🚀 Thumb-Gen AI: System Health Check")

# ১. সিক্রেটস চেক
st.subheader("📡 Step 1: Streamlit Secrets")
if "firebase" in st.secrets and "gcp_service_account" in st.secrets:
    st.success("✅ Secrets are detected!")
else:
    st.error("❌ Secrets are missing! Please check Advanced Settings.")

# ২. ফায়ারবেস কানেকশন টেস্ট
st.subheader("🔥 Step 2: Firebase Connection")
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["gcp_service_account"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    st.success("✅ Firebase Firestore is connected!")
except Exception as e:
    st.error(f"❌ Firebase Failed: {e}")

# ৩. এআই ইঞ্জিন (Vertex AI) টেস্ট
st.subheader("🤖 Step 3: Vertex AI (Nano Banana)")
try:
    aiplatform.init(project=st.secrets["gcp_service_account"]["project_id"])
    st.success("✅ AI Engine initialized successfully!")
except Exception as e:
    st.error(f"❌ Vertex AI Failed: {e}")

st.divider()
st.info("যদি সব সবুজ দেখায়, তাহলে বুঝবেন আপনার আগের UI কোডে এরর ছিল।")
