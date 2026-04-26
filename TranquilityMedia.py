import streamlit as st
import yt_dlp
import os
import re
import imageio_ffmpeg as ff
from datetime import datetime

# --- System Check ---
SAVE_DIR = "downloads"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Get internal FFmpeg path
FFMPEG_BIN = ff.get_ffmpeg_exe()

# --- Page UI Configuration ---
st.set_page_config(page_title="Tranquility Ultra-Light", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background: #10b981; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Tranquility Ultra-Light")
st.caption("High-Performance Extraction Engine • Sani Suleiman Edition")

# --- Logic: The Downloader Engine ---
def download_media(url, mode, quality):
    # Setup filenames and paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outtmpl = os.path.join(SAVE_DIR, f"Tranquility_{timestamp}.%(ext)s")

    # Dynamic Options based on Video or Audio
    ydl_opts = {
        'ffmpeg_location': FFMPEG_BIN,
        'outtmpl': outtmpl,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
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
        # Simple high-quality video selection
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Find the actual final file path
            filename = ydl.prepare_filename(info)
            if mode == "Audio (MP3)":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI Layout ---
url_input = st.text_input("🔗 Paste Media Link", placeholder="YouTube, Facebook, Instagram...")

col1, col2 = st.columns(2)
with col1:
    type_choice = st.radio("Format", ["Video (MP4)", "Audio (MP3)"])
with col2:
    if type_choice == "Video (MP4)":
        qual = st.selectbox("Resolution", ["Best", "1080p", "720p"])
    else:
        qual = st.selectbox("Bitrate", ["320kbps", "192kbps", "128kbps"])

if st.button("🚀 Start Extraction"):
    if url_input:
        with st.status("🛠️ Extracting media... please wait", expanded=True) as status:
            result_path = download_media(url_input, type_choice, qual)
            
            if "Error" in result_path:
                st.error(result_path)
                status.update(label="❌ Extraction Failed", state="error")
            else:
                st.balloons()
                status.update(label="✅ Success!", state="complete")
                with open(result_path, "rb") as file:
                    st.download_button(
                        label="💾 Save to Device",
                        data=file,
                        file_name=os.path.basename(result_path),
                        mime="video/mp4" if type_choice == "Video (MP4)" else "audio/mpeg"
                    )
    else:
        st.warning("Please enter a valid link first!")

st.divider()
st.center = st.markdown("<p style='text-align: center;'>Verified by Sani Suleiman</p>", unsafe_allow_html=True)
