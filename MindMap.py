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
# Custom CSS: Sweeping Lines & Clean Typography
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* High-Contrast Architectural Background */
        .stApp {
            background-color: #050505;
            background-image: 
                linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 25%),
                linear-gradient(225deg, rgba(255,255,255,0.05) 0%, transparent 50%),
                linear-gradient(0deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 100% 40px;
            color: #ffffff;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* Container raised slightly from absolute center */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 80vh; /* Adjusted from 70 to move content up */
            width: 100%;
            margin-top: -5vh; /* Direct nudge upwards */
        }

        .main-title {
            font-size: clamp(40px, 8vw, 85px); 
            font-weight: 200;
            letter-spacing: 15px;
            margin-bottom: 5px;
            text-transform: uppercase;
            color: #ffffff;
        }

        .subtitle {
            font-size: 12px; 
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 8px;
            opacity: 0.6;
            margin-bottom: 60px;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 4px;
            backdrop-filter: blur(10px);
        }

        /* Buttons */
        .stButton {
            display: flex;
            justify-content: center;
            gap: 10px;
        }

        .stButton > button {
            background: #ffffff;
            color: #000000 !important;
            border: none;
            padding: 10px 40px;
            font-weight: 600;
            letter-spacing: 2px;
            border-radius: 0px;
            transition: 0.3s ease;
        }

        /* Secondary Button (Back) */
        .back-btn > div > button {
            background: transparent !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }

        .stButton > button:hover {
            opacity: 0.8;
            transform: translateY(-2px);
        }

        /* Hide Streamlit components */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# Pages
# --------------------

def home_page():
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Architecting Knowledge</div>", unsafe_allow_html=True)
    
    if st.button("INITIALIZE"):
        go_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    # Vertical spacer to center card better
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; letter-spacing:5px; font-weight:200;'>REGISTRATION</p>", unsafe_allow_html=True)
        
        with st.form("signup_form", border=False):
            u = st.text_input("USER")
            p = st.text_input("PASS", type="password")
            submitted = st.form_submit_button("CREATE")
            
        if submitted and u and p:
            st.session_state.user = {"name": u}
            go_to("generator")
            
        # Back button outside form to avoid triggering form validation
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← RETURN"):
            go_to("home")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    st.markdown(f"<p style='letter-spacing:2px; opacity:0.4;'>LOGGED AS: {st.session_state.user['name'].upper()}</p>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:200; letter-spacing:5px;'>CONTROL PANEL</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT")
        depth = st.select_slider("INTENSITY", options=["1", "2", "3"])
        if st.button("PROCESS"):
            with st.spinner("ANALYZING..."):
                time.sleep(1)
            st.success("NODE MAP GENERATED")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        if st.button("LOGOUT"):
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