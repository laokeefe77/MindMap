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
# Custom CSS + Animated Background
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* ===== GLOBAL BACKGROUND ===== */
        .stApp {
            background: #000000;
            color: #ffffff;
            overflow-x: hidden;
        }

        /* ===== PARTICLE CONTAINER ===== */
        #bubble-bg {
            position: fixed;
            inset: 0;
            z-index: -1;
            pointer-events: none;
        }

        canvas#bubble-canvas {
            width: 100vw;
            height: 100vh;
            display: block;
        }

        /* ===== LANDING ===== */
        .landing-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 90vh;
        }

        .main-title {
            font-size: clamp(50px, 10vw, 120px);
            font-weight: 900;
            letter-spacing: -2px;
            line-height: 0.9;
            color: #ffffff;
            text-shadow: 10px 10px 0px rgba(0,0,0,0.6);
        }

        .subtitle {
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 12px;
            margin-top: 20px;
            margin-bottom: 60px;
        }

        /* ===== INFO SECTION ===== */
        .info-section {
            max-width: 1100px;
            margin: 120px auto 120px auto;
            padding: 80px;
            background: #000000;
            border: 4px solid white;
            box-shadow: 20px 20px 0px rgba(255,255,255,0.3);
        }

        .info-section h2 {
            font-size: 48px;
            font-weight: 900;
            margin-bottom: 30px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }

        .info-card {
            border: 2px solid white;
            padding: 25px;
            background: black;
        }

        .info-card h3 {
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        /* ===== CARDS ===== */
        .glass-card {
            background: #000000;
            border: 4px solid #ffffff;
            padding: 50px;
            border-radius: 0px;
            box-shadow: 20px 20px 0px rgba(255,255,255,0.4);
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: #ffffff !important;
            color: #000000 !important;
            border: none;
            padding: 18px 70px;
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

        /* Inputs */
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


def load_bubble_background():
    """Inject animated bubble/particle background"""
    st.markdown(
        """
        <div id="bubble-bg">
            <canvas id="bubble-canvas"></canvas>
        </div>

        <script>
        const canvas = document.getElementById("bubble-canvas");
        const ctx = canvas.getContext("2d");

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener("resize", resize);
        resize();

        const bubbles = [];
        const COUNT = 120;

        class Bubble {
            constructor() {
                this.reset();
            }

            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.z = Math.random() * 2 + 0.5;
                this.r = Math.random() * 4 + 2;
                this.vx = (Math.random() - 0.5) * 0.3;
                this.vy = (Math.random() - 0.5) * 0.3;
            }

            update() {
                this.x += this.vx * this.z;
                this.y += this.vy * this.z;

                if (
                    this.x < 0 ||
                    this.x > canvas.width ||
                    this.y < 0 ||
                    this.y > canvas.height
                ) {
                    this.reset();
                }
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.r * this.z, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(255,255,255,0.4)";
                ctx.fill();
            }
        }

        for (let i = 0; i < COUNT; i++) {
            bubbles.push(new Bubble());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let b of bubbles) {
                b.update();
                b.draw();
            }

            requestAnimationFrame(animate);
        }

        animate();
        </script>
        """,
        unsafe_allow_html=True,
    )


def go_to(page):
    st.session_state.page = page
    st.rerun()


# --------------------
# UI Pages
# --------------------

def home_page():
    load_bubble_background()

    # Hero Section
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>GENERATE SYSTEM</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIATE"):
            go_to("signup")

    st.markdown('</div>', unsafe_allow_html=True)

    # Info Section (Scroll Down)
    st.markdown(
        """
        <div class="info-section">
            <h2>HOW IT WORKS</h2>

            <div class="info-grid">

                <div class="info-card">
                    <h3>01 · INPUT</h3>
                    <p>
                    Enter any subject — science, history, business, philosophy, or ideas.
                    The system accepts both simple and complex topics.
                    </p>
                </div>

                <div class="info-card">
                    <h3>02 · ANALYSIS</h3>
                    <p>
                    MindMap Noir decomposes your topic into logical layers,
                    identifying relationships, hierarchies, and dependencies.
                    </p>
                </div>

                <div class="info-card">
                    <h3>03 · NODE GENERATION</h3>
                    <p>
                    Key concepts become nodes. Supporting ideas form branches.
                    This creates a structured knowledge network.
                    </p>
                </div>

                <div class="info-card">
                    <h3>04 · INTENSITY CONTROL</h3>
                    <p>
                    Adjust intensity to control depth: overview, detailed,
                    or expert-level mapping.
                    </p>
                </div>

                <div class="info-card">
                    <h3>05 · VISUAL MAPPING</h3>
                    <p>
                    Outputs are optimized for learning, revision, and creative thinking.
                    Complex ideas become navigable structures.
                    </p>
                </div>

                <div class="info-card">
                    <h3>06 · APPLICATION</h3>
                    <p>
                    Use generated maps for studying, research planning,
                    brainstorming, or project design.
                    </p>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def signup_page():
    load_bubble_background()

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
    load_bubble_background()

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
                time.sleep(1.2)
            st.success("MAP DEPLOYED")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## OUTPUT PREVIEW")

        if topic:
            st.markdown(f"**Target:** {topic}")
            st.markdown(f"**Depth:** {depth}")
            st.markdown("---")
            st.markdown("- Core Concept")
            st.markdown("  - Subtopic A")
            st.markdown("  - Subtopic B")
            st.markdown("    - Detail 1")
            st.markdown("    - Detail 2")
            st.markdown("- Applications")

        else:
            st.markdown("Awaiting system input...")

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
