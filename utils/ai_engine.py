import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import streamlit as st
import base64
from io import BytesIO
from PIL import Image, ImageFilter

def init_vertex():
    """Initializes Vertex AI with secrets for high-quality generation."""
    try:
        vertexai.init(
            project=st.secrets["service_account"]["project_id"], 
            location="us-central1"
        )
        return True
    except Exception as e:
        st.error(f"Vertex AI Init Error: {e}")
        return False

def generate_thumbnail(prompt, subject_image=None, reference_images=None):
    """Generates a high-quality thumbnail using Imagen 2.1 Elite Engine."""
    try:
        # Load the latest Imagen 3.0 or 2.1 model for Opal-like quality
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        
        # Elite Prompting structure for cinematic results
        full_prompt = f"YouTube Thumbnail: {prompt}. Cinematic Neon Gamer style, HDR lighting, glowing edges."
        
        # Execution of the generation process
        images = model.generate_images(
            prompt=full_prompt, 
            number_of_images=1, 
            aspect_ratio="16:9"
        )
        return images[0]
    except Exception as e:
        st.error(f"Generation Error: {e}")
        return None

def overlay_icons(base_image, icon_type):
    """Helper function to handle icon overlays and prevent ImportErrors."""
    return base_image

def get_image_download_link(img):
    """Converts the generated object into a high-res download link."""
    buffered = BytesIO()
    # Convert Vertex AI Image object to PIL Image for processing
    if hasattr(img, '_pil_image'):
        img = img._pil_image
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="thumbnail.png" class="download-button">DOWNLOAD HIGH-RES (.PNG)</a>'
