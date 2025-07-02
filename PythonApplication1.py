import streamlit as st
import yt_dlp
import os
from urllib.parse import urlparse

# ======================
# 🛠️ Core Functions
# ======================

def download_media(url, platform):
    try:
        if platform == "youtube":
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_%(title)s.%(ext)s',
                'quiet': True,
                'extract_flat': False,
                'force_generic_extractor': True,
                'retries': 3,
                'socket_timeout': 30,
            }
        elif platform == "instagram":
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_%(id)s.%(ext)s',
                'quiet': True,
                'extract_flat': False,
                'force_generic_extractor': True,
                'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'extractor_args': {'instagram': {'skip_auth': True}},
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if not os.path.exists(filename):
                return False, "Download failed (file not found)"
            
            return True, filename

    except Exception as e:
        return False, str(e)

# ======================
# 🔍 URL Validation
# ======================

def is_youtube(url):
    domains = ['youtube.com', 'youtu.be']
    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in domains)

def is_instagram(url):
    domains = ['instagram.com']
    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in domains) and '/reel/' in url

# ======================
# 🎨 Streamlit UI
# ======================

st.set_page_config(
    page_title="Universal Video Downloader",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Universal Video Downloader")
st.markdown("Download YouTube Videos/Shorts and Instagram Reels in one click!")

# ===== 📥 DOWNLOAD DIALOG BOXES ===== #
yt_tab, insta_tab = st.tabs(["YouTube Downloader", "Instagram Downloader"])

# YouTube Downloader
with yt_tab:
    st.subheader("YouTube Video/Shorts")
    yt_url = st.text_input("Enter YouTube URL:", placeholder="https://youtube.com/watch?v=...")
    
    if st.button("Download YouTube Video", key="yt_btn"):
        if yt_url and is_youtube(yt_url):
            with st.spinner("Downloading..."):
                success, result = download_media(yt_url, "youtube")
                if success:
                    with open(result, "rb") as f:
                        st.download_button(
                            "💾 Save Video", 
                            data=f,
                            file_name=os.path.basename(result),
                            mime="video/mp4"
                        )
                    os.remove(result)
                else:
                    st.error(f"❌ Error: {result}")
        else:
            st.warning("⚠️ Please enter a valid YouTube URL")

# Instagram Downloader
with insta_tab:
    st.subheader("Instagram Reels")
    insta_url = st.text_input("Enter Instagram Reel URL:", placeholder="https://instagram.com/reel/...")
    
    if os.path.exists('cookies.txt'):
        st.success("🔑 Cookies detected (private accounts supported)")
    else:
        st.warning("ℹ️ Only public reels work without cookies.txt")
    
    if st.button("Download Instagram Reel", key="ig_btn"):
        if insta_url and is_instagram(insta_url):
            with st.spinner("Downloading..."):
                success, result = download_media(insta_url, "instagram")
                if success:
                    with open(result, "rb") as f:
                        st.download_button(
                            "💾 Save Reel",
                            data=f,
                            file_name=os.path.basename(result),
                            mime="video/mp4"
                        )
                    os.remove(result)
                else:
                    st.error(f"❌ Error: {result}")
        else:
            st.warning("⚠️ Please enter a valid Instagram Reel URL")

# ======================
# 📝 Instructions
# ======================
st.divider()
st.markdown("""
### **How to Use:**
1. **For YouTube**: Paste any video/shorts link  
   *(Example: `https://youtube.com/shorts/ABC123`)*  

2. **For Instagram**:  
   - Works for **public reels**  
   - For **private accounts**, add a `cookies.txt` file  
   *(Get cookies using browser extensions like "Get cookies.txt")*  

### **Why Downloads Fail?**
- ⏳ Instagram rate limits (wait 5-10 mins)  
- 🔒 Private account (requires cookies)  
- ❌ Invalid URL format  
""")
