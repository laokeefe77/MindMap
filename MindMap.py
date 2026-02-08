import streamlit as st
import random
import time

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="MindMap Noir",
    page_icon="🧠",
    layout="wide"
)

# --------------------
# Session State Initialization
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# --------------------
# Custom CSS: Sleek Modern Noir
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* Modern Depth Gradient Background */
        .stApp {
            background: radial-gradient(circle at top right, #1a1a1a, #000000);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Title Styling: Cutting White Lines */
        .main-title {
            text-align: center; 
            font-size: 80px; 
            font-weight: 900;
            margin-top: 60px; 
            letter-spacing: -2px;
            color: #ffffff;
            line-height: 1;
        }

        .subtitle {
            text-align: center; 
            font-size: 18px; 
            text-transform: uppercase;
            letter-spacing: 4px;
            opacity: 0.6; 
            margin-bottom: 50px;
        }

        /* Floating Element Logic */
        .bubble {
            position: fixed; 
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50%; 
            background: rgba(255, 255, 255, 0.03);
            animation: float 25s infinite linear;
            z-index: 0;
            pointer-events: none; /* Won't block clicks */
        }

        @keyframes float {
            0% { transform: translateY(110vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.3; }
            90% { opacity: 0.3; }
            100% { transform: translateY(-20vh) rotate(360deg); opacity: 0; }
        }

        /* Sleek Glassmorphism Card */
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 2px; /* Sharper corners for modern look */
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        /* Button: High Contrast White */
        .stButton > button {
            background: #ffffff;
            color: #000000 !important; 
            border: none; 
            padding: 14px 40px;
            font-weight: bold;
            border-radius: 0px; /* Sharp modern edges */
            transition: 0.4s cubic-bezier(0.19, 1, 0.22, 1);
            width: 100%;
        }

        .stButton > button:hover {
            background: #e0e0e0;
            transform: scale(1.02);
            letter-spacing: 1px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(0,0,0,0.5);
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_bubbles(n=12):
    # Only render if we aren't in a form to prevent 'ghost bubbles'
    html = "".join([
        f'<div class="bubble" style="'
        f'width:{random.randint(50,150)}px;'
        f'height:{random.randint(50,150)}px;'
        f'left:{random.randint(0,95)}vw;'
        f'animation-duration:{random.randint(20,40)}s;'
        f'animation-delay:{random.randint(0,15)}s;"></div>' 
        for _ in range(n)
    ])
    st.markdown(html, unsafe_allow_html=True)

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# Page Logic
# --------------------
def home_page():
    render_bubbles(10)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The Architecture of Learning</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        if st.button("ENTER WORKSPACE"):
            go_to("signup")

def signup_page():
    st.markdown("<h2 style='text-align:center; font-weight:200; letter-spacing:10px;'>IDENTITY</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("signup_form", border=False):
            st.text_input("FULL NAME")
            username = st.text_input("USERNAME")
            password = st.text_input("PASSWORD", type="password")
            submit = st.form_submit_button("CREATE ACCOUNT")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if username and password:
            st.session_state.user = {"name": username}
            st.success("AUTHENTICATED.")
            time.sleep(0.5)
            go_to("generator")

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    render_bubbles(5)
    
    with st.sidebar:
        st.markdown(f"### OPERATOR: {st.session_state.user['name'].upper()}")
        if st.button("TERMINATE SESSION"):
            st.session_state.user = None
            go_to("home")

    st.markdown("<h1 style='text-align:center; font-weight:800;'>GENERATOR</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT MATTER", placeholder="Enter topic...")
        depth = st.select_slider("DEPTH GRADIENT", options=["LINEAR", "EXPANDED", "COMPLEX"])
        
        if st.button("INITIATE ARCHITECTURE"):
            with st.spinner("PROCESSING NODES..."):
                time.sleep(2)
            st.success("STRUCTURE COMPLETE.")
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# App Router
# --------------------
def main():
    load_css()
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()