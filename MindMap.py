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
# Custom CSS: High-Contrast Architecture
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* High-Contrast Background: Laser Lines & Deep Noir */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 35%),
                linear-gradient(225deg, rgba(255,255,255,0.1) 0%, transparent 45%),
                /* Vertical "Architecture" Lines */
                linear-gradient(90deg, transparent 49.9%, rgba(255,255,255,0.05) 50%, transparent 50.1%);
            background-size: 100% 100%, 100% 100%, 80px 100%;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* Lifted Landing Container */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 75vh; 
            width: 100%;
            margin-top: -10vh; /* Lifted significantly */
        }

        .main-title {
            font-size: clamp(45px, 9vw, 95px); 
            font-weight: 100; /* Thin but LARGE */
            letter-spacing: 20px;
            margin-bottom: 0px;
            text-transform: uppercase;
            color: #ffffff;
            text-shadow: 0 0 20px rgba(255,255,255,0.2);
        }

        .subtitle {
            font-size: 13px; 
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 10px;
            color: rgba(255,255,255,0.5);
            margin-bottom: 60px;
        }

        /* Visible Glass Card with Border Glow */
        .glass-card {
            background: rgba(15, 15, 15, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.2);
            padding: 50px;
            border-radius: 0px;
            box-shadow: 0 0 30px rgba(255,255,255,0.05);
            backdrop-filter: blur(15px);
        }

        /* Buttons: Pure White vs Outline */
        .stButton > button {
            background: #ffffff !important;
            color: #000000 !important;
            border: none;
            padding: 12px 60px;
            font-weight: 800;
            letter-spacing: 3px;
            border-radius: 0px;
            transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
        }

        /* Back Button logic */
        .back-btn-container > div > button {
            background: transparent !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.5) !important;
            margin-top: 15px;
        }

        .stButton > button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 20px rgba(255,255,255,0.3);
        }

        /* Form Text Visibility */
        .stTextInput label, .stSelectbox label {
            color: rgba(255,255,255,0.8) !important;
            letter-spacing: 2px;
        }

        /* Removing Streamlit clutter */
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# UI Components
# --------------------

def home_page():
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRUCTURAL INTELLIGENCE</div>", unsafe_allow_html=True)
    
    if st.button("INITIALIZE"):
        go_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; font-weight:200; letter-spacing:8px;'>AUTH</h3>", unsafe_allow_html=True)
        
        with st.form("signup_form", border=False):
            u = st.text_input("USERNAME")
            p = st.text_input("PASSWORD", type="password")
            submitted = st.form_submit_button("CREATE IDENTITY")
            
        if submitted and u and p:
            st.session_state.user = {"name": u}
            go_to("generator")
            
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← RETURN TO TERMINAL"):
            go_to("home")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    st.markdown(f"<p style='letter-spacing:2px; color:rgba(255,255,255,0.5);'>OPERATOR: {st.session_state.user['name'].upper()}</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-weight:200; letter-spacing:5px;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT")
        depth = st.select_slider("PRECISION", options=["LOW", "MED", "MAX"])
        if st.button("EXECUTE"):
            with st.spinner("PROCESSING..."):
                time.sleep(1)
            st.success("MAP COMPILED.")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        if st.button("TERMINATE"):
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