import streamlit as st
import yt_dlp
import os
import datetime
import re
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
SAVE_DIR = "downloads"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# --- Page Setup ---
st.set_page_config(page_title="Tranquility Universal Pro", page_icon="💫", layout="wide")

# --- STABILIZED REFRESH ---
# We use 5 seconds here. Fast enough to see the time, 
# slow enough not to crash the download engine.
st_autorefresh(interval=5000, key="datetimeticker") 

# --- UI Styling ---
BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1596203117563-71a2510b655f?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(15, 23, 42, 0.95)), url("{BACKGROUND_IMAGE}");
        background-size: cover; background-attachment: fixed;
    }}
    .block-container {{ max-width: 1100px !important; margin: auto !important; padding-top: 0rem !important; }}
    
    .marquee-container {{
        width: 100%; overflow: hidden; background: rgba(16, 185, 129, 0.15);
        border-bottom: 2px solid #10b981; padding: 18px 0; margin-bottom: 25px;
    }}
    .marquee-text {{
        display: inline-block; white-space: nowrap; animation: scroll-left 25s linear infinite;
        color: #10b981; font-weight: 900; font-size: 1.6rem; text-transform: uppercase;
        letter-spacing: 3px; text-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
    }}
    @keyframes scroll-left {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    h1, h2, h3, label, p {{ font-family: 'Inter', sans-serif !important; color: #f1f5f9 !important; }}
    div.stBlock {{ background: rgba(30, 41, 59, 0.6); padding: 2.5rem; border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.3); backdrop-filter: blur(12px); }}
    
    .stButton>button {{ 
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #059669 100%); 
        color: white !important; padding: 1.1rem; font-weight: 800; border-radius: 12px; border: none;
    }}
    
    .clock-box {{
        background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;
        border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;
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

if 'history' not in st.session_state: st.session_state.history = []

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    with st.sidebar:
        # Simple Clock that works on ALL versions
        now = datetime.datetime.now()
        st.markdown(f"""
            <div class="clock-box">
                <h2 style="margin:0; color:#10b981;">{now.strftime("%H:%M:%S")}</h2>
                <p style="margin:0; font-size:0.8rem; color:#a7f3d0;">{now.strftime("%A, %d %B %Y")}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.success("Universal Mode: Active")
        st.info("User: Tranquility 💫")
        if st.button("🗑️ Clear Logs"):
            st.session_state.history = []
            st.rerun()

    st.markdown("### 📥 Media Source")
    url = st.text_input("Paste Link Here", placeholder="YouTube, TikTok, Instagram, Facebook...")
    
    if url:
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'thumbnail' in info:
                    st.image(info['thumbnail'], use_column_width=True)
                st.caption(f"📝 Title: {info.get('title', 'Unknown Media')}")
        except: st.warning("🔍 Syncing with source...")

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
            # Persistent Status Area
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
                    'external_downloader': 'ffmpeg',
                    'external_downloader_args': {'ffmpeg_i': ffmpeg_args} if ffmpeg_args else {},
                    'noplaylist': True,
                    'quiet': True,
                    'ignoreerrors': True
                }
                
                if mode == "Audio (MP3)":
                    bitrate = quality_option.split('k')[0]
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': bitrate}]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(data)
                    if mode == "Audio (MP3)": file_path = os.path.splitext(file_path)[0] + ".mp3"
                
                st.session_state.history.append({"t": datetime.datetime.now().strftime("%H:%M"), "title": data.get('title', 'Media File')})
                st.balloons()
                st.success("Extraction Successful!")
                with open(file_path, "rb") as f:
                    st.download_button("💾 DOWNLOAD FILE", f, file_name=os.path.basename(file_path))
            except Exception as e:
                st.error(f"Engine Error: The link might be private or invalid.")
        else:
            st.warning("Please provide a link.")

with col2:
    st.markdown("### 🕒 Session Activity")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.code(f"[{item['t']}] {item['title'][:35]}...")
    else:
        st.info("Waiting for Media Source...")

st.markdown("""<div style="text-align:center; margin-top:4rem;"><div style="background:rgba(16,185,129,0.1); color:#34d399; padding:8px 25px; border-radius:50px; border:1px solid #10b981; display:inline-block; font-weight:600;">Created by Sani Suleiman</div></div>""", unsafe_allow_html=True)