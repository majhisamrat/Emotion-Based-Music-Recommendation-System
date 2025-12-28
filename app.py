import streamlit as st
from datetime import datetime

from inference.text_predict import predict_text_emotion
from inference.face_predict import predict_face_emotion
from recommendation.recommender import recommend_playlist_with_tracks

# SESSION STATE INITIALIZATION 

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# PAGE CONFIG (UNCHANGED)

st.set_page_config(
    page_title="Moodify - AI Music Recommender",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# CSS (UNCHANGED)

# CSS Styling

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    /* 1. DEFINING THE THEME 
       Default is Light Mode.
    */
    :root {
        --main-bg: #ffffff;
        --main-text: #1e293b;
        --card-bg: #f8fafc;
        --card-border: #e2e8f0;
        --card-shadow: rgba(0, 0, 0, 0.1);
        --input-bg: #ffffff;
        --input-border: #cbd5e1;
        --input-text: #1e293b;
        --sidebar-bg: #f1f5f9;
        --radio-bg: #e2e8f0;
        --radio-text: #334155;
        --radio-active-text: #0f172a;
    }

    /* 2. DARK MODE  */
    @media (prefers-color-scheme: dark) {
        :root {
            --main-bg: #0a0e27;
            --main-text: #ffffff;
            --card-bg: #1e293b; /* Dark card background */
            --card-border: #334155;
            --card-shadow: rgba(0, 0, 0, 0.3);
            --input-bg: #0f172a;
            --input-border: #334155;
            --input-text: #ffffff; /* White font for inputs in dark mode */
            --sidebar-bg: #0f172a;
            --radio-bg: #1e293b;
            --radio-text: #94a3b8;
            --radio-active-text: #ffffff;
        }
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* APPLICATION BACKGROUND  */
    .stApp {
        background: var(--main-bg);
        color: var(--main-text);
        transition: background 0.3s ease, color 0.3s ease;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Hero section  */
    .hero-section {
        text-align: center;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #ec4899 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.4);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white; /* Always white inside the colored hero box */
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #e0e7ff;
        font-weight: 300;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--main-text); /* Adapts to Black or White */
        margin-bottom: 1rem;
    }
    
    /* RADIO BUTTONS (Text Expression / Face Detection) */
    .stRadio > div {
        background: var(--radio-bg);
        padding: 0.4rem;
        border-radius: 50px;
        display: flex;
        gap: 0.3rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px var(--card-shadow);
    }
    
    .stRadio > div > label {
        color: var(--radio-text);
        padding: 0.7rem 1.5rem;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        flex: 1;
        text-align: center;
        font-weight: 600;
    }
    
    .stRadio > div > label:hover {
        background: rgba(124, 58, 237, 0.1);
        color: var(--main-text);
    }
    
    /* INPUT CARDS */
    .input-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 5px 20px var(--card-shadow);
        color: var(--main-text);
    }
    
    .input-card h3 {
        color: var(--main-text);
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .input-card p {
        color: var(--main-text);
        opacity: 0.8;
        font-size: 0.85rem;
    }
    
    /* TEXT AREA  */
    .stTextArea textarea {
        background: var(--input-bg) !important;
        border: 2px solid var(--input-border) !important;
        color: var(--input-text) !important; /* White in Dark Mode, Black in Light Mode */
        border-radius: 15px !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea label {
        color: var(--main-text) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2) !important;
    }
    
   /* Playlist header */
    .playlist-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        color: white;
    }
    
    .playlist-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #7c3aed, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .playlist-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .spotify-btn {
        display: inline-block;
        background: #1DB954;
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
    }
    
    .spotify-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.6);
    }
    
    /* Track cards  */
    .track-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 0;
        overflow: hidden;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .track-card:hover {
        transform: scale(1.03);
        border-color: #7c3aed;
        box-shadow: 0 5px 20px rgba(124, 58, 237, 0.5);
    }
    
    .track-card img {
        border-radius: 12px 12px 0 0;
    }
    
    .track-info {
        padding: 0.8rem;
        text-align: center;
    }
    
    .track-name {
        font-weight: 700;
        font-size: 0.85rem;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    
    .track-artist {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-bottom: 0.6rem;
    }
    
    .play-btn {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
        color: white;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .play-btn:hover {
        transform: scale(1.05);
    }
    
    /* Camera input */
    .stCamera {
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid #334155;
        background: #000;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #f8fafc; /* Changed to light gray to match white theme */
        border-right: 1px solid #e2e8f0;
    }
    
    .history-item {
        background: #ffffff;
        border-left: 3px solid #7c3aed;
        color: #1e293b; /* Dark text for history */
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .history-item:hover {
        background: #f1f5f9;
        transform: translateX(3px);
    }
    
    /* Section divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #7c3aed, transparent);
        margin: 2rem 0;
    }
    
    /* Compact emoji icons */
    .emoji-icon {
        font-size: 3rem;
        margin: 0.8rem 0;
        filter: drop-shadow(0 0 15px rgba(124, 58, 237, 0.6));
    }
    
    /* Stats badge */
    .stats-badge {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.3rem 0;
    }
    
    /* Tracks section title */
    .tracks-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b; /* Dark color for visibility */
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# EMOTION NORMALIZATION 

EMOTION_NORMALIZATION = {
    "sadness": "sad",
    "joy": "happy",
    "happiness": "happy",
    "anger": "angry",
    "fearful": "fear",
    "neutral": "calm"
}

# INTENT KEYWORDS

INTENT_KEYWORDS = {
    "motivate": "energy",
    "motivated": "energy",
    "motivation": "energy",
    "workout": "energy",
    "gym": "energy",
    "exercise": "energy",
    "study": "focus",
    "focus": "focus",
    "sleep": "calm",
    "relax": "calm",
    "calm": "calm"
}

INTENT_TO_EMOTION = {
    "energy": "happy",
    "focus": "calm",
    "calm": "calm"
}

def detect_intent(text):
    text = text.lower()
    for keyword, intent in INTENT_KEYWORDS.items():
        if keyword in text:
            return intent
    return None


# HERO SECTION

st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎵 Moodify</div>
    <div class="hero-subtitle">AI-powered music recommendations based on your emotions</div>
</div>
""", unsafe_allow_html=True)


# DISPLAY RESULT 

def display_result(result):
    if not result:
        st.warning("😔 No playlist found. Try a different emotion!")
        return

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="playlist-header">
        <div class="playlist-title">🎧 {result['playlist_name']}</div>
        <p class="playlist-subtitle">Curated just for your mood</p>
        <a href="{result['playlist_url']}" target="_blank" class="spotify-btn">
            ▶ Open in Spotify
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tracks-title">🎶 Featured Tracks</div>', unsafe_allow_html=True)

    tracks = result["tracks"]
    cols = st.columns(5)

    for i, track in enumerate(tracks):
        with cols[i % 5]:
            track_name = track['track_name'][:20] + "..." if len(track['track_name']) > 20 else track['track_name']
            artist_name = track['artist'][:18] + "..." if len(track['artist']) > 18 else track['artist']

            st.markdown(f"""
            <div class="track-card">
                <img src="{track.get('album_image', '')}" style="width: 100%;">
                <div class="track-info">
                    <div class="track-name">{track_name}</div>
                    <div class="track-artist">{artist_name}</div>
                    <a href="{track['track_url']}" target="_blank" class="play-btn">▶ Play</a>
                </div>
            </div>
            """, unsafe_allow_html=True)


# INPUT MODE SELECTION 
st.markdown('<div class="section-title">Choose How You Want to Express Yourself</div>', unsafe_allow_html=True)

option = st.radio(
    "",
    ["💬 Text Expression", "📸 Face Detection"],
    horizontal=True,
    label_visibility="collapsed"
)

# TEXT INPUT MODE (FIXED LOGIC)

if option == "💬 Text Expression":
    st.markdown('<div style="text-align:center;"><div class="emoji-icon">💭</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="input-card">
        <h3 style="text-align:center;color:#7c3aed;">Tell Us How You Feel</h3>
        <p style="text-align:center;color:#94a3b8;">Express your mood or what you need</p>
    </div>
    """, unsafe_allow_html=True)

    user_text = st.text_area(
        "",
        placeholder="e.g., 'I need motivation', 'feeling happy', 'workout songs'",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("🎵 Discover My Music", key="text_btn"):
        st.session_state.submitted = True

    
    if st.session_state.submitted:
        if not user_text or not user_text.strip():
            st.warning("⚠️ Please share your feelings!")
            st.session_state.submitted = False
            st.stop()

        with st.spinner("🎨 Analyzing..."):
            intent = detect_intent(user_text)

            if intent:
                final_emotion = INTENT_TO_EMOTION[intent]
                st.success(f"✨ Intent Detected: **{intent.upper()}** → Suggesting **CALM** playlist")
            else:
                emotion = predict_text_emotion(user_text)
                final_emotion = EMOTION_NORMALIZATION.get(emotion, emotion)
                st.success(f"🎭 Emotion detected: **{final_emotion.upper()}**")

            result = recommend_playlist_with_tracks(final_emotion)
            display_result(result)

            st.session_state.submitted = False

# FACE DETECTION MODE 

elif option == "📸 Face Detection":
    st.markdown('<div style="text-align:center;"><div class="emoji-icon">📷</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="input-card">
        <h3 style="text-align:center;color:#7c3aed;">Capture Your Expression</h3>
        <p style="text-align:center;color:#94a3b8;">Let AI read your emotions</p>
    </div>
    """, unsafe_allow_html=True)

    image = st.camera_input("", label_visibility="collapsed")

    if image:
        with st.spinner("🔍 Reading expression..."):
            emotion = predict_face_emotion(image)
            emotion = EMOTION_NORMALIZATION.get(emotion, emotion)

            st.success(f"🎭 Emotion: **{emotion.upper()}**")
            st.info(f"🎭 Mapped Emotion: **{emotion.upper()}**")

            result = recommend_playlist_with_tracks(emotion)
            display_result(result)

# FOOTER 

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#64748b;padding:1rem;font-size:0.85rem;">
🎵 Powered by ML • Spotify • Made with ❤️
</div>
""", unsafe_allow_html=True)
