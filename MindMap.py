import streamlit as st
import streamlit.components.v1 as components
import time
import json

import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- IMPORT FROM YOUR Gemini.py FILE ---
from Gemini import generate_learning_map

# --------------------
# Data Parser: Tree to Physics format
# --------------------
def parse_tree_to_physics(node, nodes=None, edges=None, parent_id=None):
    """
    Converts Gemini's nested JSON into the flat 'nodes' and 'edges' 
    list required for the electron repulsion simulation.
    """
    if nodes is None: nodes = []
    if edges is None: edges = []
    
    # Unique ID for each node based on name and current list length
    current_id = node['name'].replace(" ", "_").lower() + "_" + str(len(nodes))
    
    # Root node is larger than child nodes
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
if "map_data" not in st.session_state:
    st.session_state.map_data = None

# --------------------
# Custom CSS & Backgrounds
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        #bubble-bg { position: fixed; inset: 0; z-index: -1; pointer-events: none; }
        canvas#bubble-canvas { width: 100vw; height: 100vh; display: block; }
        .landing-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 90vh; }
        .main-title { font-size: clamp(50px, 10vw, 120px); font-weight: 900; letter-spacing: -2px; line-height: 0.9; color: #ffffff; text-shadow: 10px 10px 0px rgba(0,0,0,0.6); }
        .subtitle { font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 12px; margin-top: 20px; margin-bottom: 60px; }
        .info-section { max-width: 1100px; margin: 120px auto; padding: 80px; background: #000000; border: 4px solid white; box-shadow: 20px 20px 0px rgba(255,255,255,0.3); }
        .info-section h2 { font-size: 48px; font-weight: 900; margin-bottom: 30px; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
        .info-card { border: 2px solid white; padding: 25px; background: black; }
        .glass-card { background: #000000; border: 4px solid #ffffff; padding: 50px; border-radius: 0px; box-shadow: 20px 20px 0px rgba(255,255,255,0.4); }
        .stButton > button { background: #ffffff !important; color: #000000 !important; border: none; padding: 18px 70px; font-size: 20px; font-weight: 900; border-radius: 0px; width: 100%; transition: 0.15s; }
        .stButton > button:hover { background: #333333 !important; color: #ffffff !important; transform: translate(-5px, -5px); box-shadow: 10px 10px 0px #ffffff; }
        .back-btn-container > div > button { background: #000000 !important; color: #ffffff !important; border: 2px solid #ffffff !important; margin-top: 20px; }
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

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
            draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.r*this.z, 0, Math.PI*2); ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.fill(); }
        }
        for(let i=0; i<COUNT; i++) bubbles.push(new Bubble());
        function animate() { ctx.clearRect(0,0,canvas.width,canvas.height); for(let b of bubbles){ b.update(); b.draw(); } requestAnimationFrame(animate); }
        animate();
        </script>
        """,
        unsafe_allow_html=True,
    )

def render_force_graph(data):
    """The Physics Engine: Nodes behave like repelling charged particles."""
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    
    html_code = f"""
    <div id="cy" style="width: 100%; height: 650px; background: transparent;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {{ nodes: {json.dumps(cy_nodes)}, edges: {json.dumps(cy_edges)} }},
            style: [
                {{
                    selector: 'node',
                    style: {{
                        'background-color': '#ffffff',
                        'label': 'data(label)',
                        'color': '#ffffff',
                        'width': 'data(size)',
                        'height': 'data(size)',
                        'font-size': '10px',
                        'text-valign': 'center',
                        'text-halign': 'right',
                        'text-margin-x': '10px',
                        'font-family': 'monospace',
                        'font-weight': 'bold',
                        'text-outline-width': 2,
                        'text-outline-color': '#000000'
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 1.5,
                        'line-color': 'rgba(255,255,255,0.3)',
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'vee',
                        'target-arrow-color': 'rgba(255,255,255,0.3)'
                    }}
                }}
            ],
            layout: {{
                name: 'cose',
                animate: true,
                refresh: 20,
                fit: true,
                padding: 40,
                nodeRepulsion: 15000,
                idealEdgeLength: 100,
                edgeElasticity: 100,
                componentSpacing: 120
            }}
        }});
    </script>
    """
    components.html(html_code, height=660)

# --------------------
# UI Navigation
# --------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()

def home_page():
    load_bubble_background()
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown("<div class='main-title'>MINDMAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>GENERATE SYSTEM</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIATE"): go_to("signup")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-section"><h2>HOW IT WORKS</h2><div class="info-grid">
        <div class="info-card"><h3>01 · INPUT</h3><p>Enter any subject target.</p></div>
        <div class="info-card"><h3>02 · ARCHITECT</h3><p>Gemini 3 Flash deconstructs the topic.</p></div>
        <div class="info-card"><h3>03 · DYNAMICS</h3><p>Nodes repel like electrons for optimal clarity.</p></div>
    </div></div>""", unsafe_allow_html=True)

def signup_page():
    load_bubble_background()
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<br><br><div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-weight:900;'>ACCESS</h1>", unsafe_allow_html=True)
        with st.form("signup_form", border=False):
            u = st.text_input("USER ID")
            p = st.text_input("PASSWORD", type="password")
            if st.form_submit_button("CREATE PROFILE"):
                if u and p:
                    st.session_state.user = {"name": u}
                    go_to("generator")
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("BACK"): go_to("home")
        st.markdown('</div></div>', unsafe_allow_html=True)

def generator_page():
    load_bubble_background()
    if not st.session_state.user: go_to("home")
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1><hr style='border: 2px solid white;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.2])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        if st.button("RUN_ARCHITECT"):
            if topic:
                with st.spinner("INITIATING GEMINI ARCHITECT..."):
                    # 1. Call the function imported from Gemini.py
                    raw_tree = generate_learning_map(topic)
                    # 2. Parse the result for the physics engine
                    st.session_state.map_data = parse_tree_to_physics(raw_tree)
                st.success("MAP DEPLOYED")
            else:
                st.error("INPUT REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="min-height: 700px;">', unsafe_allow_html=True)
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)
        else:
            st.markdown("<div style='height: 600px; display: flex; align-items: center; justify-content: center; opacity: 0.5;'>AWAITING ARCHITECT COMMAND...</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        if st.button("SHUTDOWN"):
            st.session_state.user = None
            st.session_state.map_data = None
            go_to("home")

def main():
    load_css()
    if st.session_state.page == "home": home_page()
    elif st.session_state.page == "signup": signup_page()
    elif st.session_state.page == "generator": generator_page()

if __name__ == "__main__":
    main()