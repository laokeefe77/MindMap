import streamlit as st
import streamlit.components.v1 as components
import time
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
# Page Config
# --------------------
st.set_page_config(
    page_title="MindMap Noir",
    page_icon="🧠",
    layout="wide"
)

# --------------------
# Custom CSS
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        #bubble-bg { position: fixed; inset: 0; z-index: -1; pointer-events: none; }
        canvas#bubble-canvas { width: 100vw; height: 100vh; display: block; }

        /* BRUTALIST HUD CARD */
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 30px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 
                        12px 12px 0px rgba(0, 100, 255, 0.1);
            position: relative;
            overflow: hidden;
            margin-bottom: 20px;
        }

        /* FULL WIDTH GRAPH CONTAINER */
        .graph-display-container {
            border: 2px solid #0088ff;
            box-shadow: 0 0 20px rgba(0, 136, 255, 0.2);
            background: rgba(0, 0, 0, 0.8);
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
        }

        .stButton > button { background: #ffffff !important; color: #000000 !important; border: none; padding: 15px; font-weight: 900; width: 100%; transition: 0.1s; }
        .stButton > button:hover { background: #0088ff !important; color: #ffffff !important; transform: translateY(-2px); }
        
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def load_bubble_background():
    st.markdown("""<div id="bubble-bg"><canvas id="bubble-canvas"></canvas></div>
    <script>
    const canvas = document.getElementById("bubble-canvas");
    const ctx = canvas.getContext("2d");
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener("resize", resize); resize();
    const bubbles = [];
    class Bubble {
        constructor() { this.reset(); }
        reset() { this.x = Math.random()*canvas.width; this.y = Math.random()*canvas.height; this.z = Math.random()*2+0.5; this.r = Math.random()*4+2; this.vx = (Math.random()-0.5)*0.3; this.vy = (Math.random()-0.5)*0.3; }
        update() { this.x += this.vx*this.z; this.y += this.vy*this.z; if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height) this.reset(); }
        draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.r*this.z, 0, Math.PI*2); ctx.fillStyle = "rgba(0,136,255,0.3)"; ctx.fill(); }
    }
    for(let i=0; i<120; i++) bubbles.push(new Bubble());
    function animate() { ctx.clearRect(0,0,canvas.width,canvas.height); for(let b of bubbles){ b.update(); b.draw(); } requestAnimationFrame(animate); }
    animate();
    </script>""", unsafe_allow_html=True)

def render_force_graph(data):
    """Noir-Cyber Physics Engine: Deep Sea Blue Theme with Wrapped Border."""
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    
    # We add the border directly to the div style here to ensure it wraps the graph exactly
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
                {{
                    selector: 'node',
                    style: {{
                        'background-color': '#fff',
                        'label': 'data(label)',
                        'color': '#00d0ff', 
                        'width': 'data(size)',
                        'height': 'data(size)',
                        'font-size': '12px',
                        'text-valign': 'center',
                        'text-halign': 'right',
                        'text-margin-x': '12px',
                        'font-family': '"Courier New", monospace',
                        'font-weight': 'bold',
                        'text-transform': 'uppercase',
                        'border-width': 2,
                        'border-color': '#00a0ff',
                        'shadow-blur': 15,
                        'shadow-color': '#0088ff',
                        'shadow-opacity': 0.8
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 1.5,
                        'line-color': 'rgba(0, 150, 255, 0.2)',
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'triangle',
                        'target-arrow-color': 'rgba(0, 150, 255, 0.4)',
                        'arrow-scale': 0.8
                    }}
                }},
                {{
                    selector: ':selected',
                    style: {{
                        'background-color': '#00ffff',
                        'shadow-blur': 25
                    }}
                }}
            ],
            layout: {{
                name: 'cose',
                animate: true,
                fit: true,
                padding: 50,
                nodeRepulsion: 120000, 
                idealEdgeLength: 140
            }}
        }});
    </script>
    """
    # Increased height of the component to accommodate the internal 800px div + border
    components.html(html_code, height=820)

def generator_page():
    load_bubble_background()
    if not st.session_state.user: go_to("home")
    
    # Restored your original header style
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1><hr style='border: 2px solid white;'>", unsafe_allow_html=True)

    # Restored 2-column layout but tweaked ratios for a larger graph (1:3 instead of 1:2.2)
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
        # The graph now lives in its own container within the column
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)
        else:
            # Placeholder matches the new height
            st.markdown("""
                <div style='
                    height: 800px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    opacity: 0.3; 
                    border: 1px dashed #0088ff; 
                    border-radius: 8px;
                    font-family: monospace;
                '>
                    AWAITING ARCHITECT COMMAND...
                </div>
            """, unsafe_allow_html=True)

    with st.sidebar:
        # Sidebar remains exactly where it was
        if st.button("SHUTDOWN"):
            st.session_state.user = None
            st.session_state.map_data = None
            go_to("home")


def main():
    load_css()
    
    # --- INITIALIZATION BLOCK ---
    # This prevents the "KeyError" by ensuring the variables exist 
    # even if they are empty/None at first.
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "user" not in st.session_state:
        st.session_state.user = None
    if "map_data" not in st.session_state:
        st.session_state.map_data = None
    # ----------------------------

    # Navigation Logic
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()