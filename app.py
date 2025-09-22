import streamlit as st
import requests
import json
from streamlit.components.v1 import html
from datetime import datetime

# Configuration
API_URL = "https://dr6lm91ibb.execute-api.us-east-1.amazonaws.com/mood"  # Replace with your API Gateway URL
st.set_page_config(page_title="🌟 Your Mood Companion 🌈", layout="wide", page_icon="🌟")

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = None
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# Custom CSS with Refined Whizlabs Red Gradient
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FF3333, #FF6666);
        color: black;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: black;
    }
    .big-button {
        background: black;
        color: white;
        padding: 20px 40px;
        font-size: 24px;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        display: block;
        margin: 20px auto;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .big-button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    .emoji-grid {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 20px 0;
    }
    .emoji-btn {
        background: none;
        color: black;
        padding: 50px;
        font-size: 80px;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        transition: transform 0.2s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .emoji-btn:hover {
        transform: scale(1.2);
    }
    .console-section {
        background: rgba(255,255,255,0.2);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        backdrop-filter: blur(5px);
        color: black;
    }
    .closing-section {
        text-align: center;
        color: black;
        font-size: 24px;
        margin-top: 50px;
    }
    .back-btn {
        background: #FF3333;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        transition: background 0.3s;
    }
    .back-btn:hover {
        background: #FF5252;
    }
    .animation-container {
        text-align: center;
        margin: 20px 0;
        color: black;
    }
    @keyframes breathe {
        0% { transform: scale(1); }
        50% { transform: scale(1.5); }
        100% { transform: scale(1); }
    }
    .breathing-circle {
        width: 100px;
        height: 100px;
        background: linear-gradient(45deg, #FF3333, #FF6666);
        border-radius: 50%;
        margin: 20px auto;
        animation: breathe 4s infinite;
    }
    .text-box {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #FF6666;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Home Page
if st.session_state.page == "home":
    st.markdown('<h1 class="title">🌟 Your Mood Companion 🌈</h1>', unsafe_allow_html=True)
    st.session_state.user_id = st.text_input("Enter User ID (Default: Whiz-User)", value="Whiz-User", key="user_id_input")
    if st.button("🚀 Click Me!", key="start", help="Begin your mood journey!"):
        if st.session_state.user_id:
            st.session_state.page = "emotion_selection"
            st.rerun()
        else:
            st.error("Please enter a User ID.")

# Emotion Selection Page
elif st.session_state.page == "emotion_selection":
    st.markdown('<h1 class="title">🌟 What\'s Your Mood Today? 🌈</h1>', unsafe_allow_html=True)
    html("""
    <div class="emoji-grid">
        <button class="emoji-btn" onclick="window.parent.location='/run?emotion=angry'">😡</button>
        <button class="emoji-btn" onclick="window.parent.location='/run?emotion=sad'">😢</button>
        <button class="emoji-btn" onclick="window.parent.location='/run?emotion=happy'">😀</button>
        <button class="emoji-btn" onclick="window.parent.location='/run?emotion=fear'">😨</button>
        <button class="emoji-btn" onclick="window.parent.location='/run?emotion=disgust'">😖</button>
    </div>
    <script>
        // Redirect to next page with emotion parameter
        const urlParams = new URLSearchParams(window.location.search);
        const emotion = urlParams.get('emotion');
        if (emotion) {
            window.parent.streamlit_set_component_value(emotion);
        }
    </script>
    """, height=300)
    selected = st.session_state.get('selected_emotion')
    if selected:
        st.session_state.current_emotion = selected
        st.session_state.page = "emotion_console"
        st.rerun()

# Emotion Console Page
elif st.session_state.page == "emotion_console":
    emotion = st.session_state.current_emotion
    st.markdown(f'<h1 class="title">🌟 {emotion.capitalize()} Console 🌈</h1>', unsafe_allow_html=True)

    if emotion == "angry":
        text_input = st.text_area("What happened?", key="angry_input", class_="text-box")
        if st.button("Share", key="angry_share"):
            payload = {"user_id": st.session_state.user_id, "text_input": text_input}
            try:
                response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()["body"]
                    result = json.loads(data)
                    st.session_state.history.append(result)
                    st.markdown('<div class="console-section"><h3>🤖 Bot:</h3><p>{}</p></div>'.format(result["bot_message"]), unsafe_allow_html=True)
                    st.markdown('<div class="console-section"><h3>🧠 AI Response:</h3><p>{}</p></div>'.format(result["ai_response"]), unsafe_allow_html=True)
                    st.markdown('<h3>💡 Suggestions</h3>', unsafe_allow_html=True)
                    st.markdown('<div class="animation-container"><button onclick="startBreathing()">🧘 Breathing Exercise</button></div>', unsafe_allow_html=True)
                    st.write("Humor Chat: " + result["ai_response"])
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {str(e)}")
    else:
        if st.button("💬 Get Support", key="get_support"):
            payload = {"user_id": st.session_state.user_id, "emotion": emotion}
            try:
                response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()["body"]
                    result = json.loads(data)
                    st.session_state.history.append(result)
                    st.markdown('<div class="console-section"><h3>🤖 Bot:</h3><p>{}</p></div>'.format(result["bot_message"]), unsafe_allow_html=True)
                    st.markdown('<div class="console-section"><h3>🧠 AI Response:</h3><p>{}</p></div>'.format(result["ai_response"]), unsafe_allow_html=True)
                    st.markdown('<h3>💡 Suggestions</h3>', unsafe_allow_html=True)
                    if emotion == "sad":
                        st.write("Moral Story: " + result["ai_response"])
                        st.text_area("📝 Journal Prompt: Write your thoughts here...", height=100)
                    elif emotion == "happy":
                        st.write("Funny Poem/Rap: " + result["ai_response"])
                        st.write("📸 Take a fun selfie! (Upload via camera or file.)")
                    elif emotion == "fear":
                        st.write("Motivational Story: " + result["ai_response"])
                        st.markdown('<div class="animation-container"><button onclick="startMeditation()">🧘 Guided Meditation</button></div>', unsafe_allow_html=True)
                    elif emotion == "disgust":
                        st.write("Positive Reframe: " + result["ai_response"])
                        st.write("💕 Do one small kind act today!")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {str(e)}")

    # Breathing/Meditation Animation (JS)
    html("""
    <script>
        function startBreathing() {
            var circle = document.createElement('div');
            circle.className = 'breathing-circle';
            document.querySelector('.animation-container').appendChild(circle);
        }
        function startMeditation() {
            startBreathing();
        }
    </script>
    """, height=0)

    # Back Button
    if st.button("🔙 Back to Moods", key="back_emotions"):
        st.session_state.page = "emotion_selection"
        st.rerun()

# Closing Page
elif st.session_state.page == "closing":
    st.markdown('<h1 class="title">🌟 Session Complete 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<div class="closing-section">Thanks for sharing your feelings today 💙. See you again, bye bye 👋.</div>', unsafe_allow_html=True)
    if st.button("🚀 Start New Session", key="new_session"):
        st.session_state.page = "home"
        st.session_state.history = []
        st.session_state.current_emotion = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: black;">Powered by AWS Bedrock Nova Lite & Streamlit 💙</p>', unsafe_allow_html=True)
