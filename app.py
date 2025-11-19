import streamlit as st
import requests
import time

st.set_page_config(
    page_title="AI Slide → Script Generator",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------------
# 👑 GOD MODE NEON UI + SPACESHIP BACKGROUND (ONLY CHANGE)
# --------------------------------------------------------
st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Orbitron:wght@600;800&display=swap');

/* Reset a bit */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* 🚀 Spaceship Universe Motion Background (ONLY THIS CHANGED) */
.space-bg {
    position: fixed;
    inset: 0;
    background-image: url("https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    z-index: -4;
    filter: brightness(0.55) saturate(1.2);
    animation: spaceDrift 40s ease-in-out infinite alternate;
}

@keyframes spaceDrift {
    0% { transform: scale(1.05) translate3d(0, 0, 0); }
    50% { transform: scale(1.10) translate3d(-15px, -10px, 0); }
    100% { transform: scale(1.15) translate3d(10px, 15px, 0); }
}

/* --- EVERYTHING BELOW IS EXACTLY SAME AS YOUR EXISTING CODE --- */

.stApp {
    background: radial-gradient(circle at 0% 0%, #2b0040 0, transparent 50%),
                radial-gradient(circle at 100% 0%, #003354 0, transparent 50%),
                radial-gradient(circle at 0% 100%, #390059 0, transparent 55%),
                radial-gradient(circle at 100% 100%, #003f3f 0, transparent 55%),
                linear-gradient(135deg, #050010, #020014, #050010);
    background-size: 200% 200%;
    animation: bgShift 18s ease-in-out infinite;
    color: #f8f9ff;
}

@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    mix-blend-mode: screen;
    opacity: 0.35;
    pointer-events: none;
    z-index: -2;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("https://grainy-gradients.vercel.app/noise.svg");
    opacity: 0.16;
    mix-blend-mode: soft-light;
    pointer-events: none;
    z-index: -1;
}

/* Floating hologram bar */
.holo-bar {
    position: fixed;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    padding: 4px 16px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(0,255,213,0.1), rgba(117,54,255,0.15));
    border: 1px solid rgba(0,255,213,0.4);
    box-shadow: 0 0 18px rgba(0,255,213,0.45);
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c6fffd;
    backdrop-filter: blur(16px);
    z-index: 999;
}

/* Main card */
.main-card {
    margin-top: 90px;
    padding: 32px 26px 30px 26px;
    border-radius: 28px;
    max-width: 780px;
    margin-left: auto;
    margin-right: auto;
    background: radial-gradient(circle at top left, rgba(0,255,235,0.2), transparent 55%),
                radial-gradient(circle at bottom right, rgba(255,0,140,0.24), transparent 55%),
                rgba(5, 5, 20, 0.86);
    border: 1px solid rgba(109, 46, 255, 0.8);
    box-shadow:
        0 0 45px rgba(0, 255, 255, 0.35),
        0 0 80px rgba(207, 0, 255, 0.35);
    backdrop-filter: blur(22px);
}

.header-grid {
    display: grid;
    grid-template-columns: auto 110px;
    gap: 18px;
    align-items: center;
}

.big-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: conic-gradient(from 120deg, #00f5ff, #00ff87, #ff00f5, #00f5ff);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 22px rgba(0,255,255,0.65);
}

/* Subtitle */
.tagline {
    font-size: 0.98rem;
    color: #f3e8ff;
    opacity: 0.86;
}

.badge {
    padding: 8px 10px;
    border-radius: 16px;
    text-align: center;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    border: 1px solid rgba(0,255,196,0.8);
    background: linear-gradient(135deg, rgba(0,255,196,0.18), rgba(98,0,234,0.35));
    color: #e4fffb;
    box-shadow: 0 0 18px rgba(0,255,196,0.7);
}

.scanline {
    width: 100%;
    height: 2px;
    margin: 18px 0 18px 0;
    background: linear-gradient(90deg, transparent, #00ffe7, #ff00f5, transparent);
    opacity: 0.7;
}

input[type="text"] {
    padding: 14px 15px;
    border-radius: 14px !important;
    background: rgba(6, 4, 32, 0.96) !important;
    border: 1px solid rgba(117, 86, 255, 0.9) !important;
    color: #fdfcff !important;
    box-shadow: 0 0 15px rgba(117,86,255,0.65);
}

input[type="text"]:focus {
    border: 1px solid #00ffe7 !important;
    box-shadow: 0 0 26px rgba(0,255,231,0.8) !important;
}

/* Button */
.stButton button {
    width: 100%;
    background: radial-gradient(circle at 20% 0%, #00ffe0, #00b3ff, #7b00ff);
    color: #040111 !important;
    padding: 16px 30px;
    border-radius: 999px;
    border: none;
    font-size: 1.2rem;
    font-weight: 900;
    box-shadow:
        0 0 18px rgba(0,255,255,0.7),
        0 0 36px rgba(121,0,255,0.7);
}

.success-msg {
    font-size: 1.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 26px;
    background: linear-gradient(90deg, #00ffe7, #8cffd4);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 18px rgba(0,255,222,0.7);
}
</style>

<div class="space-bg"></div>

<div class="holo-bar">AI VIDEO LAB · POWERED BY N8N & STREAMLIT</div>

<div class="main-card">
  <div class="header-grid">
    <div>
      <div class="big-title">🎬Stock Script Generator</div>
      <div class="tagline">Drop a Google Slide→ Let the 🤖AI chew it → Get video-ready script prompts</div>
    </div>
    <div class="badge">
      REAL-TIME<br/>👾<br/>AI ENGINE
    </div>
  </div>

  <div class="scanline"></div>
</div>
""",
    unsafe_allow_html=True,
)

# Reopen main-card container
st.markdown('<div class="main-card" style="margin-top:-30px;">', unsafe_allow_html=True)

slide_link = st.text_input(
    "",
    placeholder="Paste your Google Slides link here",
    key="input1",
)

N8N_WEBHOOK_URL = st.secrets.get(
    "N8N_WEBHOOK_URL",
    "https://reinventdigital12.app.n8n.cloud/webhook-test/3710637b-dc1b-4b19-b5e9-7a52f9d7780c",
)

if "clicked" not in st.session_state:
    st.session_state.clicked = False

clicked = st.button(
    "🚀 GO AASTIK🤪! Have your SWASTIK 卐",
    key="go",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)

if clicked:
    if slide_link.strip() == "":
        st.error("Bro... enter a slide link first 😑")

    elif N8N_WEBHOOK_URL == "":
        st.error("Webhook missing in Streamlit Secrets!")

    else:
        st.session_state.clicked = True

        with st.spinner("Cooking your AI magic… 🍳🤖🔥☣️🚭"):
            payload = {"slides_url": slide_link}

            try:
                res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=2000)

                if res.status_code == 200:
                    time.sleep(2)
                    st.markdown(
                        '<div class="success-msg">📽 Generation Successful! Go edit your pieces now 🔥</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("Workflow triggered but returned an error! Check n8n logs.")
            except Exception as e:
                st.error("Error connecting to n8n webhook: " + str(e))
