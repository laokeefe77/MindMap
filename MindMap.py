import streamlit as st

# 1. Page Config
st.set_page_config(page_title="MindMap | Deep Space", layout="wide")

# 2. Starfield & Nebula CSS
st.markdown("""
    <style>
    /* Main Universe Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        color: #ffffff;
        overflow-x: hidden;
    }

    /* Star Layers */
    .stars-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: transparent;
    }

    /* Creating Stars using box-shadow shadows (Performance efficient) */
    .stars {
        width: 1px;
        height: 1px;
        background: transparent;
        box-shadow: 1744px 162px #FFF , 134px 1317px #FFF , 56px 1057px #FFF , 1041px 1858px #FFF , 183px 1851px #FFF , 1574px 1279px #FFF , 1431px 188px #FFF , 1515px 1289px #FFF , 1271px 1358px #FFF , 121px 105px #FFF;
        /* Note: In a real CSS file we'd generate 100s of these. I'll simulate with a repeating pattern */
        animation: twinkle 8s infinite;
    }

    /* The Nebula Bulb (Space Cloud) */
    .nebula {
        position: fixed;
        width: 800px;
        height: 800px;
        background: radial-gradient(circle, rgba(100, 255, 218, 0.05) 0%, rgba(0, 119, 182, 0.05) 50%, transparent 100%);
        filter: blur(100px);
        border-radius: 50%;
        z-index: -1;
        top: -20%;
        right: -10%;
        animation: drift 30s infinite alternate ease-in-out;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 0.3; }
    }

    @keyframes drift {
        from { transform: translate(0, 0); }
        to { transform: translate(-100px, 100px); }
    }

    /* Typography */
    .hero-text {
        font-size: clamp(4rem, 12vw, 8rem) !important;
        font-weight: 900;
        text-align: center;
        letter-spacing: 15px;
        background: linear-gradient(to bottom, #ffffff 30%, #64ffda 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-top: 15vh;
        margin-bottom: 0;
    }

    .slogan {
        text-align: center;
        font-size: 1rem;
        letter-spacing: 8px;
        text-transform: uppercase;
        color: #8892b0;
        opacity: 0.8;
    }

    /* Glass Panels */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0px;
        padding: 40px;
        margin-top: 20px;
        transition: 0.3s;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(100, 255, 218, 0.3);
    }

    /* Interactive Inputs */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    /* Button */
    div.stButton > button {
        width: 100%;
        background: transparent;
        color: #ffffff !important;
        border: 1px solid #ffffff;
        padding: 20px;
        text-transform: uppercase;
        letter-spacing: 3px;
        transition: 0.5s;
    }
    div.stButton > button:hover {
        background: #ffffff;
        color: #000000 !important;
        box-shadow: 0 0 50px rgba(255, 255, 255, 0.2);
    }
    </style>

    <div class="stars-container">
        <div class="stars"></div>
        <div class="nebula"></div>
    </div>
    """, unsafe_allow_html=True)

# 3. Content Flow
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.markdown('<h1 class="hero-text">MINDMApppP</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Navigating the infinite expanse of thought.</p>', unsafe_allow_html=True)
    
    st.write("##")
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Start Your Learning Journey"):
            st.session_state.page = 'auth'
            st.rerun()

    # Dynamic Descriptions (revealed on scroll)
    st.write("##")
    st.write("##")
    st.write("##")
    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="glass-card">
            <h3 style="letter-spacing: 2px;">Orbital Organization</h3>
            <p style="color: #8892b0;">Your data points aren't just entries; they are nodes in a constellation. Experience a workspace that mimics the natural clustering of the universe.</p>
        </div>""", unsafe_allow_html=True)
    
    with c2:
        st.markdown("""<div class="glass-card">
            <h3 style="letter-spacing: 2px;">Deep Discovery</h3>
            <p style="color: #8892b0;">Navigate through layers of complexity with fluid transitions. Our engine handles massive datasets with the grace of a silent orbit.</p>
        </div>""", unsafe_allow_html=True)

# --- AUTHENTICATION PAGE ---
elif st.session_state.page == 'auth':
    if st.button("Return to Void"):
        st.session_state.page = 'landing'
        st.rerun()

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; letter-spacing: 5px;'>PROTOCOL</h2>", unsafe_allow_html=True)
        
        tab_in, tab_up = st.tabs(["Initialize Session", "New Sequence"])
        
        with tab_in:
            st.text_input("User Key")
            st.text_input("Passcode", type="password")
            st.button("Authenticate")
            
        with tab_up:
            st.text_input("Assigned Name")
            st.text_input("Registry Email")
            st.text_input("New Passcode", type="password")
            st.button("Register Identity")
            
        st.markdown('</div>', unsafe_allow_html=True)