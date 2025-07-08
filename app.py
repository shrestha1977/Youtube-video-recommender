import streamlit as st
from youtubesearchpython import VideosSearch

st.set_page_config(page_title="🎥 Video Recommender", layout="wide")

st.title("🎬 YouTube Video Recommender")
st.markdown("Enter a topic and get YouTube videos recommended instantly.")

topic = st.text_input("🔍 Enter a topic (e.g., Python tutorial, Machine Learning, SpaceX):")

if topic:
    with st.spinner("Searching YouTube..."):
        videosSearch = VideosSearch(topic, limit=10)
        results = videosSearch.result()["result"]

        for video in results:
            st.subheader(video['title'])
            st.write(f"Channel: {video['channel']['name']}")
            st.write(f"Duration: {video['duration']}")
            st.write(f"Views: {video['viewCount']['short']}")
            st.write(f"[Watch on YouTube]({video['link']})")
            st.video(video['link'])
            st.markdown("---")