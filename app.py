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

# Custom CSS with Whizlabs Red Gradient
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FF4040, #FF6B6B);
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
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
        color: black;
    }
    .big-button {
        background: linear-gradient(45deg, #FF4040, #FF6B6B);
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
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        justify-items: center;
    }
    .emoji-btn {
        background: rgba(255,255,255,0.3);
        color: black;
        padding: 30px;
        font-size: 48px;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        transition: transform 0.2s, background 0.2s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .emoji-btn:hover {
        transform: scale(1.2);
        background: rgba(255,255,255,0.5);
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
        background: #FF4040;
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
        background: linear-gradient(45deg, #FF4040, #FF6B6B);
        border-radius: 50%;
        margin: 20px auto;
        animation: breathe 4s infinite;
    }
    .text-box {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #FF6B6B;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Home Page
if st.session_state.page == "home":
    st.markdown('<h1 class="title">🌟 Your Mood Companion 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI companion for emotional support (User ID: Whiz-User)</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Click Me!", key="start", help="Begin your mood journey!"):
            st.session_state.page = "emotion_selection"
            st.rerun()

# Emotion Selection Page
elif st.session_state.page == "emotion_selection":
    st.markdown('<h1 class="title">🌟 What\'s Your Mood Today? 🌈</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Click an emoji to express how you feel today</p>', unsafe_allow_html=True)
    html("""
    <div class="emoji-grid">
        <button class="emoji-btn" onclick="selectEmotion('angry')">😡</button>
        <button class="emoji-btn" onclick="selectEmotion('sad')">😢</button>
        <button class="emoji-btn" onclick="selectEmotion('happy')">😀</button>
        <button class="emoji-btn" onclick="selectEmotion('fear')">😨</button>
        <button class="emoji-btn" onclick="selectEmotion('disgust')">😖</button>
    </div>
    <script>
        function selectEmotion(emotion) {
            streamlit.setComponentValue(emotion);
        }
    </script>
    """, height=200)
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
            payload = {"user_id": "Whiz-User", "text_input": text_input}
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
                    st.write("Humor Chat: " + result["ai_response"])  # Use AI response as joke
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {str(e)}")
    else:
        if st.button("💬 Get Support", key="get_support"):
            payload = {"user_id": "Whiz-User", "emotion": emotion}
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

# Sidebar for History
st.sidebar.markdown('<h2>🌟 Your Journey 🌈</h2>', unsafe_allow_html=True)
if st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.sidebar.expander(f"Session #{i} - {entry['detected_emotion']}"):
            st.sidebar.write(f"**Bot:** {entry['bot_message'][:50]}...")
            st.sidebar.write(f"**AI:** {entry['ai_response'][:50]}...")
            st.sidebar.write(f"**Suggestion:** {entry['suggestion']}")
else:
    st.sidebar.info("No sessions yet. Start one!")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: black;">Powered by AWS Bedrock Nova Lite & Streamlit 💙</p>', unsafe_allow_html=True)
