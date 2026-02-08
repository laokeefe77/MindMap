import streamlit as st
import streamlit.components.v1 as components
import json
import time

# --- MOCK IMPORT (Ensure Gemini.py exists in your directory) ---
# from Gemini import generate_learning_map

def generate_learning_map(topic):
    """Mock function for debugging - replace with your actual import"""
    return {
        "name": topic,
        "description": f"Core concepts of {topic}",
        "children": [
            {"name": "Foundations", "description": "Basic principles"},
            {"name": "Advanced Theory", "description": "Complex applications"}
        ]
    }

# --------------------
# 1. DATA PARSER (Improved ID generation)
# --------------------
def parse_tree_to_physics(node, nodes=None, edges=None, parent_id=None):
    if nodes is None: nodes = []
    if edges is None: edges = []
    
    # Using a unique hash or index to prevent ID collisions
    node_index = len(nodes)
    current_id = f"{node['name'].replace(' ', '_').lower()}_{node_index}"
    
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
# 2. CUSTOM CSS
# --------------------
def load_css():
    st.markdown(
        """
        <style>
        .stApp { background: #000000; color: #ffffff; overflow-x: hidden; }
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 12px 12px 0px rgba(0, 100, 255, 0.2);
            position: relative;
            margin-bottom: 20px;
        }
        .stButton > button { background: #ffffff !important; color: #000000 !important; border: none; padding: 10px 20px; font-weight: 900; border-radius: 0px; width: 100%; }
        .stButton > button:hover { background: #0088ff !important; color: #ffffff !important; }
        header, footer, #MainMenu {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# 3. BACKGROUND ANIMATIONS
# --------------------
def load_space_background():
    # Integrated both bubble and star logic here for consistency
    st.markdown(
        """
        <div id="space-bg"><canvas id="star-canvas"></canvas></div>
        <script>
        const canvas = document.getElementById("star-canvas");
        const ctx = canvas.getContext("2d");
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener("resize", resize); 
        resize();
        const stars = [];
        for(let i=0; i<200; i++) stars.push({
            x: Math.random()*canvas.width, y: Math.random()*canvas.height, 
            size: Math.random()*1.5, speed: Math.random()*0.5
        });
        function animate() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width,canvas.height);
            stars.forEach(s => {
                ctx.fillStyle = "white"; ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI*2); ctx.fill();
                s.y += s.speed; if(s.y > canvas.height) s.y = 0;
            });
            requestAnimationFrame(animate);
        }
        animate();
        </script>
        <style>#space-bg { position: fixed; top:0; left:0; width:100%; height:100%; z-index:-1; }</style>
        """, unsafe_allow_html=True)

# --------------------
# 4. GRAPH ENGINE
# --------------------
def render_force_graph(data):
    cy_nodes = [{"data": n} for n in data["nodes"]]
    cy_edges = [{"data": {"id": f"e{i}", "source": e["source"], "target": e["target"]}} for i, e in enumerate(data["edges"])]
    
    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <div id="cy" style="width: 100%; height: 600px; background: #000; border: 1px solid #0088ff;"></div>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {{ nodes: {json.dumps(cy_nodes)}, edges: {json.dumps(cy_edges)} }},
            style: [
                {{ selector: 'node', style: {{ 'background-color': '#fff', 'label': 'data(label)', 'color': '#00d0ff', 'width': 'data(size)', 'height': 'data(size)', 'font-family': 'monospace' }} }},
                {{ selector: 'edge', style: {{ 'width': 1, 'line-color': '#004466', 'curve-style': 'bezier' }} }}
            ],
            layout: {{ name: 'cose', animate: true }}
        }});
    </script>
    """
    components.html(html_code, height=620)

# --------------------
# 5. PAGES
# --------------------
def home_page():
    load_space_background()
    st.markdown('<div style="text-align:center; margin-top:15vh;"><h1 style="font-size:80px; letter-spacing:10px;">NEBULA</h1><p>KNOWLEDGE ARCHITECT</p></div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 0.6, 1])
    with col2:
        if st.button("LAUNCH ARCHITECT"):
            st.session_state.page = "signup"
            st.rerun()

def signup_page():
    load_space_background() # Fixed: Replaced missing load_bubble_background
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("CREATE PROFILE"):
            if u and p:
                st.session_state.user = {"name": u}
                st.session_state.page = "generator"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    load_space_background()
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")
    col1, col2 = st.columns([1, 3]) 
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        if st.button("RUN_ARCHITECT"):
            if topic:
                raw_tree = generate_learning_map(topic)
                st.session_state.map_data = parse_tree_to_physics(raw_tree)
            else:
                st.error("INPUT REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)
        else:
            st.info("Awaiting Target...")

# --------------------
# 6. MAIN
# --------------------
def main():
    st.set_page_config(page_title="Nebula Noir", layout="wide")
    load_css()
    
    if "page" not in st.session_state: st.session_state.page = "home"
    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    if st.session_state.page == "home": home_page()
    elif st.session_state.page == "signup": signup_page()
    elif st.session_state.page == "generator": generator_page()

if __name__ == "__main__":
    main()