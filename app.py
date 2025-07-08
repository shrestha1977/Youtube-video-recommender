import streamlit as st
from googleapiclient.discovery import build

# --- CONFIG ---
API_KEY = "AIzaSyC61OdgBAQdDjP-zK0we9Uw71ElG2VF6yw"  
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# --- FUNCTION TO SEARCH YOUTUBE VIDEOS ---
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

# --- PAGE CONFIG ---
st.set_page_config(page_title="🎥 YouTube Video Recommender", layout="wide")

# --- HEADER ---
st.title("🎬 YouTube Video Recommender")
st.markdown("Type a topic or select a category below to explore top YouTube videos.")

# --- CATEGORY OR CUSTOM TOPIC ---
categories = ["🎓 Education", "🧠 Tech", "🎮 Gaming", "🎨 Design", "🎶 Music", "🌍 Travel", "🆓 Custom"]
category = st.selectbox("Choose a category or select 'Custom' to enter your own topic", categories)

# --- CUSTOM INPUT ---
if category == "🆓 Custom":
    topic = st.text_input("🔍 Enter your own topic:")
else:
    topic = category.split(" ", 1)[1]  # Extract text after emoji

# --- SEARCH AND DISPLAY VIDEOS ---
if topic:
    with st.spinner("🔎 Searching YouTube..."):
        try:
            videos = search_youtube_videos(topic)
            if videos:
                for video in videos:
                    title = video["snippet"]["title"]
                    channel = video["snippet"]["channelTitle"]
                    video_id = video["id"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"

                    st.markdown(f"### 📺 {title}")
                    st.write(f"🧑‍🏫 Channel: {channel}")
                    st.video(video_url)
                    st.markdown("---")
            else:
                st.warning("No results found. Try a different topic.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
