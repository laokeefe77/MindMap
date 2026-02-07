import streamlit as st

# 1. Page Config
st.set_page_config(page_title="MindMap | Neural Workspace", layout="wide")

# 2. Advanced CSS for Dynamic Bulbs
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #020c1b;
        color: #e6f1ff;
        overflow-x: hidden;
    }

    /* Dynamic Bulb Container */
    .bg-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }

    .bulb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.4;
        animation: move 20s infinite alternate ease-in-out;
    }

    /* Different sizes and starting positions for the bulbs */
    .bulb-1 { width: 300px; height: 300px; background: #64ffda; top: 10%; left: 10%; animation-duration: 25s; }
    .bulb-2 { width: 450px; height: 450px; background: #48cae4; bottom: 5%; right: 15%; animation-duration: 30s; animation-delay: -5s; }
    .bulb-3 { width: 200px; height: 200px; background: #0077b6; top: 40%; left: 50%; animation-duration: 20s; animation-delay: -2s; }

    @keyframes move {
        0% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, 50px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
        100% { transform: translate(0, 0) scale(1); }
    }

    /* Typography & UI */
    .hero-text {
        font-size: clamp(3rem, 10vw, 6rem) !important;
        font-weight: 800;
        text-align: center;
        letter-spacing: -2px;
        background: linear-gradient(to bottom, #ffffff, #64ffda);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-top: 10vh;
    }

    .slogan {
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #8892b0;
        margin-bottom: 5vh;
    }

    /* Dynamic Description Cards */
    .desc-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-left: 2px solid #64ffda;
        padding: 25px;
        border-radius: 0 10px 10px 0;
        transition: 0.5s;
    }
    .desc-card:hover {
        background: rgba(100, 255, 218, 0.05);
        transform: translateX(10px);
    }

    /* Auth Card */
    .glass-card {
        background: rgba(10, 25, 47, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(100, 255, 218, 0.2);
        padding: 40px;
        border-radius: 15px;
    }

    /* Button Styling */
    div.stButton > button {
        width: 100%;
        background: transparent;
        color: #64ffda !important;
        border: 1px solid #64ffda;
        padding: 15px;
        font-size: 1rem;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: #64ffda;
        color: #020c1b !important;
    }
    </style>

    <div class="bg-container">
        <div class="bulb bulb-1"></div>
        <div class="bulb bulb-2"></div>
        <div class="bulb bulb-3"></div>
    </div>
    """, unsafe_allow_html=True)

# 3. App Logic
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.markdown('<h1 class="hero-text">MINDMAP</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Cognitive architecture for the next era.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Your Learning Journey"):
            st.session_state.page = 'auth'
            st.rerun()

    # Dynamic Description Section (Scroll down content)
    st.write("##")
    st.write("##")
    st.write("---")
    
    st.markdown("### System Specifications")
    d1, d2, d3 = st.columns(3)
    
    with d1:
        st.markdown("""<div class="desc-card">
            <h4>Neural Synthesis</h4>
            <p>Automatically bridges disparate data points into a cohesive mental framework.</p>
        </div>""", unsafe_allow_html=True)
    
    with d2:
        st.markdown("""<div class="desc-card">
            <h4>Real-time Logic</h4>
            <p>Collaborative mapping that updates across the network with zero latency.</p>
        </div>""", unsafe_allow_html=True)
        
    with d3:
        st.markdown("""<div class="desc-card">
            <h4>Visual Intelligence</h4>
            <p>Advanced spatial rendering of complex hierarchies and relationships.</p>
        </div>""", unsafe_allow_html=True)

# --- AUTHENTICATION PAGE ---
elif st.session_state.page == 'auth':
    if st.button("Back"):
        st.session_state.page = 'landing'
        st.rerun()

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>IDENTIFICATION</h2>", unsafe_allow_html=True)
        
        mode = st.radio("Select Action", ["Sign In", "Register"], label_visibility="collapsed")
        
        if mode == "Sign In":
            st.text_input("User ID")
            st.text_input("Access Code", type="password")
            st.button("Authorize Access")
        else:
            st.text_input("Name")
            st.text_input("Registration Email")
            st.text_input("New Access Code", type="password")
            st.button("Create Profile")
            
        st.markdown('</div>', unsafe_allow_html=True)