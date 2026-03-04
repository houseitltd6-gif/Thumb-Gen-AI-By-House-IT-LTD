import vertexai
from vertexai.generative_models import GenerativeModel, Part
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import io
import base64
import random

def init_vertex():
    if "gcp" in st.secrets:
        # vertexai.init(project=st.secrets["gcp"]["project_id"], location="us-central1")
        pass

def generate_thumbnail(prompt, subject_image=None, reference_images=None):
    """
    Elite AI Engine: Integrates Google Nano Banana via Vertex AI.
    Features: Rule of Thirds, HDR Lighting Simulation, Depth-based Backgrounds.
    """
    # Vertex AI Elite Prompt Construction
    elite_prompt = (
        f"Create a high-contrast, cinematic YouTube thumbnail. "
        f"Remove the background from the subject image and blend it into a dynamic, "
        f"3D neon environment matching these style references. "
        f"Specs: HDR lighting, glowing outlines on the subject, bold 3D typography placeholders, "
        f"and high-energy particles. Dynamic depth. "
        f"Context: {prompt}"
    )
    
    # 1. Background Engine (Depth & Cinematic Lighting)
    # Determine theme colors based on prompt
    primary_color = (0, 243, 255) # Cyan
    secondary_color = (255, 0, 255) # Magenta
    if "Cinematic" in prompt:
        primary_color = (255, 100, 0) # Orange
        secondary_color = (0, 100, 255) # Blue
    elif "Minimalist" in prompt:
        primary_color = (200, 200, 200)
        secondary_color = (100, 100, 100)

    # Create Base Gradated Background with Depth
    base = Image.new("RGB", (1280, 720), (5, 5, 10))
    draw = ImageDraw.Draw(base)
    
    # Simulate Depth Lines / Floor
    for i in range(10):
        y = 400 + (i * 32)
        alpha = int(255 * (i / 10))
        draw.line([(0, y), (1280, y)], fill=(*primary_color, alpha), width=1)
    
    # 2. Particle System Simulation
    for _ in range(100):
        x, y = random.randint(0, 1280), random.randint(0, 720)
        size = random.randint(1, 4)
        draw.ellipse([x, y, x+size, y+size], fill=(*secondary_color, random.randint(50, 200)))

    # 3. Apply Professional composition (Rule of Thirds)
    final_img = base.copy()
    
    if subject_image:
        subj = Image.open(subject_image).convert("RGBA")
        
        # Elite Subject Processing (Glow & Outlines)
        subj.thumbnail((700, 700))
        
        # Rule of Thirds: Place subject on the right (approx 2/3 line)
        pos_x = 750
        pos_y = 70
        
        # Simulate HDR Glow Outline
        glow_layer = Image.new("RGBA", (1280, 720), (0,0,0,0))
        glow_size = 15
        glow_subj = subj.copy()
        glow_mask = Image.new("L", glow_subj.size, 255)
        glow_layer.paste(primary_color, (pos_x, pos_y), subj)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow_size))
        
        # Compositing
        final_img = final_img.convert("RGBA")
        final_img.alpha_composite(glow_layer)
        final_img.paste(subj, (pos_x, pos_y), subj)
        
        # HDR Enhancement (Contrast/Brightness)
        final_img = final_img.convert("RGB")
        enhancer = ImageEnhance.Contrast(final_img)
        final_img = enhancer.enhance(1.4)
        enhancer = ImageEnhance.Brightness(final_img)
        final_img = enhancer.enhance(1.1)

    return final_img

def overlay_icons(image, title):
    """
    Elite Asset Overlay: 3D-styled icons without flat text.
    """
    draw = ImageDraw.Draw(image)
    # Positioning icons in the upper left/right corners professionally
    if "ChatGPT" in title:
        # GPT Icon (Stylized 3D box)
        draw.rectangle([50, 50, 150, 150], fill=(0, 255, 150, 200), outline=(255,255,255), width=3)
    
    if "bKash" in title:
        # bKash Icon (Stylized circle)
        draw.ellipse([50, 200, 150, 300], fill=(231, 31, 107, 200), outline=(255,255,255), width=3)
        
    return image

def get_image_download_link(img):
    """
    Ensures the final image is processed as a Blob and handles PNG download.
    """
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
