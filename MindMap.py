import streamlit as st
import streamlit.components.v1 as components
import json
import time

# --- IMPORT FROM YOUR Gemini.py FILE ---
# Ensure Gemini.py exists in the same directory
try:
    from Gemini import generate_learning_map
except ImportError:
    def generate_learning_map(topic):
        return {"name": topic, "description": "Mock Data", "children": []}

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

        .stButton > button { 
            background: #ffffff !important; 
            color: #000000 !important; 
            border: none; 
            padding: 18px 70px; 
            font-size: 20px; 
            font-weight: 900; 
            border-radius: 0px; 
            width: 100%; 
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
        <div id="space-bg">
            <canvas id="star-canvas"></canvas>
        </div>

        <script>
            (function() {
                const canvas = document.getElementById("star-canvas");
                const ctx = canvas.getContext("2d");

                function resize() {
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                }

                window.addEventListener("resize", resize);
                resize();

                let stars = [];
                const numStars = 300;

                class Star {
                    constructor() {
                        this.reset();
                    }

                    reset() {
                        this.x = Math.random() * canvas.width;
                        this.y = Math.random() * canvas.height;
                        this.speed = Math.random() * 2 + 0.5;
                        this.size = Math.random() * 2;
                    }

                    update() {
                        this.y -= this.speed;
                        if (this.y < 0) this.reset();
                    }

                    draw() {
                        ctx.fillStyle = "#00d0ff";
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                        ctx.fill();
                    }
                }

                for (let i = 0; i < numStars; i++) {
                    stars.push(new Star());
                }

                function animate() {
                    ctx.fillStyle = "rgba(0,0,0,0.3)";
                    ctx.fillRect(0,0,canvas.width,canvas.height);

                    stars.forEach(s => {
                        s.update();
                        s.draw();
                    });

                    requestAnimationFrame(animate);
                }

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
    <div id="cy" style="width:100%; height:800px;"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>

    <script>
        cytoscape({{
            container: document.getElementById('cy'),
            elements: {{
                nodes: {json.dumps(cy_nodes)},
                edges: {json.dumps(cy_edges)}
            }},
            layout: {{ name: 'cose' }}
        }});
    </script>
    """

    components.html(html_code, height=820)

# --------------------
# 5. PAGES
# --------------------
def home_page():
    load_space_background()

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("INITIALIZE INTERFACE"):
            st.session_state.page = "signup"
            st.rerun()


def signup_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("<h1 style='text-align:center;'>ACCESS</h1>", unsafe_allow_html=True)

        u = st.text_input("USER ID")
        p = st.text_input("PASSWORD", type="password")

        # ---------- BUTTON ROW ----------
        b1, b2 = st.columns(2)

        with b1:
            if st.button("CREATE PROFILE"):
                if u and p:
                    st.session_state.user = {"name": u}
                    st.session_state.page = "generator"
                    st.rerun()

        with b2:
            if st.button("BACK"):
                st.session_state.page = "home"
                st.rerun()

        # -------------------------------

        st.markdown('</div>', unsafe_allow_html=True)


def generator_page():
    st.markdown(f"### SYSTEM LOG: {st.session_state.user['name'].upper()}")

    col1, col2 = st.columns([1, 3]) 

    with col1:
        topic = st.text_input("SUBJECT TARGET")

        if st.button("RUN_ARCHITECT"):
            if topic:
                raw_tree = generate_learning_map(topic)
                st.session_state.map_data = parse_tree_to_physics(raw_tree)

    with col2:
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)


# --------------------
# 6. MAIN
# --------------------
def main():
    st.set_page_config(page_title="MindMap Noir", layout="wide")

    load_css()

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if "user" not in st.session_state:
        st.session_state.user = None

    if "map_data" not in st.session_state:
        st.session_state.map_data = None


    if st.session_state.page == "home":
        home_page()

    elif st.session_state.page == "signup":
        signup_page()

    elif st.session_state.page == "generator":
        generator_page()


if __name__ == "__main__":
    main()
