import streamlit as st


# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="MindMap | Deep Space",
    layout="wide"
)


# =================================================
# SPACE BACKGROUND (STARS + ORBS)
# =================================================
st.markdown("""
<style>

/* =================================================
   MAIN BACKGROUND
================================================= */
.stApp {
    background: radial-gradient(ellipse at bottom, #0f1c2e 0%, #050608 100%);
    color: white;
    overflow: hidden;
}


/* =================================================
   STARFIELD SYSTEM
================================================= */

.starfield {
    position: fixed;
    inset: 0;
    z-index: -3;
    pointer-events: none;
    overflow: hidden;
}

/* Base star layer */
.stars {
    position: absolute;
    width: 2px;
    height: 2px;
    background: white;

    box-shadow:
    50px 100px white, 120px 400px white, 300px 800px white,
    500px 200px white, 700px 900px white, 900px 100px white,
    1100px 600px white, 1300px 300px white, 1500px 800px white,
    1700px 200px white, 1900px 500px white,
    200px 700px white, 400px 500px white, 600px 300px white,
    800px 600px white, 1000px 900px white, 1400px 500px white,
    1600px 100px white;

    filter: drop-shadow(0 0 6px white);

    animation: starsMove 80s linear infinite;
}

/* Smaller stars (far) */
.stars-small {
    width: 1px;
    height: 1px;
    opacity: 0.7;

    box-shadow:
    80px 200px #aaa, 250px 600px #aaa, 450px 900px #aaa,
    650px 300px #aaa, 850px 700px #aaa, 1050px 100px #aaa,
    1250px 500px #aaa, 1450px 900px #aaa, 1650px 400px #aaa;

    animation: starsMove 150s linear infinite;
}

/* Big bright stars (near) */
.stars-big {
    width: 3px;
    height: 3px;

    box-shadow:
    150px 150px #fff, 450px 350px #fff, 750px 550px #fff,
    1050px 250px #fff, 1350px 650px #fff, 1650px 850px #fff;

    filter: drop-shadow(0 0 10px #fff);

    animation: starsMove 50s linear infinite;
}


/* Star animation */
@keyframes starsMove {
    from { transform: translateY(0); }
    to   { transform: translateY(-2000px); }
}


/* =================================================
   NEBULA ORBS
================================================= */

.space-orbs {
    position: fixed;
    inset: 0;
    z-index: -2;
    pointer-events: none;
}

.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);

    background: radial-gradient(circle,
        rgba(100,255,218,0.9),
        rgba(100,255,218,0.25),
        transparent 70%);

    animation:
        float 35s infinite alternate ease-in-out,
        pulse 7s infinite ease-in-out;
}

/* Orb positions */
.o1 { width: 320px; height: 320px; top: 10%; left: 5%; }
.o2 { width: 220px; height: 220px; bottom: 20%; left: 20%; }
.o3 { width: 380px; height: 380px; top: 25%; right: 5%; }
.o4 { width: 260px; height: 260px; bottom: 15%; right: 15%; }


@keyframes float {
    from { transform: translate(0,0); }
    to   { transform: translate(150px,-120px); }
}

@keyframes pulse {
    0%,100% { opacity: 0.4; }
    50%     { opacity: 0.85; }
}


/* =================================================
   UI STYLING
================================================= */

.hero-text {
    font-size: clamp(4rem, 12vw, 8rem);
    font-weight: 900;
    text-align: center;
    letter-spacing: 14px;

    background: linear-gradient(to bottom, #fff 30%, #64ffda 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    padding-top: 15vh;
}

.slogan {
    text-align: center;
    letter-spacing: 7px;
    color: #8aa0c8;
}


/* Glass cards */
.glass-card {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.06);

    padding: 40px;
    margin-top: 20px;

    transition: 0.3s;
}

.glass-card:hover {
    border-color: rgba(100,255,218,0.5);
}


/* Inputs */
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
}


/* Buttons */
div.stButton > button {
    width: 100%;

    background: transparent;
    color: white !important;

    border: 1px solid white;

    padding: 15px;

    letter-spacing: 2px;
    transition: 0.4s;
}

div.stButton > button:hover {
    background: white;
    color: black !important;
}

</style>


<!-- STARFIELD -->
<div class="starfield">

    <div class="stars"></div>
    <div class="stars-small"></div>
    <div class="stars-big"></div>

</div>


<!-- NEBULA ORBS -->
<div class="space-orbs">

    <span class="orb o1"></span>
    <span class="orb o2"></span>
    <span class="orb o3"></span>
    <span class="orb o4"></span>

</div>

""", unsafe_allow_html=True)



# =================================================
# PAGE STATE
# =================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"


# =================================================
# LANDING PAGE
# =================================================
if st.session_state.page == "landing":

    st.markdown('<h1 class="hero-text">MindMap</h1>', unsafe_allow_html=True)

    st.markdown(
        '<p class="slogan">Navigating the infinite expanse of thought.</p>',
        unsafe_allow_html=True
    )

    st.write("##")

    _, center, _ = st.columns([1,1.3,1])


    with center:

        if st.button("Start Your Learning Journey"):
            st.session_state.page = "auth"
            st.rerun()


    st.write("---")


    c1, c2 = st.columns(2)


    with c1:

        st.markdown("""
        <div class="glass-card">

            <h3>Orbital Organization</h3>

            <p style="color:#8892b0;">
                Transform ideas into constellations
                of connected thought.
            </p>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown("""
        <div class="glass-card">

            <h3>Deep Discovery</h3>

            <p style="color:#8892b0;">
                Explore knowledge like interstellar
                navigation.
            </p>

        </div>
        """, unsafe_allow_html=True)



# =================================================
# AUTH PAGE
# =================================================
elif st.session_state.page == "auth":

    if st.button("Return to Void"):

        st.session_state.page = "landing"
        st.rerun()


    _, mid, _ = st.columns([1,2,1])


    with mid:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown(
            "<h2 style='text-align:center;letter-spacing:4px;'>PROTOCOL</h2>",
            unsafe_allow_html=True
        )


        tab1, tab2 = st.tabs(["Login", "Register"])


        with tab1:

            st.text_input("User Key")
            st.text_input("Passcode", type="password")

            st.button("Authenticate")


        with tab2:

            st.text_input("Name")
            st.text_input("Email")
            st.text_input("Password", type="password")

            st.button("Register")


        st.markdown("</div>", unsafe_allow_html=True)
