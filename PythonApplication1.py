import streamlit as st
import yt_dlp
import os
from urllib.parse import urlparse

# ========== Common Download Functions ========== #
def download_media(url, platform):
    try:
        if platform == "youtube":
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'extract_flat': False,
                'force_generic_extractor': True,
                'ignoreerrors': True,
                'retries': 3,
                'socket_timeout': 30,
            }
        elif platform == "instagram":
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'extract_flat': False,
                'force_generic_extractor': True,
                'cookiefile': 'cookies.txt',  # Optional for private accounts
                'ignoreerrors': True,
                'retries': 3,
                'socket_timeout': 30,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            media_title = info_dict.get('title', 'video' if platform == "youtube" else 'reel')
            ext = info_dict.get('ext', 'mp4')
            filename = f"{media_title}.{ext}"
            return True, filename
    except Exception as e:
        return False, str(e)

# ========== Platform-Specific Checks ========== #
def is_youtube_url(url):
    parsed = urlparse(url)
    return (parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be'] and
            ('/watch?v=' in url or '/shorts/' in url))

def is_instagram_reel(url):
    parsed = urlparse(url)
    return (parsed.netloc in ['www.instagram.com', 'instagram.com'] and
            '/reel/' in parsed.path)

# ========== Streamlit UI ========== #
st.set_page_config(
    page_title="All-in-One Video Downloader",
    page_icon="🎬",
    layout="centered"
)

st.title("🎥 All-in-One Video Downloader")
st.caption("Download YouTube Videos/Shorts & Instagram Reels")

# Tab Selection
tab1, tab2 = st.tabs(["YouTube Downloader", "Instagram Reels Downloader"])

# ========== YOUTUBE TAB ========== #
with tab1:
    st.subheader("YouTube Video/Shorts Downloader")
    youtube_url = st.text_input(
        "Enter YouTube URL (Video or Short):",
        placeholder="https://www.youtube.com/watch?v=... or https://youtube.com/shorts/...",
        key="youtube_url"
    )

    if st.button("Download YouTube Video", key="yt_download"):
        if youtube_url:
            if not is_youtube_url(youtube_url):
                st.error("❌ Invalid YouTube URL. Must be a video or Short.")
            else:
                with st.spinner("Downloading..."):
                    success, filename = download_media(youtube_url, "youtube")
                    if success:
                        st.success(f"✅ Downloaded: {filename}")
                        if os.path.exists(filename):
                            with open(filename, "rb") as f:
                                st.download_button(
                                    label="Save Video",
                                    data=f,
                                    file_name=filename,
                                    mime="video/mp4"
                                )
                            os.remove(filename)  # Cleanup
                        else:
                            st.warning("File downloaded but not found.")
                    else:
                        st.error(f"❌ Error: {filename}")
        else:
            st.warning("⚠️ Please enter a YouTube URL.")

# ========== INSTAGRAM TAB ========== #
with tab2:
    st.subheader("Instagram Reels Downloader")
    instagram_url = st.text_input(
        "Enter Instagram Reel URL:",
        placeholder="https://www.instagram.com/reel/...",
        key="instagram_url"
    )

    if st.button("Download Instagram Reel", key="ig_download"):
        if instagram_url:
            if not is_instagram_reel(instagram_url):
                st.error("❌ Invalid Instagram Reel URL.")
            else:
                with st.spinner("Downloading Reel..."):
                    success, filename = download_media(instagram_url, "instagram")
                    if success:
                        st.success(f"✅ Downloaded: {filename}")
                        if os.path.exists(filename):
                            with open(filename, "rb") as f:
                                st.download_button(
                                    label="Save Reel",
                                    data=f,
                                    file_name=filename,
                                    mime="video/mp4"
                                )
                            os.remove(filename)  # Cleanup
                        else:
                            st.warning("File downloaded but not found.")
                    else:
                        st.error(f"❌ Error: {filename}")
        else:
            st.warning("⚠️ Please enter an Instagram Reel URL.")

# Footer
st.divider()
st.markdown("""
**Notes:**
- For **private Instagram accounts**, add a `cookies.txt` file.
- Downloads are **temporary** and deleted after saving.
- Supports **YouTube Videos, Shorts, and Instagram Reels**.
""")
