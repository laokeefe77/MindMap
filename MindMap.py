import streamlit as st
import streamlit.components.v1 as components
import json
import time

# --- IMPORT FROM YOUR Gemini.py FILE ---
from Gemini import generate_learning_map

# --------------------
# 1. DATA PARSER (Balanced Scale)
# --------------------
def parse_tree_to_physics(node, nodes=None, edges=None, parent_id=None):
    if nodes is None: nodes = []
    if edges is None: edges = []
    
    current_id = node['name'].replace(" ", "_").lower() + "_" + str(len(nodes))
    # Big central hub (80), standard subnodes (35)
    node_size = 80 if parent_id is None else 35
    
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
# 2. CUSTOM CSS (Original Noir Design)
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        
        .landing-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 90vh; }
        .main-title { font-size: clamp(50px, 10vw, 120px); font-weight: 900; letter-spacing: -2px; line-height: 0.9; color: #ffffff; }
        .subtitle { font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 12px; margin-top: 20px; margin-bottom: 60px; }

        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 12px 12px 0px rgba(0, 100, 255, 0.2);
            position: relative; overflow: hidden; margin-bottom: 20px;
        }

        .stButton > button { background: #ffffff !important; color: #000000 !important; border: none; padding: 18px 70px; font-size: 20px; font-weight: 900; border-radius: 0px; width: 100%; transition: 0.1s; }
        .stButton > button:hover { background: #0088ff !important; color: #ffffff !important; transform: translate(-3px, -3px); box-shadow: 6px 6px 0px #ffffff; }

        .stTextInput label { color: #ffffff !important; font-weight: bold; font-size: 18px; }
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 3. STARFIELD ENGINE (Fixed Background)
# --------------------
def load_bubble_background():
    # This renders the starfield as a fixed background layer
    components.html(
        """
        <style>
            body { margin: 0; overflow: hidden; background: black; }
            canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; }
        </style>
        <canvas id="starCanvas"></canvas>
        <script>
            const canvas = document.getElementById("starCanvas");
            const ctx = canvas.getContext("2d");
            let stars = [];

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            window.onresize = resize;
            resize();

            class Star {
                constructor() {
                    this.reset();
                    this.y = Math.random() * canvas.height;
                }
                reset() {
                    this.x = Math.random() * canvas.width;
                    this.y = canvas.height + 10;
                    this.size = Math.random() * 1.5 + 0.5;
                    this.speed = Math.random() * 0.8 + 0.2;
                    this.opacity = Math.random() * 0.5 + 0.3;
                }
                update() {
                    this.y -= this.speed;
                    if (this.y < -10) this.reset();
                }
                draw() {
                    ctx.fillStyle = `rgba(0, 160, 255, ${this.opacity})`;
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            for(let i=0; i<150; i++) stars.push(new Star());

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                stars.forEach(s => { s.update(); s.draw(); });
                requestAnimationFrame(animate);
            }
            animate();
        </script>
        """,
        height=0 # Hidden iframe container so it doesn't push UI down
    )

# --------------------
# 4. GRAPH ENGINE (Original Wrapped Border)
# --------------------
def render_force_graph(data):
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    
    html_code = f"""
    <div id="cy" style="width: 100%; height: 800px; background: #000; border: 2px solid #0088ff; border-radius: 8px; box-shadow: 0 0 15px rgba(0, 136, 255, 0.3);"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {{ nodes: {json.dumps(cy_nodes)}, edges: {json.dumps(cy_edges)} }},
            style: [
                {{ selector: 'node', style: {{ 'background-color': '#fff', 'label': 'data(label)', 'color': '#00d0ff', 'width': 'data(size)', 'height': 'data(size)', 'font-size': '14px', 'text-valign': 'center', 'text-halign': 'right', 'font-family': 'monospace', 'border-width': 2, 'border-color': '#00a0ff', 'shadow-blur': 15, 'shadow-color': '#0088ff' }} }},
                {{ selector: 'edge', style: {{ 'width': 2, 'line-color': 'rgba(0, 150, 255, 0.2)', 'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'target-arrow-color': 'rgba(0, 150, 255, 0.4)' }} }}
            ],
            layout: {{ 
                name: 'cose', animate: true, fit: true, padding: 50,
                nodeOverlap: 50, nodeRepulsion: 4500000, idealEdgeLength: 100, gravity: 2.5
            }}
        }});
    </script>
    """
    components.html(html_code, height=820)

# --------------------
# 5. PAGE LOGIC
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

def main():
    st.set_page_config(page_title="MindMap Noir", page_icon="🧠", layout="wide")
    load_css()
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    if st.session_state.page == "home": home_page()
    elif st.session_state.page == "signup": signup_page()
    elif st.session_state.page == "generator": generator_page()

if __name__ == "__main__":
    main()