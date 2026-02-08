import streamlit as st
import streamlit.components.v1 as components
import json
import time

# --- IMPORT FROM YOUR Gemini.py FILE ---
from Gemini import generate_learning_map

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
# 2. CUSTOM CSS (TERMINAL HUD THEME)
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        /* Base App Styling */
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        
        /* THE SIDEBAR - MAKING IT VISIBLE & HUD-LIKE */
        [data-testid="stSidebar"] {
            background-color: #000810 !important;
            border-right: 2px solid #00d0ff;
            box-shadow: 5px 0 15px rgba(0, 208, 255, 0.2);
        }
        
        /* Sidebar Button Styling */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(0, 208, 255, 0.1) !important;
            color: #00d0ff !important;
            border: 1px solid #00d0ff !important;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            text-align: left;
            padding: 10px;
            margin-bottom: 10px;
            transition: 0.3s;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #00d0ff !important;
            color: #000000 !important;
            box-shadow: 0 0 20px #00d0ff;
        }

        /* Glass Card for Login/Generator */
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1);
            position: relative;
        }

        /* Sections styling */
        .section-dark {
            background-color: #0e1117;
            padding: 80px 20px;
            border-radius: 15px;
            margin-top: 50px;
            border: 1px solid rgba(0, 208, 255, 0.1);
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
            #space-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: radial-gradient(circle at center, #001525 0%, #000000 100%); }
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
                    init() { this.x = (Math.random() - 0.5) * canvas.width; this.y = (Math.random() - 0.5) * canvas.height; this.z = Math.random() * canvas.width; this.prevZ = this.z; }
                    update() { this.prevZ = this.z; this.z -= 8; if (this.z <= 0) { this.init(); this.z = canvas.width; this.prevZ = this.z; } }
                    draw() {
                        const x = (this.x / this.z) * (canvas.width/2) + (canvas.width/2);
                        const y = (this.y / this.z) * (canvas.height/2) + (canvas.height/2);
                        const size = (1 - this.z / canvas.width) * 2;
                        ctx.beginPath(); ctx.fillStyle = `rgba(0, 200, 255, ${1 - this.z / canvas.width})`;
                        ctx.arc(x, y, size, 0, Math.PI * 2); ctx.fill();
                    }
                }
                for (let i = 0; i < 400; i++) { stars.push(new Star()); }
                function animate() { ctx.fillStyle = "rgba(0, 0, 0, 0.4)"; ctx.fillRect(0, 0, canvas.width, canvas.height); stars.forEach(s => { s.update(); s.draw(); }); requestAnimationFrame(animate); }
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
    
    # HERO SECTION
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; text-align: center;">
            <div style="font-size: 100px; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: 15px; text-shadow: 0 0 20px rgba(0, 150, 255, 0.8);">Nebula</div>
            <div style="width: 300px; height: 2px; background: linear-gradient(90deg, transparent, #00d0ff, transparent); margin: 20px 0;"></div>
            <div style="font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 12px; color: #ffffff;">Knowledge Mapping Protocol</div>
            <div style="font-family: 'Courier New', monospace; color: #00d0ff; font-size: 12px; letter-spacing: 4px; margin-top: 20px; opacity: 0.7;">[ OPEN SIDEBAR MENU TO INITIALIZE ]</div>
        </div>
    """, unsafe_allow_html=True)

    # FEATURES SECTION
    st.markdown("""
    <div class="section-dark">
        <h2 style="text-align: center; color: #fff; font-size: 2.5rem; margin-bottom: 40px;">Why Nebula?</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; max-width: 1100px; margin: 0 auto;">
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,208,255,0.2);">
                <h3>🧠 Visual Thinking</h3>
                <p>Turn abstract topics into navigable, interconnected galaxies of information.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,208,255,0.2);">
                <h3>⚡ AI Architect</h3>
                <p>Generate instant, structured learning paths tailored to your specific goals.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,208,255,0.2);">
                <h3>🌌 Scalable Knowledge</h3>
                <p>Seamlessly bridge the gap between absolute beginner and true mastery.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PHILOSOPHY & FAQ (The rest of your content)
    st.markdown("""
        <div style="padding: 100px 10%; text-align: center;">
            <h2>Our Philosophy</h2>
            <p style="color:#88ccff; font-size:20px; margin-top:30px;">“Build systems. Not notes.”</p>
        </div>
        <div class="section-dark">
            <h2 style="text-align: center;">FAQ</h2>
            <div style="max-width: 800px; margin: 0 auto;">
                <h4>❓ What is Nebula?</h4>
                <p>An AI-powered knowledge mapping system.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def signup_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<br><br><div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-weight:900;'>ACCESS</h1>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("CREATE PROFILE"):
            if u and p:
                st.session_state.user = {"name": u}
                st.session_state.page = "generator"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    col1, col2 = st.columns([1, 3]) 
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        if st.button("RUN_ARCHITECT"):
            if topic:
                with st.spinner("INITIATING..."):
                    raw_tree = generate_learning_map(topic)
                    st.session_state.map_data = parse_tree_to_physics(raw_tree)
            else: st.error("INPUT REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.session_state.map_data:
            # Re-using your Cytoscape logic here
            cy_nodes = [{"data": n} for n in st.session_state.map_data["nodes"]]
            cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(st.session_state.map_data["edges"])]
            html_code = f"<div id='cy' style='width:100%;height:800px;background:#000;'></div><script src='https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js'></script><script>var cy=cytoscape({{container:document.getElementById('cy'),elements:{{nodes:{json.dumps(cy_nodes)},edges:{json.dumps(cy_edges)}}},style:[{{selector:'node',style:{{'label':'data(label)','color':'#00d0ff','background-color':'#fff'}}}}],layout:{{name:'cose'}}}});</script>"
            components.html(html_code, height=820)

# --------------------
# 5. MAIN / NAVIGATION
# --------------------
def main():
    st.set_page_config(page_title="Nebula", layout="wide")
    load_css()
    
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    # THE SIDEBAR (High Visibility)
    with st.sidebar:
        st.markdown("<h1 style='color:#00d0ff; font-family:monospace; font-size:24px;'>NEBULA_OS</h1>", unsafe_allow_html=True)
        st.write("---")
        
        if st.button("🛰️ DASHBOARD / HOME"):
            st.session_state.page = "home"
            st.rerun()
            
        if not st.session_state.user:
            if st.button("🔑 INITIALIZE ACCESS"):
                st.session_state.page = "signup"
                st.rerun()
        else:
            st.success(f"ONLINE: {st.session_state.user['name'].upper()}")
            if st.button("🧠 COMMAND CENTER"):
                st.session_state.page = "generator"
                st.rerun()
            if st.button("⚠️ SHUTDOWN"):
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()

    # Page Routing
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()