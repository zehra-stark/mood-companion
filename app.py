import streamlit as st
import requests
import json
from datetime import datetime

# ------------------- CONFIG -------------------
API_URL = "https://dr6lm91ibb.execute-api.us-east-1.amazonaws.com/mood"  # Replace with your API Gateway URL

st.set_page_config(page_title="🌟 Your Mood Companion 🌈", layout="wide", page_icon="🌟")

# ------------------- SESSION STATE -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_id" not in st.session_state:
    st.session_state.user_id = "Whiz-User"
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = None
if "bot_reply" not in st.session_state:
    st.session_state.bot_reply = None

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff, #ff6666, #ff9900);
    font-family: 'Arial', sans-serif;
    color: white;
}

/* Title */
.title {
    text-align: center;
    font-size: 3.5em;
    margin-bottom: 0.5em;
    color: white;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
}

/* Emoji grid */
.emoji-grid {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin: 40px 0;
}
.emoji-btn {
    font-size: 120px;
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s;
}
.emoji-btn:hover {
    transform: scale(1.3);
}

/* Reply box */
.reply-box {
    background: black;
    color: white;
    text-align: center;
    padding: 20px;
    font-size: 20px;
    border-radius: 15px;
    margin: 20px auto;
    width: 70%;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

/* Text areas & inputs */
textarea, input, .stButton > button {
    background-color: black !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Footer */
.footer {
    text-align: center;
    color: white;
    font-size: 18px;
    margin-top: 80px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- PAGES -------------------
# Home Page
if st.session_state.page == "home":
    st.markdown('<h1 class="title">🌟 Your Mood Companion 🌈</h1>', unsafe_allow_html=True)
    if st.button("🚀 What’s Your Mood Today?"):
        st.session_state.page = "emotion_selection"
        st.rerun()

# Emotion Selection Page
elif st.session_state.page == "emotion_selection":
    st.markdown('<h1 class="title">🌟 What\'s Your Mood Today? 🌈</h1>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("😡", key="angry_btn"): st.session_state.current_emotion = "angry"; st.session_state.page = "emotion_console"; st.rerun()
    with col2:
        if st.button("😢", key="sad_btn"): st.session_state.current_emotion = "sad"; st.session_state.page = "emotion_console"; st.rerun()
    with col3:
        if st.button("😀", key="happy_btn"): st.session_state.current_emotion = "happy"; st.session_state.page = "emotion_console"; st.rerun()
    with col4:
        if st.button("😨", key="fear_btn"): st.session_state.current_emotion = "fear"; st.session_state.page = "emotion_console"; st.rerun()
    with col5:
        if st.button("😖", key="disgust_btn"): st.session_state.current_emotion = "disgust"; st.session_state.page = "emotion_console"; st.rerun()

# Emotion Console Page
elif st.session_state.page == "emotion_console":
    emotion = st.session_state.current_emotion
    st.markdown(f'<h1 class="title">🌟 {emotion.capitalize()} Console 🌈</h1>', unsafe_allow_html=True)

    user_text = st.text_area("Share your thoughts:", key="user_input")

    if st.button("💬 Submit"):
        payload = {"user_id": st.session_state.user_id, "emotion": emotion, "text_input": user_text}
        try:
            response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                data = response.json()
                if "body" in data:
                    result = json.loads(data["body"])
                else:
                    result = data
                st.session_state.bot_reply = result.get("reply", "No reply received.")
                st.balloons()
                st.markdown(f'<div class="reply-box">{st.session_state.bot_reply}</div>', unsafe_allow_html=True)
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to API: {str(e)}")

    if st.button("✅ Now, is your mood okay?"):
        st.session_state.page = "closing"
        st.rerun()

    if st.button("🔙 Back to Moods"):
        st.session_state.page = "emotion_selection"
        st.rerun()

# Closing Page
elif st.session_state.page == "closing":
    st.markdown('<h1 class="title">🌟 Session Complete 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<div class="closing-text">Thanks for sharing your feelings today 💙</div>', unsafe_allow_html=True)
    st.markdown('<div class="closing-text">💡 Quote: "Every storm runs out of rain 🌦️"</div>', unsafe_allow_html=True)

    if st.button("🚀 Start New Session"):
        st.session_state.page = "home"
        st.session_state.bot_reply = None
        st.session_state.current_emotion = None
        st.rerun()

# Footer (always bottom)
st.markdown('<div class="footer">Powered by Whizlabs Team ❤️</div>', unsafe_allow_html=True)

