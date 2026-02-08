import streamlit as st
import random
import time

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="MindMap Journey",
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
# Custom CSS (Enhanced for Glassmorphism)
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .main-title {
            text-align: center; font-size: 64px; font-weight: bold;
            margin-top: 50px; letter-spacing: 2px; color: #6dd5ed;
        }
        .subtitle {
            text-align: center; font-size: 20px; opacity: 0.8; margin-bottom: 40px;
        }
        .bubble {
            position: fixed; border-radius: 50%; opacity: 0.2;
            animation: float 20s infinite linear;
            background: radial-gradient(circle, #6dd5ed, #2193b0);
            z-index: -1;
        }
        @keyframes float {
            from { transform: translateY(100vh); }
            to { transform: translateY(-120vh); }
        }
        /* Glassmorphism Card Effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .stButton > button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white; border: none; padding: 12px 30px;
            border-radius: 50px; transition: 0.3s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 198, 255, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_bubbles(n=20):
    html = "".join([f'<div class="bubble" style="width:{random.randint(40,100)}px;height:{random.randint(40,100)}px;left:{random.randint(0,100)}vw;animation-duration:{random.randint(15,30)}s;animation-delay:{random.randint(0,10)}s;"></div>' for _ in range(n)])
    st.markdown(html, unsafe_allow_html=True)

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# Page: Home
# --------------------
def home_page():
    render_bubbles(20)
    st.markdown("<div class='main-title'>MindMap</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Organize your thoughts. Build your future.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Your Journey", use_container_width=True):
            go_to("signup")

# --------------------
# Page: Signup
# --------------------
def signup_page():
    st.markdown("<h1 style='text-align:center;'>Join the Journey</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Create Account")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if name and username and password:
            st.session_state.user = {"name": name, "username": username}
            st.success("Account created! Redirecting to Workspace...")
            time.sleep(1)
            go_to("generator")
        else:
            st.error("Please fill in all fields.")

# --------------------
# Page: Protected Generator (The New Page)
# --------------------
def generator_page():
    # SECURITY CHECK: Redirect if not logged in
    if not st.session_state.user:
        st.warning("Please sign up to access the generator.")
        time.sleep(1)
        go_to("home")
        return

    render_bubbles(10)
    
    # Sidebar for navigation/Logout
    with st.sidebar:
        st.title(f"Hi, {st.session_state.user['name']}!")
        if st.button("Logout"):
            st.session_state.user = None
            go_to("home")

    st.markdown("<h1 style='text-align:center;'>MindMap Generator</h1>", unsafe_allow_html=True)
    st.write("Enter a topic below to architect your learning path.")

    # Generator UI
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    topic = st.text_input("What do you want to learn today?", placeholder="e.g. Quantum Physics, Italian Cooking...")
    depth = st.select_slider("Map Complexity", options=["Simple", "Standard", "Deep"])
    
    if st.button("Generate Map 🧠"):
        with st.status("Architecting your data structure...", expanded=True) as status:
            st.write("Initializing Gemini Flash...")
            time.sleep(1)
            st.write("Building hierarchical nodes...")
            time.sleep(1)
            status.update(label="Map Complete!", state="complete", expanded=False)
        
        st.success(f"Successfully generated a {depth} map for **{topic}**!")
        # This is where you would call your JSON generate function
        st.info("Visualizer rendering engine coming in next update.")
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# Main App Router
# --------------------
def main():
    load_css()
    page = st.session_state.page

    if page == "home":
        home_page()
    elif page == "signup":
        signup_page()
    elif page == "generator":
        generator_page()

if __name__ == "__main__":
    main()