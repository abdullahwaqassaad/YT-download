import streamlit as st
import yt_dlp

def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return True, info_dict.get('title', 'video')
    except Exception as e:
        return False, str(e)

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', '0%')
        progress = progress.replace('%', '')
        try:
            progress_float = float(progress)
            progress_bar.progress(progress_float)
        except:
            pass

# Streamlit UI
st.title("YouTube Video Downloader")

url = st.text_input("Enter YouTube URL:")
progress_bar = st.progress(0)

if st.button("Download"):
    if url:
        st.write("Downloading...")
        success, message = download_video(url)
        if success:
            st.success(f"Successfully downloaded: {message}")
            progress_bar.progress(100)
        else:
            st.error(f"Error: {message}")
            progress_bar.progress(0)
    else:
        st.warning("Please enter a YouTube URL")
