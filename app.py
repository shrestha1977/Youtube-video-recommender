import streamlit as st
from googleapiclient.discovery import build
from streamlit_lottie import st_lottie
import requests

# --- CONFIG ---
API_KEY = "AIzaSyC61OdgBAQdDjP-zK0we9Uw71ElG2VF6yw"  # Replace with your real API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# --- FUNCTION TO SEARCH VIDEOS ---
def search_youtube_videos(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=10,
        type="video"
    )
    response = request.execute()
    return response.get("items", [])

# --- LOAD LOTTIE ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_youtube = load_lottieurl("https://app.lottiefiles.com/share/cd8cd16e-b4fa-427b-b0fa-aacadf01b2f3")

# --- PAGE CONFIG ---
st.set_page_config(page_title="🎥 Video Recommender", layout="wide")

# --- UI HEADER ---
st_lottie(lottie_youtube, speed=1, height=250, key="intro")
st.title("🎬 YouTube Video Recommender")
st.markdown("✨ _Explore YouTube videos by category or custom search!_")

# --- CATEGORY SELECTOR ---
category = st.selectbox("📂 Choose a Category", [
    "📌 Choose", "🧠 Tech", "🩺 Health", "🎶 Music", "🎓 Education", 
    "🎨 Design", "🎮 Gaming", "🌍 Travel", "🆓 Custom Topic"
])

# --- CUSTOM TOPIC ---
if category == "🆓 Custom Topic":
    topic = st.text_input("🔍 Enter your own topic")
else:
    topic = category.split(" ", 1)[1] if category != "📌 Choose" else ""

# --- SEARCH BUTTON ---
if topic:
    with st.spinner("🔎 Searching YouTube..."):
        videos = search_youtube_videos(topic)
        if videos:
            for video in videos:
                title = video["snippet"]["title"]
                channel = video["snippet"]["channelTitle"]
                video_id = video["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                st.markdown("#### 📺 " + title)
                st.write(f"🧑‍🏫 **Channel:** {channel}")
                st.write(f"🔗 [Watch on YouTube]({video_url})")
                st.video(video_url)
                st.markdown("---")
        else:
            st.warning("No results found.")
