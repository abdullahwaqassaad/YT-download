import streamlit as st
import yt_dlp
import os
import time
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
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Verify file was actually downloaded
            if not os.path.exists(filename):
                # Try alternative filename pattern
                filename = f"yt_{info['id']}.mp4"
                if not os.path.exists(filename):
                    return False, "File downloaded but not found"
            
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
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'ignoreerrors': False,
            'retries': 3,
            'socket_timeout': 60,
            'extractor_args': {
                'instagram': {
                    'skip_auth': True,
                    'extract_reels': True
                }
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return False, "Failed to extract video info"
            
            # Multiple fallback filename options
            filename = ydl.prepare_filename(info) if 'id' in info else f"ig_reel_{int(time.time())}.mp4"
            
            # Verify download
            if not os.path.exists(filename):
                return False, "File downloaded but not found"
            
            return True, filename
            
    except Exception as e:
        return False, str(e)

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
    
    yt_status = st.empty()
    
    if st.button("Download YouTube Video", key="yt_dl_btn"):
        if yt_url:
            if not is_youtube(yt_url):
                yt_status.error("❌ Invalid YouTube URL")
            else:
                with st.spinner("Downloading YouTube video..."):
                    success, result = download_youtube(yt_url)
                    if success:
                        yt_status.success("✅ Download complete!")
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
    
    ig_status = st.empty()
    
    if st.button("Download Instagram Reel", key="ig_dl_btn"):
        if ig_url:
            if not is_instagram_reel(ig_url):
                ig_status.error("❌ Invalid Instagram Reel URL")
            else:
                with st.spinner("Downloading Instagram reel..."):
                    success, result = download_instagram(ig_url)
                    if success:
                        ig_status.success("✅ Download complete!")
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
**Important Notes:**
1. For **private Instagram accounts**, create a `cookies.txt` file in the same folder
2. Instagram downloads may fail if:
   - The reel is from a private account (without cookies)
   - You've made too many requests recently
3. All downloads are automatically deleted after you save them
""")
