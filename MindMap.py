import streamlit as st

# 1. Page Config
st.set_page_config(page_title="MindMap | Neural Workspace", layout="wide")

# 2. Futuristic CSS (No Emojis)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020c1b 100%);
        color: #e6f1ff;
    }

    /* Animated Blobs */
    .blob {
        position: fixed;
        width: 400px;
        height: 400px;
        background: linear-gradient(135deg, #64ffda22 0%, #48cae422 100%);
        filter: blur(100px);
        border-radius: 50%;
        z-index: -1;
        animation: float 25s infinite alternate ease-in-out;
    }
    
    @keyframes float {
        0% { transform: translate(-5%, -5%) scale(1); }
        100% { transform: translate(10%, 15%) scale(1.1); }
    }

    /* Hero Section */
    .hero-text {
        font-size: 5rem !important;
        font-weight: 800;
        text-align: center;
        letter-spacing: -2px;
        background: -webkit-linear-gradient(#ffffff, #64ffda);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 5rem;
    }

    .slogan {
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #8892b0;
        margin-bottom: 4rem;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        padding: 50px;
        margin-top: 20px;
    }

    /* Refined Button */
    div.stButton > button {
        width: 100%;
        background: transparent;
        color: #64ffda !important;
        border: 1px solid #64ffda;
        padding: 18px;
        border-radius: 2px;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: 0.4s all;
    }
    
    div.stButton > button:hover {
        background: rgba(100, 255, 218, 0.1);
        border: 1px solid #ffffff;
        color: #ffffff !important;
        box-shadow: 0 0 30px rgba(100, 255, 218, 0.2);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        color: #8892b0;
    }

    .stTabs [aria-selected="true"] {
        color: #64ffda !important;
    }
    </style>
    
    <div class="blob" style="top: -10%; left: -10%;"></div>
    <div class="blob" style="bottom: -10%; right: -10%; animation-delay: -7s;"></div>
    """, unsafe_allow_html=True)

# 3. Application Flow
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- PAGE 1: LANDING ---
if st.session_state.page == 'landing':
    st.markdown('<h1 class="hero-text">MINDMAP</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">The visual workspace where ideas come to life.</p>', unsafe_allow_html=True)
    
    # Empty space for scroll effect
    st.write("##")
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("Start Your Learning Journey"):
            st.session_state.page = 'auth'
            st.rerun()

    # Detailed Descriptions (The "Scroll Down" content)
    st.write("##")
    st.write("##")
    st.markdown("---")
    
    desc_col1, desc_col2 = st.columns(2)
    with desc_col1:
        st.markdown("### Structural Intelligence")
        st.write("Transform fragmented thoughts into a cohesive neural network. Our engine maps relationships between concepts automatically, allowing for non-linear knowledge acquisition.")
    
    with desc_col2:
        st.markdown("### Cognitive Synchrony")
        st.write("Collaborate within a shared mental model. Real-time updates ensure that every contributor stays aligned with the evolving architecture of the project.")

# --- PAGE 2: AUTHENTICATION ---
elif st.session_state.page == 'auth':
    # Back button at top left
    if st.button("Back"):
        st.session_state.page = 'landing'
        st.rerun()

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; letter-spacing: 2px;'>SYSTEM ACCESS</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            st.text_input("User Identification")
            st.text_input("Security Key", type="password")
            if st.button("Initialize Session"):
                st.success("Authorization successful.")
                
        with tab2:
            st.text_input("Full Legal Name")
            st.text_input("Email Address")
            st.text_input("New Security Key", type="password")
            st.text_input("Confirm Security Key", type="password")
            if st.button("Create Account"):
                st.toast("Profile synchronized.")
        
        st.markdown('</div>', unsafe_allow_html=True)