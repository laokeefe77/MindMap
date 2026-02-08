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
# Custom CSS
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* 1. ORIGINAL AGGRESSIVE GRID */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(45deg, #000000 25%, rgba(255,255,255,0.6) 100%),
                linear-gradient(90deg, rgba(255,255,255,0.15) 2px, transparent 2px),
                linear-gradient(0deg, rgba(255,255,255,0.15) 2px, transparent 2px);
            background-size: 100% 100%, 60px 60px, 60px 60px;
            color: #ffffff;
            background-attachment: fixed;
        }

        /* 2. THE NEW MINIMAL SPINNING ARROW */
        /* We use a specific class path to kill the default Streamlit button styling */
        .back-arrow-container div[data-testid="stButton"] button {
            background-color: transparent !important;
            background: transparent !important;
            color: #ffffff !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            font-size: 80px !important; /* Extremely large */
            line-height: 1 !important;
            padding: 0px !important;
            width: auto !important;
            height: auto !important;
            transition: transform 0.6s ease-in-out !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* The Spin Animation */
        .back-arrow-container div[data-testid="stButton"] button:hover {
            transform: rotate(-180deg) !important;
            background-color: transparent !important;
            color: #ffffff !important;
            border: none !important;
        }
        
        /* Kill the click animation shadow */
        .back-arrow-container div[data-testid="stButton"] button:active {
            background-color: transparent !important;
            border: none !important;
        }

        /* 3. THE BOX (GLASS CARD) */
        .glass-card {
            background: #000000;
            border: 4px solid #ffffff;
            padding: 50px;
            border-radius: 0px;
            box-shadow: 20px 20px 0px rgba(255,255,255,0.4);
        }

        /* 4. MAIN BUTTONS (INITIATE / CREATE / RUN) */
        /* These stay as the big white blocks you liked */
        div[data-testid="stForm"] .stButton button, 
        .landing-container .stButton button,
        .glass-card .stButton button {
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
            background: #333333 !important;
            color: #ffffff !important;
            transform: translate(-5px, -5px);
            box-shadow: 10px 10px 0px #ffffff;
        }

        /* 5. TITLES & TYPOGRAPHY */
        .main-title {
            font-size: clamp(50px, 10vw, 120px); 
            font-weight: 900;
            letter-spacing: -2px;
            text-transform: uppercase;
            line-height: 0.9;
            color: #ffffff;
            text-shadow: 4px 4px 15px rgba(0,0,0,0.8);
        }
        .subtitle {
            font-size: 16px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 12px; margin-bottom: 60px;
        }
        .landing-container {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; text-align: center; min-height: 60vh;
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
# UI COMPONENTS
# --------------------

def back_arrow():
    """Renders the minimal large arrow in the corner"""
    st.markdown('<div class="back-arrow-container">', unsafe_allow_html=True)
    if st.button("⟵"): # Using a longer arrow for clear visual change
        go_to("home")
    st.markdown('</div>', unsafe_allow_html=True)

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
    back_arrow()
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-weight:900; color:white; margin-top:0;'>ACCESS</h1>", unsafe_allow_html=True)
        
        with st.form("signup_form", border=False):
            u = st.text_input("USER ID")
            p = st.text_input("PASSWORD", type="password")
            submitted = st.form_submit_button("CREATE PROFILE")
            
        if submitted and u and p:
            st.session_state.user = {"name": u}
            go_to("generator")
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    back_arrow()
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