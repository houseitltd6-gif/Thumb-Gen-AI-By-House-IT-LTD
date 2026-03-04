import streamlit as st
import os
from utils.firebase_utils import initialize_firebase, ensure_user_profile, get_user_role

# Page Config
st.set_page_config(page_title="Thumb-Gen AI", layout="wide")

# Initialize DB
db = initialize_firebase()

# Authentication Logic in Sidebar
if 'user' not in st.session_state:
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        # Dummy Auth logic - Replace with your Firebase Auth logic
        st.session_state.user = {'uid': 'some_unique_id', 'email': email}
        if db:
            ensure_user_profile(db, st.session_state.user)
        st.rerun()
else:
    role = get_user_role(db, st.session_state.user['uid'])
    st.sidebar.success(f"Logged in as: {st.session_state.user['email']}")
    st.sidebar.info(f"Role: {role}")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

# Main UI - Stage 1: Style & Subject Upload
st.title("Thumb-Gen AI 🚀")
st.markdown("### Stage 1: Style & Subject Reference")

col1, col2 = st.columns(2)

with col1:
    style = st.selectbox("Select Thumbnail Style", ["Gamer Neon", "Cinematic", "Anime", "Vlog Classic"])
    
with col2:
    # Adding the Image Uploader here as requested
    uploaded_file = st.file_uploader("Upload Subject Image", type=['png', 'jpg', 'jpeg'])

if st.button("Next"):
    if uploaded_file is not None:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.style = style
        st.success("Style and Image saved! Proceeding to Next Stage...")
    else:
        st.warning("Please upload an image to continue.")

# Floating WhatsApp Support
st.markdown("""
    <a href="https://wa.me/YOUR_NUMBER" class="whatsapp-float" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="50">
    </a>
    <style>
    .whatsapp-float { position: fixed; bottom: 20px; right: 20px; z-index: 100; }
    </style>
""", unsafe_allow_html=True)
