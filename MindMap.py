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
        #bubble-bg { position: fixed; inset: 0; z-index: -1; pointer-events: none; }
        canvas#bubble-canvas { width: 100vw; height: 100vh; display: block; }

        .landing-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 90vh; }
        .main-title { font-size: clamp(50px, 10vw, 120px); font-weight: 900; letter-spacing: -2px; line-height: 0.9; color: #ffffff; }
        .subtitle { font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 12px; margin-top: 20px; margin-bottom: 60px; }

        /* BLUE BRUTALIST GLASS CARD */
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 
                        12px 12px 0px rgba(0, 100, 255, 0.2);
            position: relative;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .glass-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(rgba(0, 150, 255, 0.1) 1px, transparent 1px);
            background-size: 30px 30px;
            pointer-events: none;
            z-index: 0;
        }
        .glass-card > * { position: relative; z-index: 1; }

        .stButton > button { background: #ffffff !important; color: #000000 !important; border: none; padding: 18px 70px; font-size: 20px; font-weight: 900; border-radius: 0px; width: 100%; transition: 0.1s; }
        .stButton > button:hover { background: #0088ff !important; color: #ffffff !important; transform: translate(-3px, -3px); box-shadow: 6px 6px 0px #ffffff; }

        .stTextInput label { color: #ffffff !important; font-weight: bold; font-size: 18px; }
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 3. BACKGROUND ANIMATION
# --------------------
def load_bubble_background():
    st.markdown(
        """
        <div id="bubble-bg"><canvas id="bubble-canvas"></canvas></div>
        <script>
        const canvas = document.getElementById("bubble-canvas");
        const ctx = canvas.getContext("2d");
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener("resize", resize); resize();
        const bubbles = []; const COUNT = 120;
        class Bubble {
            constructor() { this.reset(); }
            reset() { this.x = Math.random()*canvas.width; this.y = Math.random()*canvas.height; this.z = Math.random()*2+0.5; this.r = Math.random()*4+2; this.vx = (Math.random()-0.5)*0.3; this.vy = (Math.random()-0.5)*0.3; }
            update() { this.x += this.vx*this.z; this.y += this.vy*this.z; if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height) this.reset(); }
            draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.r*this.z, 0, Math.PI*2); ctx.fillStyle = "rgba(0,150,255,0.2)"; ctx.fill(); }
        }
        for(let i=0; i<COUNT; i++) bubbles.push(new Bubble());
        function animate() { ctx.clearRect(0,0,canvas.width,canvas.height); for(let b of bubbles){ b.update(); b.draw(); } requestAnimationFrame(animate); }
        animate();
        </script>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 4. GRAPH ENGINE (BLUE THEME)
# --------------------
def render_force_graph(data):
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    
    html_code = f"""
    <div id="cy" style="
        width: 100%; 
        height: 800px; 
        background: #000; 
        border: 2px solid #0088ff; 
        box-shadow: 0 0 15px rgba(0, 136, 255, 0.3);
        border-radius: 8px;
    "></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {{ nodes: {json.dumps(cy_nodes)}, edges: {json.dumps(cy_edges)} }},
            style: [
                {{ selector: 'node', style: {{ 
                    'background-color': '#fff', 
                    'label': 'data(label)', 
                    'color': '#00d0ff', 
                    'width': 'data(size)', 
                    'height': 'data(size)', 
                    'font-size': '12px', 
                    'text-valign': 'center', 
                    'text-halign': 'right', 
                    'font-family': 'monospace', 
                    'border-width': 2, 
                    'border-color': '#00a0ff', 
                    'shadow-blur': 15, 
                    'shadow-color': '#0088ff' 
                }} }},
                {{ selector: 'edge', style: {{ 
                    'width': 1.5, 
                    'line-color': 'rgba(0, 150, 255, 0.2)', 
                    'curve-style': 'bezier', 
                    'target-arrow-shape': 'triangle', 
                    'target-arrow-color': 'rgba(0, 150, 255, 0.4)' 
                }} }},
                {{ selector: ':selected', style: {{ 'background-color': '#00ffff', 'shadow-blur': 25 }} }}
            ],
            layout: {{ 
                name: 'cose', 
                animate: true, 
                componentSpacing: 200,      // Forces separate components further apart
                nodeRepulsion: 10000000,    // Extreme repulsion
                idealEdgeLength: 300,       // Triple the distance between parent/child
                edgeElasticity: 0.1,        // Makes edges very "weak" so they don't pull nodes together
                nestingFactor: 0.05,        // Drastically reduces the "cluster" pull
                gravity: 0.05,              // Minimum gravity so nodes don't drift to center
                numIter: 2500,              // Max iterations to allow full expansion
                initialTemp: 500,           // High energy start to "explode" the nodes outward
                coolingFactor: 0.99         // Slower cooling so it spends more time expanding
            }}
        }});
    </script>
    """
    components.html(html_code, height=820)

# --------------------
# 5. PAGE DEFINITIONS
# --------------------
def home_page():
    load_bubble_background()
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>GENERATE SYSTEM</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIATE"): 
            st.session_state.page = "signup"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    load_bubble_background()
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
    load_bubble_background()
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1><hr style='border: 2px solid white;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3]) 
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        if st.button("RUN_ARCHITECT"):
            if topic:
                with st.spinner("INITIATING GEMINI ARCHITECT..."):
                    raw_tree = generate_learning_map(topic)
                    st.session_state.map_data = parse_tree_to_physics(raw_tree)
                st.success("MAP DEPLOYED")
            else:
                st.error("INPUT REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)
        else:
            st.markdown("<div style='height: 800px; display: flex; align-items: center; justify-content: center; opacity: 0.3; border: 1px dashed #0088ff; border-radius: 8px; font-family: monospace;'>AWAITING ARCHITECT COMMAND...</div>", unsafe_allow_html=True)

    with st.sidebar:
        if st.button("SHUTDOWN"):
            st.session_state.user = None
            st.session_state.map_data = None
            st.session_state.page = "home"
            st.rerun()

# --------------------
# 6. MAIN EXECUTION
# --------------------
def main():
    st.set_page_config(page_title="MindMap Noir", page_icon="🧠", layout="wide")
    load_css()
    
    # Initialize Session State
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    # Routing
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()