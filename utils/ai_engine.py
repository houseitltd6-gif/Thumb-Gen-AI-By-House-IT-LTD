import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

def generate_thumbnail(prompt_text, subject_image, reference_images):
    try:
        # Initialize Vertex AI with Project ID from Secrets
        vertexai.init(project=st.secrets["service_account"]["project_id"], location="us-central1")
        
        # Load Imagen 2.1 Model
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001") # Use latest available
        
        # Elite Prompt Engineering for Opal-like quality
        full_prompt = f"""
        YouTube Thumbnail Masterpiece: {prompt_text}. 
        Style: High-contrast Neon Gamer aesthetic, HDR lighting, cinematic depth.
        Composition: Subject focused on the right side, bold 3D typography placeholders on the left.
        Details: Glowing outlines, vibrant particles, matching the provided style references perfectly.
        """
        
        # Generating image
        images = model.generate_images(
            prompt=full_prompt,
            number_of_images=1,
            aspect_ratio="16:9",
            guidance_scale=15.0 # Higher scale for better adherence to prompt
        )
        
        return images[0]
    except Exception as e:
        st.error(f"Imagen Generation Error: {e}")
        return None

def get_image_download_link(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/png;base64,{img_str}" download="thumbnail.png" class="download-button">DOWNLOAD HIGH-RES (.PNG)</a>'
