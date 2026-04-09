import streamlit as st
import yt_dlp
import os
import datetime
import re
import imageio_ffmpeg as ff

# --- Configuration ---
SAVE_DIR = "downloads"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Dynamically find the portable FFmpeg engine
FFMPEG_EXE = ff.get_ffmpeg_exe()

# --- 1. Page Setup ---
st.set_page_config(page_title="Tranquility Universal Pro", page_icon="💫", layout="wide")

# --- 2. Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- 3. UI Styling ---
BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1596203117563-71a2510b655f?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(15, 23, 42, 0.95)), url("{BACKGROUND_IMAGE}");
        background-size: cover; background-attachment: fixed;
    }}
    .block-container {{ max-width: 1100px !important; margin: auto !important; padding-top: 3.5rem !important; }}
    .marquee-container {{
        width: 100%; overflow: hidden; background: rgba(16, 185, 129, 0.15);
        border-bottom: 2px solid #10b981; padding: 15px 0; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); border-radius: 8px;
    }}
    .marquee-text {{
        display: inline-block; white-space: nowrap; animation: scroll-left 25s linear infinite;
        color: #10b981; font-weight: 900; font-size: 1.6rem; text-transform: uppercase;
        letter-spacing: 3px; text-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
    }}
    @keyframes scroll-left {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    h1, h2, h3, label, p {{ font-family: 'Inter', sans-serif !important; color: #f1f5f9 !important; }}
    div.stBlock {{ 
        background: rgba(30, 41, 59, 0.6); padding: 2.5rem; border-radius: 20px; 
        border: 1px solid rgba(16, 185, 129, 0.3); backdrop-filter: blur(12px); 
    }}
    .stButton>button {{ 
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #059669 100%); 
        color: white !important; padding: 1.1rem; font-weight: 800; border-radius: 12px; border: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Welcome Bar ---
st.markdown("""
    <div class="marquee-container">
        <div class="marquee-text">
            🚀 UNIVERSAL ACCESS ENABLED: TIKTOK, INSTAGRAM, FACEBOOK, AND YOUTUBE! ✨ VERIFIED AS THE BEST ALL-IN-ONE DOWNLOADER BY SANI SULEIMAN ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align:center;'>💫 Tranquility Universal Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Multi-Platform Extraction Engine • Sani Suleiman Edition</p>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3039/3039387.png", width=80)
        st.markdown("## Control Center")
        st.success("Status: Online 📡")
        st.info("User: Tranquility 💫")
        if st.button("🗑️ Clear Logs"):
            st.session_state['history'] = []
            st.rerun()

    st.markdown("### 📥 Media Source")
    url = st.text_input("Paste Link Here", placeholder="YouTube, TikTok, Instagram, Facebook...")
    
    if url:
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'thumbnail' in info:
                    st.image(info['thumbnail'], use_column_width=True)
                st.caption(f"📝 Title: {info.get('title', 'Media File')}")
        except: st.write("🔍 Syncing with source...")

    st.markdown("#### ✂️ Precision Trim (Optional)")
    t_col1, t_col2 = st.columns(2)
    start_time = t_col1.text_input("Start (HH:MM:SS)", "00:00:00")
    end_time = t_col2.text_input("End (HH:MM:SS)", "00:00:00")

    st.markdown("#### ⚙️ Quality Settings")
    mode = st.radio("Output Format", ["Video (MP4)", "Audio (MP3)"], horizontal=True)
    
    if mode == "Video (MP4)":
        quality_option = st.selectbox("Resolution:", ["Best Available", "1080p", "720p", "480p"])
    else:
        quality_option = st.selectbox("Bitrate:", ["320kbps", "192kbps", "128kbps"])

    if st.button("🚀 START EXTRACTION"):
        if url:
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        p = d.get('_percent_str', '0%').replace('%','')
                        progress_bar.progress(float(p.strip())/100)
                        status_text.text(f"📥 Extracting: {p}%")

                fmt = 'best'
                if mode == "Video (MP4)" and quality_option != "Best Available":
                    res = quality_option.split('p')[0]
                    fmt = f"bestvideo[height<={res}]+bestaudio/best[height<={res}]"

                ffmpeg_args = []
                if start_time != "00:00:00": ffmpeg_args.extend(["-ss", start_time])
                if end_time != "00:00:00": ffmpeg_args.extend(["-to", end_time])

                ydl_opts = {
                    'format': fmt,
                    'outtmpl': f'{SAVE_DIR}/%(title)s.%(ext)s',
                    'progress_hooks': [progress_hook],
                    'ffmpeg_location': FFMPEG_EXE,
                    'noplaylist': True,
                    'quiet': True,
                    'ignoreerrors': False,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                if mode == "Audio (MP3)":
                    bitrate = quality_option.split('k')[0]
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': bitrate}]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(data)
                    if mode == "Audio (MP3)": file_path = os.path.splitext(file_path)[0] + ".mp3"
                
                st.session_state['history'].append({"t": datetime.datetime.now().strftime("%H:%M"), "title": data.get('title', 'Media File')})
                st.balloons()
                st.success("Extraction Successful!")
                with open(file_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD FILE", f, file_name=os.path.basename(file_path))
            except Exception as e:
                st.error(f"Engine Detail: {str(e)[:250]}")
        else:
            st.warning("Please provide a link.")

with col2:
    st.markdown("### 🕒 Session Activity")
    if 'history' in st.session_state and st.session_state['history']:
        for item in reversed(st.session_state['history']):
            st.code(f"[{item['t']}] {item['title'][:35]}...")
    else:
        st.info("Waiting for Media Source...")

st.markdown("""<div style="text-align:center; margin-top:4rem;"><div style="background:rgba(16,185,129,0.1); color:#34d399; padding:8px 25px; border-radius:50px; border:1px solid #10b981; display:inline-block; font-weight:600;">Created by Sani Suleiman</div></div>""", unsafe_allow_html=True)
