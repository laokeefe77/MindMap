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
# 2. CUSTOM CSS (BLUE HUD THEME)
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 10, 20, 0.95);
            border-right: 1px solid rgba(0, 136, 255, 0.3);
        }

        .main-title { font-size: clamp(50px, 10vw, 120px); font-weight: 900; letter-spacing: -2px; line-height: 0.9; color: #ffffff; }
        
        /* BLUE BRUTALIST GLASS CARD */
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 12px 12px 0px rgba(0, 100, 255, 0.2);
            position: relative;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .stButton > button { 
            background: transparent !important; 
            color: #00d0ff !important; 
            border: 1px solid #00d0ff !important; 
            padding: 10px 20px; 
            font-size: 14px; 
            font-family: 'Courier New', monospace;
            border-radius: 0px; 
            width: 100%; 
            transition: 0.3s; 
        }
        .stButton > button:hover { 
            background: #00d0ff !important; 
            color: #000000 !important; 
            box-shadow: 0 0 15px #00d0ff;
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
                const numStars = 400;
                let centerX, centerY;
                function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; centerX = canvas.width / 2; centerY = canvas.height / 2; }
                window.addEventListener("resize", resize);
                resize();
                class Star {
                    constructor() { this.init(); }
                    init() { this.x = (Math.random() - 0.5) * canvas.width; this.y = (Math.random() - 0.5) * canvas.height; this.z = Math.random() * canvas.width; this.prevZ = this.z; }
                    update() { this.prevZ = this.z; this.z -= 8; if (this.z <= 0) { this.init(); this.z = canvas.width; this.prevZ = this.z; } }
                    draw() {
                        const x = (this.x / this.z) * centerX + centerX;
                        const y = (this.y / this.z) * centerY + centerY;
                        const prevX = (this.x / this.prevZ) * centerX + centerX;
                        const prevY = (this.y / this.prevZ) * centerY + centerY;
                        const size = (1 - this.z / canvas.width) * 2;
                        ctx.beginPath(); ctx.strokeStyle = `rgba(0, 200, 255, ${1 - this.z / canvas.width})`; ctx.lineWidth = size; ctx.lineCap = "round"; ctx.moveTo(prevX, prevY); ctx.lineTo(x, y); ctx.stroke();
                    }
                }
                for (let i = 0; i < numStars; i++) { stars.push(new Star()); }
                function animate() { ctx.fillStyle = "rgba(0, 0, 0, 0.4)"; ctx.fillRect(0, 0, canvas.width, canvas.height); stars.forEach(s => { s.update(); s.draw(); }); requestAnimationFrame(animate); }
                animate();
            })();
        </script>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 4. GRAPH ENGINE
# --------------------
def render_force_graph(data):
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    html_code = f"""
    <div id="cy" style="width: 100%; height: 800px; background: #000; border: 2px solid #0088ff; border-radius: 8px;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {{ nodes: {json.dumps(cy_nodes)}, edges: {json.dumps(cy_edges)} }},
            style: [
                {{ selector: 'node', style: {{ 'background-color': '#fff', 'label': 'data(label)', 'color': '#00d0ff', 'width': 'data(size)', 'height': 'data(size)', 'font-size': '10px', 'font-family': 'monospace' }} }},
                {{ selector: 'edge', style: {{ 'width': 1, 'line-color': 'rgba(0, 150, 255, 0.2)' }} }}
            ],
            layout: {{ name: 'cose', animate: true }}
        }});
    </script>
    """
    components.html(html_code, height=820)

# --------------------
# 5. PAGE DEFINITIONS
# --------------------
def home_page():
    load_space_background()
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 85vh; text-align: center;">
            <div style="font-size: 100px; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: 15px; text-shadow: 0 0 20px rgba(0, 150, 255, 0.8);">Nebula</div>
            <div style="width: 300px; height: 2px; background: linear-gradient(90deg, transparent, #00d0ff, transparent); margin: 20px 0;"></div>
            <div style="font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 12px; color: #ffffff;">Knowledge Mapping Protocol</div>
            <div style="font-family: 'Courier New', monospace; color: #00d0ff; font-size: 12px; letter-spacing: 4px; margin-top: 20px; opacity: 0.7;">LAT: 40.7128 | LONG: 74.0060</div>
        </div>
    """, unsafe_allow_html=True)

    # Secondary Info
    st.markdown("""
    <div style="background-color: #0e1117; padding: 80px 20px; border-radius: 15px; margin-top: 50px;">
        <h2 style="text-align: center;">Why Nebula?</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; max-width: 1100px; margin: 40px auto;">
            <div class="feature-card" style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border: 1px solid rgba(0,136,255,0.2);">
                <h3>🧠 Visual Thinking</h3>
                <p>Turn abstract topics into navigable, interconnected galaxies of information.</p>
            </div>
            <div class="feature-card" style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border: 1px solid rgba(0,136,255,0.2);">
                <h3>⚡ AI Architect</h3>
                <p>Generate instant, structured learning paths tailored to your specific goals.</p>
            </div>
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
        if st.session_state.map_data: render_force_graph(st.session_state.map_data)

# --------------------
# 6. NAVIGATION ENGINE (SIDE MENU)
# --------------------
def main():
    st.set_page_config(page_title="Nebula", page_icon="🌌", layout="wide")
    load_css()
    
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    # THE SIDEBAR MENU (Three-line menu icon appears automatically in top left)
    with st.sidebar:
        st.markdown("<h2 style='color:#00d0ff; font-family:monospace;'>NEBULA_OS</h2>", unsafe_allow_html=True)
        st.write("---")
        
        if st.button("🛰️ HOME PROTOCOL"):
            st.session_state.page = "home"
            st.rerun()
            
        if not st.session_state.user:
            if st.button("🔑 INITIALIZE ACCESS"):
                st.session_state.page = "signup"
                st.rerun()
        else:
            st.write(f"USER: {st.session_state.user['name'].upper()}")
            if st.button("🧠 COMMAND CENTER"):
                st.session_state.page = "generator"
                st.rerun()
            if st.button("⚠️ SHUTDOWN"):
                st.session_state.user = None
                st.session_state.map_data = None
                st.session_state.page = "home"
                st.rerun()

    # Page Rendering
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()