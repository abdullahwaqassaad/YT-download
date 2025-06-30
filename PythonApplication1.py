import streamlit as st
import yt_dlp
import os
from urllib.parse import urlparse

def download_instagram_reel(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'reel_%(id)s.%(ext)s',
            'quiet': True,
            'extract_flat': False,
            'force_generic_extractor': True,
            'cookiefile': 'cookies.txt',  # Optional for private accounts
            'ignoreerrors': False,
            'retries': 3,
            'socket_timeout': 30,
            'extractor_args': {
                'instagram': {
                    'skip_auth': True,
                    'extract_reels': True
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            
            if not info_dict:
                return False, "Failed to extract video information"
                
            # Handle different possible filename scenarios
            filename = ydl.prepare_filename(info_dict)
            if not os.path.exists(filename):
                # Try alternative filename pattern
                filename = f"reel_{info_dict.get('id', 'unknown')}.mp4"
                
            if os.path.exists(filename):
                return True, filename
            else:
                return False, "File downloaded but not found"
                
    except Exception as e:
        return False, str(e)

def is_instagram_reel(url):
    parsed = urlparse(url)
    return (parsed.netloc in ['www.instagram.com', 'instagram.com'] and
            '/reel/' in parsed.path)

# Streamlit UI for Instagram
st.title("Instagram Reels Downloader")
url = st.text_input("Enter Instagram Reel URL:", placeholder="https://www.instagram.com/reel/...")

if st.button("Download Reel"):
    if url:
        if not is_instagram_reel(url):
            st.error("Please enter a valid Instagram Reel URL")
        else:
            with st.spinner("Downloading Reel..."):
                success, result = download_instagram_reel(url)
                
                if success:
                    st.success("✅ Reel downloaded successfully!")
                    with open(result, "rb") as f:
                        st.download_button(
                            label="Save Reel",
                            data=f,
                            file_name=os.path.basename(result),
                            mime="video/mp4"
                        )
                    os.remove(result)  # Clean up
                else:
                    st.error(f"❌ Error: {result}")
    else:
        st.warning("Please enter a Reel URL")

st.markdown("""
**Note:**
- Works with public Reels only (unless you provide cookies)
- If downloads fail, try adding a cookies.txt file
""")
