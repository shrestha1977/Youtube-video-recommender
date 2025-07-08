import streamlit as st
from googleapiclient.discovery import build

# --- YOUTUBE API CONFIG ---
API_KEY = st.secrets["openai_api_key"]  
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# --- SEARCH FUNCTION ---
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
st.set_page_config(page_title="🎥 YouTube Recommender", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("🎯 Options")
search_mode = st.sidebar.radio("Search Mode", ["🔘 By Category", "🆓 Custom Search"])
categories = ["🎓 Education", "🧠 Tech", "🎮 Gaming", "🎨 Design", "🎶 Music", "🌍 Travel"]
st.sidebar.markdown("---")
st.sidebar.info("🎬 Top Videos at Your Fingertips — Just One Topic Away! 🔎\n🕵️‍♂️ AI-Powered Topic Search — Explore YouTube Smarter, Not Harder! 🤖")

# --- MAIN HEADER ---
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B; font-size: 3em;'>🎬 YouTube Video Recommender</h1>
    <p style='text-align: center; font-size: 1.2em; color: gray;'>Discover top YouTube videos by topic or category instantly.</p>
""", unsafe_allow_html=True)

# --- TOPIC INPUT ---
if search_mode == "🔘 By Category":
    selected_category = st.selectbox("📂 Select a Category", categories)
    topic = selected_category.split(" ", 1)[1]
else:
    topic = st.text_input("🔍 Enter a topic (e.g., Python, SpaceX, Meditation):")

# --- SEARCH BUTTON ---
search_clicked = st.button("🎥 Search Videos")

# --- RESULTS ---
if search_clicked and topic:
    with st.spinner("🔎 Fetching top YouTube videos..."):
        try:
            results = search_youtube_videos(topic)
            if results:
                st.success(f"✅ Showing results for: **{topic}**")
                for video in results:
                    title = video["snippet"]["title"]
                    channel = video["snippet"]["channelTitle"]
                    video_id = video["id"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    description = video["snippet"]["description"]

                    with st.expander(f"📺 {title} — by {channel}"):
                        st.write(f"🔗 [Watch on YouTube]({video_url})")
                        st.write(f"📝 {description if description else '_No description provided_'}")
                        st.video(video_url)
            else:
                st.warning("😕 No videos found. Try another topic.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- FOOTER ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 0.9em;'>Built with ❤️ using Streamlit + YouTube API</p>",
    unsafe_allow_html=True
)
