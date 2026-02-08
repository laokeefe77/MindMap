def home_page():
    load_space_background()
    
    # --- HERO SECTION ---
    st.markdown("""
        <style>
        .hero-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60vh;
            text-align: center;
        }
        .glitch-title {
            font-size: 100px;
            font-weight: 900;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 15px;
            text-shadow: 0 0 20px rgba(0, 150, 255, 0.8), 0 0 40px rgba(0, 150, 255, 0.4);
            margin-bottom: 0;
            animation: pulse 4s infinite alternate;
        }
        @keyframes pulse {
            from { opacity: 0.8; transform: scale(0.98); }
            to { opacity: 1; transform: scale(1); }
        }
        .scanline {
            width: 300px;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00d0ff, transparent);
            margin: 20px 0;
            box-shadow: 0 0 10px #00d0ff;
        }
        .coordinates {
            font-family: 'Courier New', monospace;
            color: #00d0ff;
            font-size: 12px;
            letter-spacing: 4px;
            margin-bottom: 20px;
            opacity: 0.7;
        }
        </style>
        
        <div class="hero-container">
            <div class="glitch-title">Nebula</div>
            <div class="scanline"></div>
            <div class="subtitle" style="margin-bottom:10px;">Knowledge Mapping Protocol</div>
            <div class="coordinates">LAT: 40.7128 | LONG: 74.0060 | SECTOR: G-9</div>
        </div>
    """, unsafe_allow_html=True)

    # PRIMARY CALL TO ACTION (Under Hero)
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 LAUNCH ARCHITECT", key="hero_launch"):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- FEATURES SECTION ---
    st.markdown("""
    <style>
        .section-dark { background-color: #0e1117; padding: 50px 20px; border-radius: 15px; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; max-width: 1100px; margin: 0 auto; }
        .feature-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 20px; }
    </style>
    <div class="section-dark">
        <h2 style='text-align:center;'>Why Nebula?</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🧠 Visual Thinking</h3>
                <p>Turn abstract topics into navigable, interconnected galaxies of information.</p>
            </div>
            <div class="feature-card">
                <h3>⚡ AI Architect</h3>
                <p>Generate instant, structured learning paths tailored to your specific goals.</p>
            </div>
            <div class="feature-card">
                <h3>🌌 Scalable Knowledge</h3>
                <p>Seamlessly bridge the gap between absolute beginner and true mastery.</p>
            </div>
            <div class="feature-card">
                <h3>🔒 Personal System</h3>
                <p>Your data is yours. Secure, private, and hosted within your own universe.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- PHILOSOPHY & FAQ ---
    st.markdown("""
        <div style="text-align: center; padding: 80px 0;">
            <h2>Our Philosophy</h2>
            <p style="color:#88ccff; font-size:20px;">“Build systems. Not notes.”</p>
            <p style="color:#88ccff; font-size:20px;">“Clarity is engineered.”</p>
        </div>
    """, unsafe_allow_html=True)

    # --- FINAL CALL TO ACTION ---
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2>Ready to Begin?</h2>
            <p style="color:#99ccff;">Transform how you learn. Design how you think.</p>
        </div>
    """, unsafe_allow_html=True)

    _, col_final, _ = st.columns([1, 1, 1])
    with col_final:
        if st.button("✨ GET STARTED", key="final_get_started"):
            st.session_state.page = "signup"
            st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)