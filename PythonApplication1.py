import streamlit as st
import yt_dlp
import os
from urllib.parse import urlparse

# ========================
# Core Download Functions
# ========================

def download_youtube(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'yt_%(title)s.%(ext)s',
            'quiet': True,
            'extract_flat': False,
            'force_generic_extractor': True,
            'ignoreerrors': False,
            'retries': 3,
            'socket_timeout': 30,
            'noplaylist': True,
            'progress_hooks': [youtube_progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return True, filename
            
    except Exception as e:
        return False, str(e)

def download_instagram(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'ig_%(id)s.%(ext)s',
            'quiet': True,
            'extract_flat': False,
            'force_generic_extractor': True,
            'cookiefile': 'cookies.txt',
            'ignoreerrors': False,
            'retries': 3,
            'socket_timeout': 60,
            'extractor_args': {
                'instagram': {
                    'skip_auth': True,
                    'extract_reels': True
                }
            },
            'progress_hooks': [instagram_progress_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return False, "Failed to extract video info"
            
            # Multiple fallback filename options
            filename = ydl.prepare_filename(info) if 'id' in info else f"ig_reel_{int(time.time())}.mp4"
            return True, filename
            
    except Exception as e:
        return False, str(e)

# ========================
# Progress Trackers
# ========================

def youtube_progress_hook(d):
    if st.session_state.get('yt_progress_bar'):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%','')
            try:
                st.session_state.yt_progress_bar.progress(float(percent)/100)
            except:
                pass

def instagram_progress_hook(d):
    if st.session_state.get('ig_progress_bar'):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%','')
            try:
                st.session_state.ig_progress_bar.progress(float(percent)/100)
            except:
                pass

# ========================
# URL Validators
# ========================

def is_youtube(url):
    domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
    parsed = urlparse(url)
    return (parsed.netloc.replace('www.','') in domains and 
            any(x in parsed.path for x in ['/watch', '/shorts']))

def is_instagram_reel(url):
    domains = ['instagram.com', 'www.instagram.com']
    parsed = urlparse(url)
    return (parsed.netloc.replace('www.','') in domains and 
            '/reel/' in parsed.path)

# ========================
# Streamlit UI
# ========================

st.set_page_config(
    page_title="Universal Video Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 Universal Video Downloader")
st.caption("Download YouTube Videos/Shorts and Instagram Reels")

tab_yt, tab_ig = st.tabs(["YouTube Downloader", "Instagram Downloader"])

# YouTube Tab
with tab_yt:
    st.subheader("YouTube Video/Shorts Downloader")
    yt_url = st.text_input(
        "Enter YouTube URL:",
        placeholder="https://www.youtube.com/watch?v=... or https://youtube.com/shorts/...",
        key="yt_url"
    )
    
    st.session_state.yt_progress_bar = st.progress(0)
    yt_status = st.empty()
    
    if st.button("Download YouTube Video", key="yt_dl_btn"):
        if yt_url:
            if not is_youtube(yt_url):
                yt_status.error("❌ Invalid YouTube URL")
            else:
                with st.spinner("Connecting to YouTube..."):
                    success, result = download_youtube(yt_url)
                    if success:
                        yt_status.success(f"✅ Download complete: {os.path.basename(result)}")
                        with open(result, "rb") as f:
                            st.download_button(
                                label="Save Video",
                                data=f,
                                file_name=os.path.basename(result),
                                mime="video/mp4"
                            )
                        os.remove(result)
                    else:
                        yt_status.error(f"❌ Error: {result}")
        else:
            yt_status.warning("⚠️ Please enter a YouTube URL")

# Instagram Tab
with tab_ig:
    st.subheader("Instagram Reels Downloader")
    ig_url = st.text_input(
        "Enter Instagram Reel URL:",
        placeholder="https://www.instagram.com/reel/...",
        key="ig_url"
    )
    
    st.session_state.ig_progress_bar = st.progress(0)
    ig_status = st.empty()
    
    if st.button("Download Instagram Reel", key="ig_dl_btn"):
        if ig_url:
            if not is_instagram_reel(ig_url):
                ig_status.error("❌ Invalid Instagram Reel URL")
            else:
                with st.spinner("Connecting to Instagram..."):
                    success, result = download_instagram(ig_url)
                    if success:
                        ig_status.success(f"✅ Download complete: {os.path.basename(result)}")
                        with open(result, "rb") as f:
                            st.download_button(
                                label="Save Reel",
                                data=f,
                                file_name=os.path.basename(result),
                                mime="video/mp4"
                            )
                        os.remove(result)
                    else:
                        ig_status.error(f"❌ Error: {result}")
        else:
            ig_status.warning("⚠️ Please enter an Instagram URL")

# Footer
st.divider()
st.markdown("""
**Tips:**
- For private Instagram accounts, add a `cookies.txt` file
- YouTube downloads typically work without issues
- If Instagram fails, try again after some time
- Downloads are automatically deleted after saving
""")
