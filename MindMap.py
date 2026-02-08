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
        /* 1. BACKGROUND & GRID */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(45deg, #000000 25%, rgba(255,255,255,0.1) 100%),
                linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px),
                linear-gradient(0deg, rgba(255,255,255,0.05) 1px, transparent 1px);
            background-size: 100% 100%, 60px 60px, 60px 60px;
            color: #ffffff;
            background-attachment: fixed;
        }

        /* 2. FLOATING BACK ARROW */
        .back-arrow-container {
            position: fixed;
            top: 30px;
            left: 30px;
            z-index: 999;
        }
        
        /* Styling the streamlit button to look like a minimal arrow */
        .back-arrow-container .stButton > button {
            background: transparent !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
            border-radius: 0px !important;
            width: 50px !important;
            height: 50px !important;
            padding: 0px !important;
            font-size: 24px !important;
            font-weight: 200 !important;
            transition: 0.3s;
        }
        
        .back-arrow-container .stButton > button:hover {
            background: #ffffff !important;
            color: #000000 !important;
            box-shadow: 5px 5px 0px rgba(255,255,255,0.3);
        }

        /* 3. LANDING & TYPOGRAPHY */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 70vh; 
        }

        .main-title {
            font-size: clamp(50px, 10vw, 120px); 
            font-weight: 900;
            letter-spacing: -2px;
            text-transform: uppercase;
            line-height: 0.9;
            color: #ffffff;
        }

        .subtitle {
            font-size: 14px; 
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 10px;
            margin-bottom: 40px;
        }

        /* 4. THE BOX (GLASS CARD) */
        .glass-card {
            background: #000000;
            border: 4px solid #ffffff;
            padding: 40px;
            border-radius: 0px;
            box-shadow: 15px 15px 0px rgba(255,255,255,0.2);
        }

        /* 5. MAIN BUTTONS */
        .stButton > button {
            background: #ffffff !important;
            color: #000000 !important;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 900;
            border-radius: 0px;
            width: 100%;
            transition: 0.2s;
        }

        .stButton > button:hover {
            background: #333333 !important;
            color: #ffffff !important;
            transform: translate(-3px, -3px);
            box-shadow: 8px 8px 0px #ffffff;
        }

        /* Hidden Streamlit UI */
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
    """Renders the back arrow in the corner"""
    st.markdown('<div class="back-arrow-container">', unsafe_allow_html=True)
    if st.button("←"):
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
    # Show the back arrow instead of a button inside the form
    back_arrow()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # THE BOX STARTS HERE
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # TITLE IS NOW INSIDE THE BOX
        st.markdown("<h1 style='text-align:center; font-weight:900; margin-top:0; color:white;'>ACCESS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; letter-spacing:3px; font-size:10px; margin-bottom:30px;'>ESTABLISH CREDENTIALS</p>", unsafe_allow_html=True)
        
        with st.form("signup_form", border=False):
            u = st.text_input("USER ID")
            p = st.text_input("PASSWORD", type="password")
            submitted = st.form_submit_button("CREATE PROFILE")
            
        if submitted and u and p:
            st.session_state.user = {"name": u}
            go_to("generator")
            
        st.markdown('</div>', unsafe_allow_html=True) # THE BOX ENDS HERE

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    back_arrow()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    
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