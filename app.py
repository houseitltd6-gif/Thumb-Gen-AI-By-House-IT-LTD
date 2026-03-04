import streamlit as st
import os
from utils.firebase_utils import init_firebase, get_user_role, log_generation, get_admin_stats, ensure_user_profile
from utils.ai_engine import init_vertex, generate_thumbnail, overlay_icons, get_image_download_link

# Page Configuration
st.set_page_config(
    page_title="Thumb-Gen AI | House IT LTD",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Firebase and Vertex AI
db = init_firebase()
init_vertex()

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Ensure directories exist
os.makedirs("assets", exist_ok=True)
os.makedirs("utils", exist_ok=True)

local_css("assets/styles.css")

# --- UI Components ---

def floating_whatsapp():
    whatsapp_html = """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <a href="https://wa.me/your_number" class="whatsapp-float" target="_blank">
    <i class="fa fa-whatsapp"></i>
    </a>
    """
    st.markdown(whatsapp_html, unsafe_allow_html=True)

def neon_tagline():
    st.markdown('<div class="typewriter">Dominate YouTube with AI-Powered Visuals.</div>', unsafe_allow_html=True)

def adsense_slot(position="top"):
    st.markdown(f'<div class="adsense-placeholder">Google AdSense - {position}</div>', unsafe_allow_html=True)

# --- App Layout ---

def main():
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Sidebar
    with st.sidebar:
        st.title("User Profile")
        if not st.session_state.user:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                # Mock Login logic - In production, use firebase_utils
                uid = "mock_123"
                st.session_state.user = {"uid": uid, "email": email}
                # Automatically ensure user profile exists in Firestore
                if db:
                    ensure_user_profile(db, uid, email)
                st.rerun()
        else:
            st.write(f"Logged in as: {st.session_state.user['email']}")
            role = get_user_role(db, st.session_state.user['uid']) if db else 'user'
            if role == 'admin':
                st.success("Admin Access Granted")
                if st.button("View Admin Dashboard"):
                    st.session_state.page = "admin"
            
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

        st.divider()
        adsense_slot("Sidebar")
        
    # Main Content Area
    if st.session_state.get("page") == "admin":
        render_admin_dashboard()
        return

    adsense_slot("Top")
    st.title("Thumb-Gen AI 🚀")
    neon_tagline()
    
    st.divider()
    
    # 5-Stage Workflow Interface
    if 'stage' not in st.session_state:
        st.session_state.stage = 1
    
    stages = ["Style & Subject", "Metadata", "Asset Select", "Quality Presets", "Result"]
    st.markdown(f"### Stage {st.session_state.stage}: {stages[st.session_state.stage-1]}")
    
    # Render Stage Content
    if st.session_state.stage == 1:
        st.info("Select your style and upload your subject image.")
        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("Select Style", ["Gamer Neon", "Cinematic", "Minimalist"])
        with col2:
            uploaded_file = st.file_uploader("Upload Subject (PNG, JPG, JPEG)", type=['png', 'jpg', 'jpeg'])
            
        if st.button("Next"):
            if uploaded_file:
                st.session_state.style = style
                st.session_state.subject = uploaded_file
                st.session_state.stage = 2
                st.rerun()
            else:
                st.warning("Please upload a subject image to proceed.")
        
    elif st.session_state.stage == 2:
        title = st.text_input("Thumbnail Title (e.g., 'ChatGPT Secrets')")
        keywords = st.text_area("Additional Keywords")
        if st.button("Next"):
            st.session_state.title = title
            st.session_state.keywords = keywords
            st.session_state.stage = 3
            st.rerun()

    elif st.session_state.stage == 3:
        st.info("Select specific overlay icons or assets.")
        use_gpt = st.checkbox("ChatGPT Icon", value="ChatGPT" in st.session_state.get('title', ''))
        use_bkash = st.checkbox("bKash Icon", value="bKash" in st.session_state.get('title', ''))
        if st.button("Next"):
            st.session_state.use_gpt = use_gpt
            st.session_state.use_bkash = use_bkash
            st.session_state.stage = 4
            st.rerun()
        
    elif st.session_state.stage == 4:
        quality = st.select_slider("Quality Preset", options=["Draft", "HD", "Ultra"])
        if st.button("Generate"):
            st.session_state.quality = quality
            with st.spinner("AI is crafting your visual..."):
                img = generate_thumbnail(f"{st.session_state.style} thumbnail with title {st.session_state.title}", st.session_state.subject)
                img = overlay_icons(img, st.session_state.title)
                st.session_state.final_image = img
                if st.session_state.user and db:
                    log_generation(db, st.session_state.user['uid'], {
                        "title": st.session_state.title,
                        "style": st.session_state.style
                    })
            st.session_state.stage = 5
            st.rerun()
        
    elif st.session_state.stage == 5:
        st.success("Generation Complete!")
        st.image(st.session_state.final_image, caption="Final Thumbnail (1280x720)")
        
        # Download Link Handling
        img_data = get_image_download_link(st.session_state.final_image)
        st.markdown(f'<a href="{img_data}" download="thumbnail.png" class="stButton"><button style="width:100%">Download High-Res (.png)</button></a>', unsafe_allow_html=True)
        
        if st.button("Start New"):
            st.session_state.stage = 1
            # Clear stage-specific state
            for key in ['style', 'subject', 'title', 'keywords', 'final_image']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # Footer
    st.divider()
    cols = st.columns(4)
    cols[0].markdown("[Terms of Service](#)")
    cols[1].markdown("[Privacy Policy](#)")
    cols[3].markdown("© 2026 House IT LTD")
    
    floating_whatsapp()

def render_admin_dashboard():
    st.title("Admin Control Panel")
    if st.button("Back to Generator"):
        st.session_state.page = "main"
        st.rerun()
    
    if db:
        stats = get_admin_stats(db)
        cols = st.columns(3)
        cols[0].metric("Total Users", stats['total_users'])
        cols[1].metric("Total Generations", stats['total_generations'])
        
        st.subheader("Recent User Activity")
        # In a real app, you'd fetch and display user logs here
        st.info("Log tracking is active in Firestore.")
    else:
        st.warning("Firebase not initialized. Admin stats unavailable.")

if __name__ == "__main__":
    main()
