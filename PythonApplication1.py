import streamlit as st
import yt_dlp
import os

def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'quiet': True,  # Suppress console output
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
            progress_float = float(progress)
            progress_bar.progress(min(100, max(0, progress_float)))
        except ValueError:
            pass

# Streamlit UI
st.title("🎬 YouTube Video Downloader")

url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
progress_bar = st.progress(0)
status_message = st.empty()

if st.button("Download Video"):
    if url:
        status_message.info("Starting download...")
        progress_bar.progress(5)  # Show initial progress
        
        success, message = download_video(url)
        
        if success:
            status_message.success(f"✅ Download complete: {message}")
            progress_bar.progress(100)
            
            # Check if file exists and offer download
            if os.path.exists(message):
                with open(message, "rb") as file:
                    st.download_button(
                        label="Save Video",
                        data=file,
                        file_name=message,
                        mime="video/mp4"
                    )
            else:
                st.warning("File was downloaded but cannot be found.")
        else:
            status_message.error(f"❌ Error: {message}")
            progress_bar.progress(0)
    else:
        status_message.warning("⚠️ Please enter a YouTube URL")
