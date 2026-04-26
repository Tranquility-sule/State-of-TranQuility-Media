import streamlit as st
import yt_dlp
import os
import re
import imageio_ffmpeg as ff
from datetime import datetime
import tempfile

# --- 1. System Setup (Cloud Friendly) ---
# We use a temporary directory because Streamlit Cloud has restricted write access
SAVE_DIR = tempfile.gettempdir() 

# Get internal FFmpeg path
try:
    FFMPEG_BIN = ff.get_ffmpeg_exe()
except Exception:
    FFMPEG_BIN = None

# --- 2. Page Configuration ---
st.set_page_config(page_title="Tranquility Ultra-Light", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background: #10b981; color: white; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Tranquility Ultra-Light")
st.caption("Cloud-Verified Extraction Engine • Sani Suleiman Edition")

# --- 3. The Core Downloader Function ---
def download_media(url, mode, quality):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Save to the system's temp folder to avoid "Permission Denied" online
    base_filename = f"Tranquility_{timestamp}"
    outtmpl = os.path.join(SAVE_DIR, f"{base_filename}.%(ext)s")

    ydl_opts = {
        'ffmpeg_location': FFMPEG_BIN,
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    if mode == "Audio (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality.replace('kbps', ''),
            }],
        })
    else:
        # Standard format selection for better compatibility online
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Find the path of the downloaded file
            downloaded_file = ydl.prepare_filename(info)
            if mode == "Audio (MP3)":
                downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"
            return downloaded_file
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. User Interface ---
url_input = st.text_input("🔗 Paste Media Link", placeholder="YouTube, TikTok, Instagram...")

col1, col2 = st.columns(2)
with col1:
    type_choice = st.radio("Format", ["Video (MP4)", "Audio (MP3)"])
with col2:
    if type_choice == "Video (MP4)":
        qual = st.selectbox("Resolution", ["Best", "1080p", "720p"])
    else:
        qual = st.selectbox("Bitrate", ["320kbps", "192kbps", "128kbps"])

if st.button("🚀 START EXTRACTION"):
    if url_input:
        with st.status("🛠️ Engine processing... this may take a minute", expanded=True) as status:
            result_path = download_media(url_input, type_choice, qual)
            
            if "Error" in result_path:
                st.error("The server blocked this request or the link is private.")
                st.caption(f"Technical Detail: {result_path}")
                status.update(label="❌ Failed", state="error")
            else:
                st.balloons()
                status.update(label="✅ Ready for Download!", state="complete")
                with open(result_path, "rb") as file:
                    st.download_button(
                        label="💾 CLICK TO SAVE FILE",
                        data=file,
                        file_name=os.path.basename(result_path),
                        mime="video/mp4" if type_choice == "Video (MP4)" else "audio/mpeg"
                    )
    else:
        st.warning("Please enter a link first!")

st.divider()
st.markdown("<p style='text-align: center; color: #666;'>Developed by Sani Suleiman • Ikotun & Zaria Deployment</p>", unsafe_allow_html=True)
