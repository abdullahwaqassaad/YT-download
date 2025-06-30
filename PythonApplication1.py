import streamlit as st
import yt_dlp
import os

def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'quiet': True,
            'extract_flat': False,  # Essential for Shorts
            'force_generic_extractor': True,  # Helps with Shorts
            'ignoreerrors': True,  # Skip unavailable videos
            'retries': 3,  # Retry on failures
            'socket_timeout': 30  # Longer timeout for Shorts
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            ext = info_dict.get('ext', 'mp4')
            filename = f"{video_title}.{ext}"
            return True, filename
    except Exception as e:
        return False, str(e)

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', '0%')
        progress = progress.replace('%', '')
        try:
            progress_float = max(0, min(100, float(progress)))  # Clamp between 0-100
            progress_bar.progress(progress_float / 100)  # Convert to 0.0-1.0
        except ValueError:
            pass

# Streamlit UI Configuration
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="▶️",
    layout="centered"
)

# Main App Interface
st.title("🎬 YouTube Video Downloader")
st.caption("Download regular videos and Shorts in best quality")

url = st.text_input(
    "Enter YouTube URL:",
    placeholder="https://www.youtube.com/watch?v=... or https://youtube.com/shorts/..."
)

progress_bar = st.progress(0)
status_message = st.empty()

if st.button("Download Video", type="primary"):
    if url:
        status_message.info("Starting download...")
        progress_bar.progress(0.05)  # Initial progress
        
        success, message = download_video(url)
        
        if success:
            status_message.success(f"✅ Download complete!")
            progress_bar.progress(1.0)
            
            if os.path.exists(message):
                with open(message, "rb") as file:
                    btn = st.download_button(
                        label="Save Video",
                        data=file,
                        file_name=message,
                        mime="video/mp4",
                        type="primary"
                    )
                if btn:
                    os.remove(message)  # Clean up after download
            else:
                st.warning("File downloaded but not found locally")
        else:
            status_message.error(f"❌ Error: {message}")
            progress_bar.progress(0)
    else:
        status_message.warning("⚠️ Please enter a YouTube URL")

# Footer
st.divider()
st.caption("Note: Videos are temporarily stored on server and deleted after download")
