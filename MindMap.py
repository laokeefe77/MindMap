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
        /* Modern Background with Sweeping Linear Gradients */
        .stApp {
            background-color: #000000;
            background-image: 
                linear-gradient(215deg, rgba(255,255,255,0.05) 0%, transparent 40%),
                linear-gradient(125deg, rgba(255,255,255,0.03) 0%, transparent 50%);
            color: #ffffff;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* Centering Container for the Landing Page */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 70vh;
            width: 100%;
        }

        /* Thinner, Sleeker Typography */
        .main-title {
            font-size: 72px; 
            font-weight: 300; /* Light weight for elegance */
            letter-spacing: 12px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: 14px; 
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 6px;
            opacity: 0.5;
            margin-bottom: 40px;
        }

        /* Glass Card - Minimized to only wrap content */
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 4px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            display: inline-block; /* Prevents empty stretching */
            width: 100%;
        }

        /* Perfectly Centered Button */
        .stButton {
            display: flex;
            justify-content: center;
        }

        .stButton > button {
            background: #ffffff;
            color: #000000 !important;
            border: none;
            padding: 12px 50px;
            font-weight: 600;
            letter-spacing: 2px;
            border-radius: 2px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background: #cccccc;
            transform: scale(1.05);
        }

        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# Page Logic
# --------------------

def home_page():
    # Using a single container to ensure vertical and horizontal centering
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The Architecture of Intelligence</div>", unsafe_allow_html=True)
    
    # Custom button placement for centering
    if st.button("ENTER"):
        go_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; font-weight:300; letter-spacing:4px;'>SIGN UP</h3>", unsafe_allow_html=True)
        with st.form("signup_form", border=False):
            st.text_input("NAME")
            username = st.text_input("USER")
            password = st.text_input("PASS", type="password")
            # The form submit button also centers automatically with CSS
            submit = st.form_submit_button("CREATE")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit and username and password:
        st.session_state.user = {"name": username}
        go_to("generator")

def generator_page():
    if not st.session_state.user:
        go_to("home")
    
    # Minimalist Workspace
    st.markdown(f"<h5 style='letter-spacing:3px; opacity:0.6;'>OPERATOR: {st.session_state.user['name'].upper()}</h5>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-weight:300; letter-spacing:2px;'>WORKSPACE</h2>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("INPUT TOPIC", placeholder="e.g., Deep Learning")
        depth = st.select_slider("DEPTH", options=["LOW", "MID", "MAX"])
        if st.button("EXECUTE"):
            with st.spinner("BUILDING..."):
                time.sleep(2)
            st.success("JSON COMPILED.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        if st.button("LOGOUT"):
            st.session_state.user = None
            go_to("home")

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