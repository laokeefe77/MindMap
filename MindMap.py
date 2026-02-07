import streamlit as st

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="MindMap | Deep Space",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Space Background + Effects
# -------------------------------------------------
st.markdown("""
<style>

/* ================================
   Main Background
================================ */
.stApp {
    background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
    color: white;
    overflow-x: hidden;
}


/* ================================
   Space Layer (Orbs)
================================ */
.space-layer {
    position: fixed;
    inset: 0;
    z-index: -2;
    overflow: hidden;
    pointer-events: none;
}

/* Floating Orbs */
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.6;

    background: radial-gradient(circle,
        rgba(100,255,218,0.8),
        rgba(100,255,218,0.25),
        transparent 70%);

    animation:
        float 30s infinite alternate ease-in-out,
        pulse 7s infinite ease-in-out;
}

/* Individual Orbs */
.o1 { width: 280px; height: 280px; top: 10%; left: 5%; }
.o2 { width: 180px; height: 180px; top: 70%; left: 15%; }
.o3 { width: 350px; height: 350px; top: 25%; right: 5%; }
.o4 { width: 220px; height: 220px; bottom: 15%; right: 15%; }
.o5 { width: 160px; height: 160px; top: 50%; left: 45%; }
.o6 { width: 260px; height: 260px; bottom: 35%; left: 65%; }


/* Floating Motion */
@keyframes float {
    from { transform: translate(0, 0); }
    to   { transform: translate(120px, -150px); }
}

/* Glow Pulse */
@keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50%      { opacity: 0.85; }
}


/* ================================
   Typography
================================ */
.hero-text {
    font-size: clamp(4rem, 12vw, 8rem) !important;
    font-weight: 900;
    text-align: center;
    letter-spacing: 15px;

    background: linear-gradient(to bottom,
        #ffffff 30%,
        #64ffda 100%);

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    padding-top: 15vh;
    margin-bottom: 0;
}

.slogan {
    text-align: center;
    font-size: 1rem;
    letter-spacing: 8px;
    text-transform: uppercase;
    color: #8892b0;
    opacity: 0.8;
}


/* ================================
   Glass Panels
================================ */
.glass-card {
    background: rgba(255,255,255,0.02);
    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 0px;

    padding: 40px;
    margin-top: 20px;

    transition: 0.3s;
}

.glass-card:hover {
    border: 1px solid rgba(100,255,218,0.3);
}


/* ================================
   Inputs
================================ */
.stTextInput input {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
}


/* ================================
   Buttons
================================ */
div.stButton > button {

    width: 100%;

    background: transparent;
    color: white !important;

    border: 1px solid white;

    padding: 20px;

    text-transform: uppercase;
    letter-spacing: 3px;

    transition: 0.5s;
}

div.stButton > button:hover {

    background: white;
    color: black !important;

    box-shadow: 0 0 50px rgba(255,255,255,0.2);
}

</style>


<!-- Space Orbs -->
<div class="space-layer">

    <span class="orb o1"></span>
    <span class="orb o2"></span>
    <span class="orb o3"></span>
    <span class="orb o4"></span>
    <span class="orb o5"></span>
    <span class="orb o6"></span>

</div>

""", unsafe_allow_html=True)


# -------------------------------------------------
# Page State
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"


# -------------------------------------------------
# Landing Page
# -------------------------------------------------
if st.session_state.page == "landing":

    st.markdown('<h1 class="hero-text">MindMap</h1>', unsafe_allow_html=True)

    st.markdown(
        '<p class="slogan">Navigating the infinite expanse of thought.</p>',
        unsafe_allow_html=True
    )

    st.write("##")

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        if st.button("Start Your Learning Journey"):

            st.session_state.page = "auth"
            st.rerun()


    st.write("##")
    st.write("##")
    st.write("---")


    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="glass-card">

            <h3 style="letter-spacing:2px;">
                Orbital Organization
            </h3>

            <p style="color:#8892b0;">
                Your data points aren't just entries;
                they are nodes in a constellation.
                Experience a workspace that mimics
                natural clustering of the universe.
            </p>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown("""
        <div class="glass-card">

            <h3 style="letter-spacing:2px;">
                Deep Discovery
            </h3>

            <p style="color:#8892b0;">
                Navigate through layers of complexity
                with fluid transitions. Our engine
                handles massive datasets with the
                grace of silent orbit.
            </p>

        </div>
        """, unsafe_allow_html=True)



# -------------------------------------------------
# Auth Page
# -------------------------------------------------
elif st.session_state.page == "auth":

    if st.button("Return to Void"):

        st.session_state.page = "landing"
        st.rerun()


    c1, c2, c3 = st.columns([1, 2, 1])


    with c2:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("""
        <h2 style="
            text-align:center;
            letter-spacing:5px;
        ">
            PROTOCOL
        </h2>
        """, unsafe_allow_html=True)


        tab_in, tab_up = st.tabs(
            ["Initialize Session", "New Sequence"]
        )


        with tab_in:

            st.text_input("User Key")
            st.text_input("Passcode", type="password")

            st.button("Authenticate")


        with tab_up:

            st.text_input("Assigned Name")
            st.text_input("Registry Email")
            st.text_input("New Passcode", type="password")

            st.button("Register Identity")


        st.markdown('</div>', unsafe_allow_html=True)
