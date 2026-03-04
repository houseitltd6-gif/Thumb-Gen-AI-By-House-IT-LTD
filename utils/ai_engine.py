import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

def init_vertex():
    """Initializes Vertex AI with secrets."""
    try:
        vertexai.init(
            project=st.secrets["service_account"]["project_id"], 
            location="us-central1"
        )
        return True
    except Exception as e:
        st.error(f"Vertex AI Init Error: {e}")
        return False

def generate_thumbnail(prompt_text, subject_image, reference_images):
    """Generates a high-quality thumbnail using Imagen 2.1."""
    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        
        # Elite Prompt Engineering
        full_prompt = f"YouTube Thumbnail: {prompt_text}. Cinematic Neon Gamer style, HDR lighting, glowing edges."
        
        # Generate
        images = model.generate_images(prompt=full_prompt, number_of_images=1, aspect_ratio="16:9")
        return images[0]
    except Exception as e:
        st.error(f"Generation Error: {e}")
        return None

def overlay_icons(base_image, icon_type):
    """Placeholder for icon overlay logic to prevent ImportErrors."""
    return base_image

def get_image_download_link(img):
    """Creates a base64 download link."""
    buffered = BytesIO()
    # Handle both PIL and Vertex AI Image objects
    if hasattr(img, '_pil_image'):
        img = img._pil_image
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="thumbnail.png" class="download-button">DOWNLOAD HIGH-RES (.PNG)</a>'
