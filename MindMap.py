import streamlit as st
import streamlit.components.v1 as components
import json
import time

# --- IMPORT FROM YOUR Gemini.py FILE ---
# from Gemini import generate_learning_map 

# --------------------
# 1. DATA PARSER
# --------------------
def parse_tree_to_physics(node, nodes=None, edges=None, parent_id=None):
    if nodes is None: nodes = []
    if edges is None: edges = []
    
    current_id = node['name'].replace(" ", "_").lower() + "_" + str(len(nodes))
    node_size = 45 if parent_id is None else 25
    
    nodes.append({
        "id": current_id, 
        "label": node['name'].upper(), 
        "size": node_size,
        "description": node.get('description', '')
    })
    
    if parent_id:
        edges.append({"source": parent_id, "target": current_id})
        
    if "children" in node and node["children"]:
        for child in node["children"]:
            parse_tree_to_physics(child, nodes, edges, current_id)
            
    return {"nodes": nodes, "edges": edges}

# --------------------
# 2. ENHANCED NEAT CSS
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Space+Mono&display=swap');

        /* Global Reset */
        .stApp { 
            background: #000000; 
            color: #ffffff; 
            font-family: 'Inter', sans-serif;
        }

        /* Typography Scaling */
        h1 { font-size: 3.5rem !important; font-weight: 900 !important; letter-spacing: -1px !important; }
        h2 { font-size: 2.2rem !important; font-weight: 700 !important; margin-bottom: 1.5rem !important; }
        h3 { font-size: 1.5rem !important; font-weight: 700 !important; color: #00d0ff; }
        p { font-size: 1.1rem !important; line-height: 1.6 !important; opacity: 0.8; }

        /* Centering Utilities */
        .center-text { text-align: center; }
        .flex-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }

        /* Modern Glass Card */
        .glass-card { 
            background: rgba(10, 20, 30, 0.4); 
            border: 1px solid rgba(0, 180, 255, 0.2);
            padding: 2.5rem; 
            border-radius: 12px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
            margin: 1rem 0;
        }

        /* Button Styling */
        .stButton > button { 
            background: transparent !important; 
            color: #00d0ff !important; 
            border: 1px solid #00d0ff !important; 
            padding: 0.75rem 2rem; 
            font-size: 1rem; 
            font-weight: 700; 
            border-radius: 4px; 
            width: 100%; 
            transition: 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .stButton > button:hover { 
            background: #00d0ff !important; 
            color: #000 !important; 
            box-shadow: 0 0 20px rgba(0, 208, 255, 0.4);
        }

        /* Input Fields */
        .stTextInput input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(0,208,255,0.3) !important;
            color: white !important;
            border-radius: 4px !important;
        }

        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 3. BACKGROUND ANIMATION
# --------------------
def load_space_background():
    st.markdown(
        """
        <div id="space-bg"><canvas id="star-canvas"></canvas></div>
        <style>
            #space-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: #000; }
            #star-canvas { display: block; }
        </style>
        <script>
            (function() {
                const canvas = document.getElementById("star-canvas");
                const ctx = canvas.getContext("2d");
                let stars = [];
                function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
                window.addEventListener("resize", resize);
                resize();
                class Star {
                    constructor() { this.init(); }
                    init() {
                        this.x = (Math.random() - 0.5) * canvas.width;
                        this.y = (Math.random() - 0.5) * canvas.height;
                        this.z = Math.random() * canvas.width;
                    }
                    update() {
                        this.z -= 5;
                        if (this.z <= 0) { this.init(); this.z = canvas.width; }
                    }
                    draw() {
                        const x = (this.x / this.z) * (canvas.width/2) + (canvas.width/2);
                        const y = (this.y / this.z) * (canvas.height/2) + (canvas.height/2);
                        const s = (1 - this.z / canvas.width) * 2;
                        ctx.fillStyle = `rgba(0, 208, 255, ${1 - this.z / canvas.width})`;
                        ctx.fillRect(x, y, s, s);
                    }
                }
                for (let i = 0; i < 300; i++) stars.push(new Star());
                function animate() {
                    ctx.fillStyle = "black"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                    stars.forEach(s => { s.update(); s.draw(); });
                    requestAnimationFrame(animate);
                }
                animate();
            })();
        </script>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 4. PAGE DEFINITIONS
# --------------------

def home_page():
    load_space_background()
    
    st.markdown("""
        <div class="flex-center" style="height: 70vh; text-align: center;">
            <h1 style="margin-bottom: 0;">NEBULA</h1>
            <div style="width: 100px; height: 2px; background: #00d0ff; margin: 20px 0; box-shadow: 0 0 10px #00d0ff;"></div>
            <p style="text-transform: uppercase; letter-spacing: 8px; font-weight: 300; font-family: 'Space Mono'; color: #00d0ff;">
                Knowledge Mapping Protocol
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        if st.button("Launch Architect"):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown("---")
    
    # Feature Section with Clean Grid
    st.markdown("""
        <div class="center-text" style="padding: 4rem 0;">
            <h2>Engineered for Clarity</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin-top: 3rem;">
                <div class="glass-card">
                    <h3>Visual Thinking</h3>
                    <p>Map abstract concepts into navigable constellations.</p>
                </div>
                <div class="glass-card">
                    <h3>AI Architect</h3>
                    <p>Structure your learning path with neural precision.</p>
                </div>
                <div class="glass-card">
                    <h3>Personal Node</h3>
                    <p>Data-driven insights for long-term retention.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def signup_page():
    load_space_background()
    # Centering the login box
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 class='center-text'>SYSTEM ACCESS</h2>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("PASSWORD", type="password")
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        if st.button("INITIALIZE PROFILE"):
            if u and p:
                st.session_state.user = {"name": u}
                st.session_state.page = "generator"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    st.markdown(f"<p style='font-family:\"Space Mono\"; color:#00d0ff;'>LOGGED_AS: {st.session_state.user['name'].upper()}</p>", unsafe_allow_html=True)
    st.markdown("<h1>COMMAND CENTER</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2.5], gap="large") 
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("TARGET SUBJECT")
        if st.button("RUN ARCHITECT"):
            # Mocking the AI call for demonstration
            # raw_tree = generate_learning_map(topic)
            # st.session_state.map_data = parse_tree_to_physics(raw_tree)
            st.info("Architect is scanning...")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.map_data:
            # Graph rendering call here
            pass
        else:
            st.markdown("""
                <div style='height: 600px; display: flex; align-items: center; justify-content: center; 
                border: 1px dashed rgba(0, 136, 255, 0.3); border-radius: 12px; font-family: "Space Mono"; opacity: 0.5;'>
                    AWAITING TARGET PARAMETERS...
                </div>
            """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Nebula | AI", page_icon="🧠", layout="wide")
    load_css()
    
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()