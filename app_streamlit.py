import os
import io
import requests
from PIL import Image
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Helmet Detection Dashboard",
    page_icon="🪖",
    layout="wide"
)

# Load Custom CSS
def load_css():
    css_path = "static/style.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# App Header
st.markdown("""
    <div class="custom-card">
        <h2 style="margin:0;">🪖 Helmet Detection System</h2>
        <p style="color: #a1a1aa; margin: 4px 0 0 0;">YOLO Inference via FastAPI Backend</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar System Health
with st.sidebar:
    st.header("⚙️ Server Status")
    try:
        res = requests.get(f"{API_URL}/health", timeout=2)
        if res.status_code == 200:
            data = res.json()
            st.markdown('<span class="status-badge">FastAPI Active</span>', unsafe_allow_html=True)
            st.caption(f"Model: `{data['model']}`")
        else:
            st.error("Server return error status.")
    except Exception:
        st.error("FastAPI Backend Offline")

# Helper function to read MJPEG stream frame by frame
def render_mjpeg_stream(response, placeholder):
    bytes_data = b""
    for chunk in response.iter_content(chunk_size=2048):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start marker
        b = bytes_data.find(b'\xff\xd9')  # JPEG end marker
        if a != -1 and b != -1:
            jpg = bytes_data[a:b+2]
            bytes_data = bytes_data[b+2:]
            placeholder.image(jpg, channels="BGR", use_container_width=True)

# App Tabs
tab_img, tab_vid = st.tabs(["🖼️ Image Processing", "🎥 Video Processing"])

# ==================== IMAGE TAB ====================
with tab_img:
    mode = st.radio("Choose Source:", ["Upload Custom Image", "Select from Media/ Folder"], key="img_mode", horizontal=True)
    
    col1, col2 = st.columns(2)
    
    if mode == "Upload Custom Image":
        with col1:
            st.markdown('<div class="custom-card"><b>Upload Image</b></div>', unsafe_allow_html=True)
            uploaded_img = st.file_uploader("Choose Image File", type=["jpg", "jpeg", "png"], key="img_file")
            if uploaded_img:
                st.image(uploaded_img, use_container_width=True)

        with col2:
            st.markdown('<div class="custom-card"><b>Detection Output</b></div>', unsafe_allow_html=True)
            if uploaded_img and st.button("Detect Helmet", key="btn_detect_uploaded_img"):
                with st.spinner("Processing image..."):
                    files = {"file": (uploaded_img.name, uploaded_img.getvalue(), uploaded_img.type)}
                    resp = requests.post(f"{API_URL}/detect/image", files=files)
                    if resp.status_code == 200:
                        st.image(Image.open(io.BytesIO(resp.content)), use_container_width=True)
                    else:
                        st.error("Failed to process image.")
                        
    else:  # Select from Media folder
        media_imgs = [f for f in os.listdir("Media") if f.endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists("Media") else []
        with col1:
            st.markdown('<div class="custom-card"><b>Sample Media Files</b></div>', unsafe_allow_html=True)
            selected_img = st.selectbox("Select Image:", media_imgs)
            if selected_img:
                img_path = os.path.join("Media", selected_img)
                st.image(img_path, use_container_width=True)

        with col2:
            st.markdown('<div class="custom-card"><b>Detection Output</b></div>', unsafe_allow_html=True)
            if selected_img and st.button("Detect Helmet", key="btn_detect_local_img"):
                with st.spinner("Processing image..."):
                    img_path = os.path.join("Media", selected_img)
                    with open(img_path, "rb") as f:
                        files = {"file": (selected_img, f.read(), "image/jpeg")}
                        resp = requests.post(f"{API_URL}/detect/image", files=files)
                    if resp.status_code == 200:
                        st.image(Image.open(io.BytesIO(resp.content)), use_container_width=True)
                    else:
                        st.error("Failed to process image.")

# ==================== VIDEO TAB ====================
with tab_vid:
    vid_mode = st.radio("Choose Video Source:", ["Upload Custom Video (.mp4)", "Select from Media/ Folder"], key="vid_mode", horizontal=True)
    
    col1, col2 = st.columns(2)
    
    if vid_mode == "Upload Custom Video (.mp4)":
        with col1:
            st.markdown('<div class="custom-card"><b>Upload Video</b></div>', unsafe_allow_html=True)
            uploaded_vid = st.file_uploader("Choose Video File", type=["mp4", "avi", "mov"], key="vid_file")
            if uploaded_vid:
                st.video(uploaded_vid)

        with col2:
            st.markdown('<div class="custom-card"><b>Real-time Detection Stream</b></div>', unsafe_allow_html=True)
            vid_placeholder = st.empty()
            if uploaded_vid and st.button("Start Live Stream", key="btn_stream_uploaded_vid"):
                files = {"file": (uploaded_vid.name, uploaded_vid.getvalue(), uploaded_vid.type)}
                try:
                    resp = requests.post(f"{API_URL}/detect/video/upload", files=files, stream=True)
                    if resp.status_code == 200:
                        render_mjpeg_stream(resp, vid_placeholder)
                    else:
                        st.error("Could not stream uploaded video.")
                except Exception as e:
                    st.error(f"Error streaming video: {e}")

    else:  # Select from Media folder
        media_vids = [f for f in os.listdir("Media") if f.endswith('.mp4')] if os.path.exists("Media") else []
        with col1:
            st.markdown('<div class="custom-card"><b>Sample Media Videos</b></div>', unsafe_allow_html=True)
            selected_vid = st.selectbox("Select Video File:", media_vids)
            if selected_vid:
                st.video(os.path.join("Media", selected_vid))

        with col2:
            st.markdown('<div class="custom-card"><b>Real-time Detection Stream</b></div>', unsafe_allow_html=True)
            vid_placeholder = st.empty()
            if selected_vid and st.button("Start Live Stream", key="btn_stream_local_vid"):
                try:
                    resp = requests.get(f"{API_URL}/detect/video/local/{selected_vid}", stream=True)
                    if resp.status_code == 200:
                        render_mjpeg_stream(resp, vid_placeholder)
                    else:
                        st.error("Could not stream video.")
                except Exception as e:
                    st.error(f"Error streaming video: {e}")