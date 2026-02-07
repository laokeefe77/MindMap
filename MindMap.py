import streamlit as st
import random

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="MindMap Journey",
    page_icon="🧠",
    layout="wide"
)

# --------------------
# Session State
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# --------------------
# Custom CSS
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        .main-title {
            text-align: center;
            font-size: 64px;
            font-weight: bold;
            margin-top: 80px;
            letter-spacing: 2px;
        }

        .subtitle {
            text-align: center;
            font-size: 20px;
            opacity: 0.8;
            margin-bottom: 60px;
        }

        .bubble {
            position: fixed;
            border-radius: 50%;
            opacity: 0.25;
            animation: float 20s infinite linear;
            background: radial-gradient(circle, #6dd5ed, #2193b0);
        }

        @keyframes float {
            from {
                transform: translateY(100vh);
            }
            to {
                transform: translateY(-120vh);
            }
        }

        .center-btn {
            display: flex;
            justify-content: center;
            margin-top: 80px;
        }

        .stButton > button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white;
            border: none;
            padding: 16px 40px;
            font-size: 20px;
            border-radius: 50px;
            transition: 0.3s ease;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }

        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #0072ff, #00c6ff);
        }

        .form-card {
            background: rgba(255,255,255,0.08);
            padding: 40px;
            border-radius: 20px;
            max-width: 600px;
            margin: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# Floating Bubbles
# --------------------
def render_bubbles(n=20):
    html = ""
    for i in range(n):
        size = random.randint(40, 120)
        left = random.randint(0, 100)
        duration = random.randint(15, 35)
        delay = random.randint(0, 20)

        html += f"""
        <div class="bubble" style="
            width:{size}px;
            height:{size}px;
            left:{left}vw;
            animation-duration:{duration}s;
            animation-delay:{delay}s;
        "></div>
        """

    st.markdown(html, unsafe_allow_html=True)

# --------------------
# Navigation
# --------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

# --------------------
# Home Page
# --------------------
def home_page():
    render_bubbles(25)

    st.markdown("<div class='main-title'>MindMap</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Organize your thoughts. Build your future.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
    if st.button("🚀 Start Your Journey"):
        go_to("signup")
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------
# Signup Page
# --------------------
def signup_page():
    st.markdown("<h1 style='text-align:center;'>Create Your Account</h1>", unsafe_allow_html=True)

    st.markdown("<div class='form-card'>", unsafe_allow_html=True)

    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        interest = st.selectbox(
            "Main Interest",
            ["Study", "Business", "Programming", "Design", "Other"],
        )

        submit = st.form_submit_button("Sign Up")

    if submit:
        if not name or not email or not username or not password:
            st.error("Please fill in all required fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            # Example: Store in session (replace with database later)
            st.session_state.user = {
                "name": name,
                "email": email,
                "username": username,
                "age": age,
                "interest": interest,
            }

            st.success("Account created successfully!")
            st.info("Welcome to MindMap 🎉")

            if st.button("Go to Dashboard"):
                go_to("dashboard")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        go_to("home")

# --------------------
# Dashboard Page
# --------------------
def dashboard_page():
    user = st.session_state.get("user", {})

    st.markdown("<h1>📊 Dashboard</h1>", unsafe_allow_html=True)

    if not user:
        st.warning("Please sign up first.")
        if st.button("Go to Signup"):
            go_to("signup")
        return

    st.success(f"Welcome, {user.get('name', 'User')} 👋")

    st.markdown("---")

    st.subheader("Your Profile")
    st.write("**Username:**", user.get("username"))
    st.write("**Email:**", user.get("email"))
    st.write("**Age:**", user.get("age"))
    st.write("**Interest:**", user.get("interest"))

    st.markdown("---")

    st.subheader("Your MindMap (Coming Soon 🚧)")
    st.info("Here you will be able to create and manage your mind maps.")

    if st.button("Log Out"):
        st.session_state.clear()
        go_to("home")

# --------------------
# Main App
# --------------------
def main():
    load_css()

    page = st.session_state.page

    if page == "home":
        home_page()
    elif page == "signup":
        signup_page()
    elif page == "dashboard":
        dashboard_page()


if __name__ == "__main__":
    main()
