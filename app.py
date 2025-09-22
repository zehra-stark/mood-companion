import streamlit as st
import requests
import json
from streamlit.components.v1 import html

# Configuration
API_URL = "https://dr6lm91ibb.execute-api.us-east-1.amazonaws.com/mood"  # Replace with your API Gateway URL
st.set_page_config(page_title="Your Mood Companion🤪", layout="centered")

# Session State for Navigation and History
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"

# Custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 24px;
            margin: 10px;
            cursor: pointer;
            border-radius: 12px;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #45a049;
        }
        .emoji-button {
            background-color: #ffeb3b;
            color: black;
            padding: 20px;
            font-size: 36px;
            margin: 10px;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .emoji-button:hover {
            transform: scale(1.1);
        }
        .console {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .closing {
            text-align: center;
            color: #2196F3;
            font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page
if st.session_state.page == "home":
    st.title("🌈 Mood Companion ✨")
    st.write("Welcome! Click below to start your mood journey.")
    if st.button("Start My Session", key="start_session", help="Begin your mood support session!"):
        st.session_state.page = "emotion_selection"

# Emotion Selection Page
elif st.session_state.page == "emotion_selection":
    st.title("🌈 Choose Your Mood ✨")
    st.write("Click an emoji to express how you feel!")
    cols = st.columns(5)
    emotions = ["😡 Angry", "😢 Sad", "😀 Happy", "😨 Fear", "😖 Disgust"]
    for i, (col, emotion) in enumerate(zip(cols, emotions)):
        if col.button(emotion, key=f"emotion_{i}", help=f"Select {emotion} mood"):
            st.session_state.current_emotion = emotion.split()[0]
            st.session_state.page = "emotion_console"

# Emotion Console Page
elif st.session_state.page == "emotion_console":
    emotion = st.session_state.current_emotion.lower()
    st.title(f"🌈 {emotion.capitalize()} Console ✨")

    # API Call
    if st.button("Get Support", key="get_support"):
        payload = {"user_id": st.session_state.user_id, "emotion": emotion}
        try:
            response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                data = response.json()["body"]
                result = json.loads(data)
                st.session_state.history.append(result)

                # Display Console
                st.markdown(f'<div class="console"><p><strong>Bot:</strong> {result["bot_message"]}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="console"><p><strong>AI Response:</strong> {result["ai_response"]}</p></div>', unsafe_allow_html=True)

                # Suggestions (HTML/CSS/JavaScript for animations and media)
                st.subheader("Suggestions")
                if emotion == "angry":
                    html("""
                        <button onclick="startBreathing()">Breathing Exercise</button>
                        <p>Joke: {result["ai_response"] if 'joke' in result else 'Loading...'}</p>
                        <audio controls><source src="https://www.youtube.com/watch?v=dQw4w9WgXcQ" type="audio/mp3"></audio>
                        <div id="breathing-circle" style="display:none; width: 100px; height: 100px; background: #4CAF50; border-radius: 50%; margin: 20px auto; animation: breathe 4s infinite;"></div>
                        <script>
                            function startBreathing() {{
                                var circle = document.getElementById('breathing-circle');
                                circle.style.display = 'block';
                            }}
                            @keyframes breathe {{
                                0% {{ transform: scale(1); }}
                                50% {{ transform: scale(1.5); }}
                                100% {{ transform: scale(1); }}
                            }}
                        </script>
                    """.format(result=result), height=200)
                elif emotion == "sad":
                    st.write(f"Moral Story: {result['ai_response']}")
                    html('<audio controls><source src="https://www.youtube.com/watch?v=abc123" type="audio/mp3"></audio>')
                    st.text_area("Journal Prompt: Write your thoughts here...", height=100)
                elif emotion == "happy":
                    st.write(f"Poem/Rap: {result['ai_response']}")
                    html('<audio controls><source src="https://www.youtube.com/watch?v=xyz789" type="audio/mp3"></audio>')
                    st.write("Take a selfie! (Upload to S3 via API later)")  # Placeholder for S3 integration
                elif emotion == "fear":
                    st.write(f"Motivational Story: {result['ai_response']}")
                    html('<audio controls><source src="https://www.youtube.com/watch?v=def456" type="audio/mp3"></audio>')
                    html("""
                        <button onclick="startBreathing()">Guided Meditation</button>
                        <div id="breathing-circle" style="display:none; width: 100px; height: 100px; background: #2196F3; border-radius: 50%; margin: 20px auto; animation: breathe 4s infinite;"></div>
                        <script>
                            function startBreathing() {{
                                var circle = document.getElementById('breathing-circle');
                                circle.style.display = 'block';
                            }}
                            @keyframes breathe {{
                                0% {{ transform: scale(1); }}
                                50% {{ transform: scale(1.5); }}
                                100% {{ transform: scale(1); }}
                            }}
                        </script>
                    """, height=200)
                elif emotion == "disgust":
                    st.write(f"Positive Reframe: {result['ai_response']}")
                    html('<audio controls><source src="https://www.youtube.com/watch?v=ghi789" type="audio/mp3"></audio>')
                    st.write("Suggestion: Do one small kind act today!")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to API: {str(e)}")

    # Back to Emotion Selection
    if st.button("Back to Emotions", key="back_to_emotions"):
        st.session_state.page = "emotion_selection"

# Closing Page
elif st.session_state.page == "closing":
    st.title("🌈 Closing ✨")
    st.markdown('<div class="closing">Thanks for sharing your feelings today 💙. See you again, bye bye 👋</div>', unsafe_allow_html=True)
    if st.button("Start New Session", key="new_session"):
        st.session_state.page = "home"
        st.session_state.history = []
        st.session_state.current_emotion = None

# History Sidebar
st.sidebar.title("🌈 Your History ✨")
if st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.sidebar.expander(f"Interaction #{i}"):
            st.write(f"**Bot Message:** {entry['bot_message']}")
            st.write(f"**AI Response:** {entry['ai_response']}")
            st.write(f"**Suggestion:** {entry['suggestion']}")
            st.write(f"**Emotion:** {entry['detected_emotion']}")
            st.write(f"**Approx. Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.sidebar.info("No history yet. Interact to save your journey!")

# User ID Input in Sidebar
st.session_state.user_id = st.sidebar.text_input("Your User ID:", value=st.session_state.user_id, help="Track your mood sessions.")
