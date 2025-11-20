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
# 🚀 NO SPEEDING EFFECT - CONSTANT SLOW STARS
# --------------------------------------------------------

# Initialize states
if "processing" not in st.session_state:
    st.session_state.processing = False

# Generate random star positions radiating from center
import random
random.seed(42)

stars_html = ""
for i in range(150):
    angle = random.uniform(0, 360)
    distance = random.uniform(5, 45)
    
    import math
    center_x = 50 + distance * math.cos(math.radians(angle))
    center_y = 50 + distance * math.sin(math.radians(angle))
    
    delay = random.uniform(0, 8)
    size = random.choice([2, 3, 3, 4])
    
    stars_html += f'<div class="star" style="left: {center_x}%; top: {center_y}%; width: {size}px; height: {size}px; animation-delay: -{delay}s;"></div>\n'

st.markdown(
    f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Orbitron:wght@600;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
}}

/* CRITICAL: Lock all UI elements - NO FLICKERING */
header[data-testid="stHeader"],
.stApp > header,
[data-testid="stToolbar"] {{
    position: fixed !important;
    z-index: 999999 !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
}}

/* Lock main content */
.main .block-container,
.stMarkdown,
.stButton,
.stTextInput {{
    opacity: 1 !important;
    visibility: visible !important;
}}

.space-bg {{
    position: fixed;
    inset: 0;
    background: #000000;
    overflow: hidden;
    z-index: -5;
}}

.star-field {{
    position: fixed;
    width: 100%;
    height: 100%;
    perspective: 800px;
    transform-style: preserve-3d;
    z-index: -4;
}}

/* Base star - constant slow speed */
.star {{
    position: absolute;
    background: radial-gradient(circle, white 0%, rgba(255,255,255,0.9) 60%, transparent 100%);
    border-radius: 50%;
    box-shadow: 0 0 10px 3px rgba(255, 255, 255, 0.5);
    transform-origin: center center;
    animation: radialFlow 8s linear infinite;
}}

@keyframes radialFlow {{
    0% {{
        transform: translate(-50%, -50%) translateZ(-2000px) scale(0.05);
        opacity: 0;
    }}
    8% {{ opacity: 0.8; }}
    92% {{ opacity: 0.8; }}
    100% {{
        transform: translate(-50%, -50%) translateZ(500px) scale(5);
        opacity: 0;
    }}
}}

/* Gentle twinkle */
.star::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: white;
    border-radius: 50%;
    animation: twinkle 4s ease-in-out infinite;
}}

@keyframes twinkle {{
    0%, 100% {{ opacity: 0.3; }}
    50% {{ opacity: 1; }}
}}

.stApp {{
    background: transparent;
    color: #f8f9ff;
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 50px 50px;
    mix-blend-mode: screen;
    opacity: 0.15;
    pointer-events: none;
    z-index: -2;
}}

.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("https://grainy-gradients.vercel.app/noise.svg");
    opacity: 0.06;
    mix-blend-mode: soft-light;
    pointer-events: none;
    z-index: -1;
}}

.holo-bar {{
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
}}

.main-card {{
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
}}

.header-grid {{
    display: grid;
    grid-template-columns: auto 110px;
    gap: 18px;
    align-items: center;
}}

.big-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: conic-gradient(from 120deg, #00f5ff, #00ff87, #ff00f5, #00f5ff);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 22px rgba(0,255,255,0.65);
}}

.tagline {{
    font-size: 0.98rem;
    color: #f3e8ff;
    opacity: 0.86;
}}

.badge {{
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
}}

.scanline {{
    width: 100%;
    height: 2px;
    margin: 18px 0 18px 0;
    background: linear-gradient(90deg, transparent, #00ffe7, #ff00f5, transparent);
    opacity: 0.7;
}}

input[type="text"] {{
    padding: 14px 15px;
    border-radius: 14px !important;
    background: rgba(6, 4, 32, 0.96) !important;
    border: 1px solid rgba(117, 86, 255, 0.9) !important;
    color: #fdfcff !important;
    box-shadow: 0 0 15px rgba(117,86,255,0.65);
}}

input[type="text"]:focus {{
    border: 1px solid #00ffe7 !important;
    box-shadow: 0 0 26px rgba(0,255,231,0.8) !important;
}}

.stButton button {{
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
}}

.success-msg {{
    font-size: 1.3rem;
    font-weight: 800;
    text-align: center;
    margin-top: 26px;
    background: linear-gradient(90deg, #00ffe7, #8cffd4);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 18px rgba(0,255,222,0.7);
}}
</style>

<div class="space-bg">
  <div class="star-field">
    {stars_html}
  </div>
</div>

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

clicked = st.button(
    "🚀 GO AASTIK🤪! Have your SWASTIK 卐",
    key="go",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# Handle button click - NO RERUN NEEDED
if clicked and not st.session_state.processing:
    if slide_link.strip() == "":
        st.error("Bro... enter a slide link first 😑")
    elif N8N_WEBHOOK_URL == "":
        st.error("Webhook missing in Streamlit Secrets!")
    else:
        # Start processing WITHOUT rerun
        st.session_state.processing = True

# Processing happens directly
if st.session_state.processing:
    with st.spinner("Cooking your AI magic… 🍳🤖🔥☣️🚭"):
        payload = {"slides_url": slide_link}
        
        try:
            res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=2000)
            
            # Any response = success
            st.session_state.processing = False
            
            st.markdown(
                '<div class="success-msg">📽 Generation Successful! Go edit your pieces now 🔥</div>',
                unsafe_allow_html=True,
            )
            
            time.sleep(2)
            st.rerun()
                
        except requests.exceptions.Timeout:
            st.session_state.processing = False
            st.error("⏱️ Request timed out after 2000 seconds. Your workflow might still be running in n8n.")
            
        except requests.exceptions.ConnectionError:
            st.session_state.processing = False
            st.error("🔌 Cannot connect to n8n server. Please check if n8n is running and the webhook URL is correct.")
            
        except Exception as e:
            st.session_state.processing = False
            st.error(f"❌ Unexpected error: {str(e)}")
