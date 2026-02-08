import streamlit as st
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
# Session State
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# --------------------
# Custom CSS: Bottom-Left (Black) to Top-Right (White)
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* 1. AGGRESSIVE GRADIENT: Black (Bottom-Left) to White (Top-Right) */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(45deg, #000000 25%, rgba(255,255,255,0.6) 100%),
                /* Thicker, more visible floor lines (2px) */
                linear-gradient(rgba(255,255,255,0.15) 2px, transparent 2px),
                linear-gradient(90deg, rgba(255,255,255,0.15) 2px, transparent 2px);
            background-size: 100% 100%, 100% 100%, 60px 60px, 60px 60px;
            color: #ffffff;
            background-attachment: fixed;
        }

        /* 2. RAISED LANDING */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 60vh; 
            margin-top: 5vh;
        }

        /* 3. BOLD TYPOGRAPHY */
        .main-title {
            font-size: clamp(50px, 10vw, 120px); 
            font-weight: 900;
            letter-spacing: -2px;
            margin-bottom: 0px;
            text-transform: uppercase;
            line-height: 0.9;
            color: #ffffff;
            /* Added text shadow for legibility against white areas */
            text-shadow: 4px 4px 15px rgba(0,0,0,0.8);
        }

        .subtitle {
            font-size: 16px; 
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 12px;
            color: #ffffff;
            margin-top: 20px;
            margin-bottom: 60px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        }

        /* 4. OBVIOUS CARD */
        .glass-card {
            background: #000000;
            border: 4px solid #ffffff;
            padding: 50px;
            border-radius: 0px;
            box-shadow: 20px 20px 0px rgba(255,255,255,0.4);
        }

        /* 5. BUTTONS */
        .stButton > button {
            background: #ffffff !important;
            color: #000000 !important;
            border: none;
            padding: 20px 80px;
            font-size: 20px;
            font-weight: 900;
            border-radius: 0px;
            width: 100%;
            transition: 0.15s;
        }

        .stButton > button:hover {
            background: #ff0000 !important;
            color: #ffffff !important;
            transform: translate(-5px, -5px);
            box-shadow: 10px 10px 0px #ffffff;
        }

        .back-btn-container > div > button {
            background: #000000 !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
            margin-top: 20px;
        }

        /* Form Text Visibility */
        .stTextInput label, .stSelectbox label {
            color: #ffffff !important;
            font-weight: bold;
            font-size: 18px;
        }

        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# UI
# --------------------

def home_page():
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>GENERATE SYSTEM</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIATE"):
            go_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-weight:900;'>ACCESS</h1>", unsafe_allow_html=True)
        
        with st.form("signup_form", border=False):
            u = st.text_input("USER ID")
            p = st.text_input("PASSWORD", type="password")
            submitted = st.form_submit_button("CREATE PROFILE")
            
        if submitted and u and p:
            st.session_state.user = {"name": u}
            go_to("generator")
            
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("BACK"):
            go_to("home")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        depth = st.select_slider("INTENSITY", options=["1", "2", "3"])
        if st.button("RUN_ARCHITECT"):
            with st.spinner("CALCULATING NODES..."):
                time.sleep(1)
            st.success("MAP DEPLOYED")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        if st.button("SHUTDOWN"):
            st.session_state.user = None
            go_to("home")

# --------------------
# Main
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