import streamlit as st
import requests
import json

# ------------------- CONFIG -------------------
API_URL = "https://dr6lm91ibb.execute-api.us-east-1.amazonaws.com/mood"  # Replace with your API Gateway URL
LOGO_URL = "https://pbs.twimg.com/profile_images/1615289734917689344/G5TDhGl2_400x400.jpg"

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
if "selfie" not in st.session_state:
    st.session_state.selfie = None

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #ff0000, #ff6600, #ffcc00);
    font-family: 'Arial', sans-serif;
    color: white;
    text-align: center;
}

/* Title */
.title {
    text-align: center;
    font-size: 3.5em;
    margin: 20px 0 40px 0;
    color: white;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
}

/* Emoji grid */
.emoji-grid {
    display: flex;
    justify-content: center;
    gap: 80px;
    margin: 40px auto;
}
.emoji-btn {
    font-size: 150px;
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s;
}
.emoji-btn:hover {
    transform: scale(1.3);
}

/* Reply Box */
.reply-box {
    background: black;
    color: white;
    text-align: center;
    padding: 25px;
    font-size: 20px;
    border-radius: 15px;
    margin: 20px auto;
    width: 70%;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

/* Center Inputs */
textarea, input, .stButton > button {
    margin: auto;
    display: block;
    background-color: black !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Hide top menu and footer */
header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------- PAGES -------------------

# Home Page
if st.session_state.page == "home":
    st.image(LOGO_URL, width=120)
    st.markdown('<h1 class="title">🌟 Your Mood Companion 🌈</h1>', unsafe_allow_html=True)

    if st.button("🚀 What’s Your Mood Today?"):
        st.session_state.page = "emotion_selection"
        st.rerun()

# Emotion Selection Page
elif st.session_state.page == "emotion_selection":
    st.image(LOGO_URL, width=120)
    st.markdown('<h1 class="title">🌟 What\'s Your Mood Today? 🌈</h1>', unsafe_allow_html=True)

    st.markdown('<div class="emoji-grid">', unsafe_allow_html=True)
    if st.button("😡", key="angry_btn"): st.session_state.current_emotion = "angry"; st.session_state.page = "emotion_console"; st.rerun()
    if st.button("😢", key="sad_btn"): st.session_state.current_emotion = "sad"; st.session_state.page = "emotion_console"; st.rerun()
    if st.button("😀", key="happy_btn"): st.session_state.current_emotion = "happy"; st.session_state.page = "emotion_console"; st.rerun()
    if st.button("😨", key="fear_btn"): st.session_state.current_emotion = "fear"; st.session_state.page = "emotion_console"; st.rerun()
    if st.button("😖", key="disgust_btn"): st.session_state.current_emotion = "disgust"; st.session_state.page = "emotion_console"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Emotion Console Page
elif st.session_state.page == "emotion_console":
    emotion = st.session_state.current_emotion
    st.image(LOGO_URL, width=120)
    st.markdown(f'<h1 class="title">🌟 {emotion.capitalize()} Console 🌈</h1>', unsafe_allow_html=True)

    # Different flows for each emotion
    if emotion == "happy":
        st.write("✨ You look glowing today! Want to share your smile? Upload a selfie 😍")
        uploaded = st.file_uploader("Click/Upload your Happy Selfie 📸", type=["jpg", "jpeg", "png"])
        if uploaded:
            st.session_state.selfie = uploaded
            col1, col2 = st.columns([1,1])
            with col1:
                st.image(uploaded, width=250, caption="Your Happy Selfie 😊")
            with col2:
                st.markdown('<div class="reply-box">Yay! That smile made my day! 🌟 Keep shining 🌈</div>', unsafe_allow_html=True)

    elif emotion == "angry":
        user_story = st.text_area("😡 I sense anger. Tell me what happened:")
        if st.button("💬 Share"):
            payload = {"user_id": st.session_state.user_id, "emotion": "angry", "text_input": user_story}
            try:
                response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()
                    reply = json.loads(data["body"]).get("bot_message", "I hear you.")
                    st.markdown(f'<div class="reply-box">{reply}</div>', unsafe_allow_html=True)
            except:
                st.error("API not reachable")

    elif emotion == "sad":
        st.write("😢 Feeling low? Want me to suggest something cheerful?")
        if st.button("🎶 Yes, play me something"):
            st.markdown('<div class="reply-box">🎵 How about some uplifting music? Try listening to ‘Happy – Pharrell Williams’ 💛</div>', unsafe_allow_html=True)

    elif emotion == "fear":
        fear_input = st.text_area("😨 What’s worrying you?")
        if st.button("💬 Share"):
            st.markdown('<div class="reply-box">You are safe 💙 Try some deep breathing 🌬️</div>', unsafe_allow_html=True)

    elif emotion == "disgust":
        disgust_input = st.text_area("😖 What’s making you uncomfortable?")
        if st.button("💬 Share"):
            st.markdown('<div class="reply-box">😌 Sometimes stepping away helps. Want me to suggest a calming activity?</div>', unsafe_allow_html=True)

    if st.button("✅ Now, is your mood okay?"):
        st.session_state.page = "closing"
        st.rerun()

# Closing Page
elif st.session_state.page == "closing":
    st.image(LOGO_URL, width=120)
    st.markdown('<h1 class="title">🌟 Session Complete 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<div class="reply-box">Thanks for sharing your feelings today 💙</div>', unsafe_allow_html=True)
    st.markdown('<div class="reply-box">💡 Quote: "Every storm runs out of rain 🌦️"</div>', unsafe_allow_html=True)

    if st.button("🚀 Start New Session"):
        st.session_state.page = "home"
        st.session_state.bot_reply = None
        st.session_state.current_emotion = None
        st.session_state.selfie = None
        st.rerun()

