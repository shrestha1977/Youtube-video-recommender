import streamlit as st
from googleapiclient.discovery import build

API_KEY = "AIzaSyC61OdgBAQdDjP-zK0we9Uw71ElG2VF6yw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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

st.set_page_config(page_title="🎥 Video Recommender", layout="wide")
st.title("🎬 YouTube Video Recommender")
st.markdown("Enter a topic and get top YouTube video recommendations.")

topic = st.text_input("🔍 Enter a topic")

if topic:
    with st.spinner("Searching YouTube..."):
        videos = search_youtube_videos(topic)
        for video in videos:
            title = video["snippet"]["title"]
            channel = video["snippet"]["channelTitle"]
            video_id = video["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            st.subheader(title)
            st.write(f"Channel: {channel}")
            st.write(f"[Watch on YouTube]({video_url})")
            st.video(video_url)
            st.markdown("---")
