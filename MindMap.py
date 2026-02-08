import streamlit as st
import streamlit.components.v1 as components
import json
import time
import os

# --- PERSISTENCE HELPERS ---
DB_FILE = "users_db.json"

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
    
    # Back to the original balanced sizes
    node_size = 70 if parent_id is None else 35
    
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
        
        /* THE FIX: Hide the header bar background but KEEP the sidebar button visible */
        header[data-testid="stHeader"] {
            background: rgba(0,0,0,0) !important;
            border-bottom: none !important;
        }
        
        /* Make the sidebar arrow visible, blue, and glowing */
        [data-testid="stSidebarCollapsedControl"] {
            color: #00d0ff !important;
            background-color: rgba(0, 136, 255, 0.1) !important;
            border-radius: 0 10px 10px 0 !important;
            border: 1px solid #00d0ff !important;
            top: 10px !important;
        }

        /* Hide the rest of the garbage in the top right menu */
        #MainMenu, footer {visibility: hidden;}

        .main-title { font-size: clamp(50px, 10vw, 120px); font-weight: 900; letter-spacing: -2px; line-height: 0.9; color: #ffffff; }
        
        .glass-card { 
            background: linear-gradient(135deg, #000 0%, #050a10 100%); 
            border: 1px solid rgba(0, 180, 255, 0.3);
            padding: 40px; 
            border-radius: 4px; 
            box-shadow: 10px 10px 0px rgba(0, 0, 0, 1), 12px 12px 0px rgba(0, 100, 255, 0.2);
            position: relative;
            margin-bottom: 20px;
        }

        .stButton > button { 
            background: #ffffff !important; 
            color: #000000 !important; 
            border: none; 
            padding: 10px 20px; 
            font-size: 16px; 
            font-weight: 900; 
            border-radius: 0px; 
            width: 100%; 
            transition: 0.1s; 
        }
        .stButton > button:hover { 
            background: #0088ff !important; 
            color: #ffffff !important; 
            transform: translate(-2px, -2px); 
            box-shadow: 4px 4px 0px #ffffff; 
        }
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
        <style>
            #space-bg {
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                z-index: -1;
                background: radial-gradient(circle at center, #001525 0%, #000000 100%);
            }
            #star-canvas {
                display: block;
            }
        </style>
        <script>
            (function() {
                const canvas = document.getElementById("star-canvas");
                const ctx = canvas.getContext("2d");
                let stars = [];
                const numStars = 400;
                let centerX, centerY;

                function resize() {
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                    centerX = canvas.width / 2;
                    centerY = canvas.height / 2;
                }

                window.addEventListener("resize", resize);
                resize();

                class Star {
                    constructor() {
                        this.init();
                    }
                    init() {
                        this.x = (Math.random() - 0.5) * canvas.width;
                        this.y = (Math.random() - 0.5) * canvas.height;
                        this.z = Math.random() * canvas.width;
                        this.prevZ = this.z;
                    }
                    update() {
                        this.prevZ = this.z;
                        this.z -= 8; // Speed of travel
                        if (this.z <= 0) {
                            this.init();
                            this.z = canvas.width;
                            this.prevZ = this.z;
                        }
                    }
                    draw() {
                        const x = (this.x / this.z) * centerX + centerX;
                        const y = (this.y / this.z) * centerY + centerY;
                        
                        const prevX = (this.x / this.prevZ) * centerX + centerX;
                        const prevY = (this.y / this.prevZ) * centerY + centerY;

                        const size = (1 - this.z / canvas.width) * 2;
                        
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 200, 255, ${1 - this.z / canvas.width})`;
                        ctx.lineWidth = size;
                        ctx.lineCap = "round";
                        ctx.moveTo(prevX, prevY);
                        ctx.lineTo(x, y);
                        ctx.stroke();
                    }
                }

                for (let i = 0; i < numStars; i++) {
                    stars.push(new Star());
                }

                function animate() {
                    ctx.fillStyle = "rgba(0, 0, 0, 0.4)"; // Trail effect
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
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
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'text-valign': 'center', 
                    'text-halign': 'right', 
                    'text-margin-x': '10px',
                    'font-family': 'monospace', 
                    'border-width': 2, 
                    'border-color': '#00a0ff', 
                    'shadow-blur': 12, 
                    'shadow-color': '#0088ff' 
                }} }},
                {{ selector: 'edge', style: {{ 
                    'width': 3,
                    'line-color': 'rgba(0, 150, 255, 0.4)', 
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': 'rgba(0, 150, 255, 0.4)',
                    'arrow-scale': 1.2
                }} }},
                {{ selector: ':selected', style: {{ 'background-color': '#00ffff', 'shadow-blur': 25 }} }}
            ],
            layout: {{ 
                name: 'cose', 
                animate: true, 
                refresh: 20,
                fit: true, 
                padding: 60,
                
                /* COMPACT PHYSICS SETTINGS */
                nodeOverlap: 150,            // Reduced to allow tighter packing
                nodeRepulsion: 4000000,      // Cut in half to let them get closer
                idealEdgeLength: 50,         // Cut in half to pull nodes together
                edgeElasticity: 150,         // Increased "snap" to pull edges tight
                nestingFactor: 0.1, 
                gravity: 0.35,               // Doubled gravity to pull everything toward the center
                numIter: 2500,
                initialTemp: 1000,
                coolingFactor: 0.99
            }}
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
        <style>
        .hero-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            text-align: center;
        }

        .glitch-title {
            font-size: 100px;
            font-weight: 900;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 15px;
            text-shadow: 0 0 20px rgba(0, 150, 255, 0.8),
                         0 0 40px rgba(0, 150, 255, 0.4);
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
            margin-bottom: 40px;
            opacity: 0.7;
        }

        /* FORCE FULL WIDTH AND REMOVE OFFSET EFFECTS */
        div.stButton > button {
            width: 100% !important;
            background: transparent !important;
            color: #00d0ff !important;
            border: 2px solid #00d0ff !important;
            padding: 25px 0px !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            letter-spacing: 5px !important;
            border-radius: 0px !important;
            box-shadow: none !important;
            transform: none !important;
            transition: all 0.4s ease !important;
        }

        div.stButton > button:hover {
            background: rgba(0, 208, 255, 0.1) !important;
            border-color: #ffffff !important;
            color: #ffffff !important;
            box-shadow: 0 0 30px rgba(0, 208, 255, 0.3) !important;
        }
        </style>
        
        <div class="hero-container">
            <div class="glitch-title">Nebula</div>
            <div class="scanline"></div>
            <div class="subtitle" style="margin-bottom:10px;">
                Knowledge Mapping Protocol
            </div>
            <div class="coordinates">
                LAT: 40.7128 | LONG: 74.0060 | SECTOR: G-9
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- FULL WIDTH BUTTON ---
    # use_container_width=True combined with removing the columns 
    # makes it span the entire horizontal space.
    if st.button("INITIALIZE INTERFACE", use_container_width=True):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # FEATURES SECTION
    st.markdown("""
    <style>
        .section-dark {
            background-color: #0e1117;
            padding: 50px 20px;
            border-radius: 15px;
        }
        .section-dark h2 {
            text-align: center;
            color: #ffffff;
            font-size: 2.5rem;
            margin-bottom: 40px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 25px;
            max-width: 1100px;
            margin: 0 auto;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.1);
            border-color: #7d2ae8;
            box-shadow: 0 10px 30px rgba(125, 42, 232, 0.2);
        }
        .section {
            padding: 100px 10%;
            text-align: center;
        }
    </style>
    <div class="section-dark">
        <h2>Why Nebula?</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🧠 Visual Thinking</h3>
                <p>Turn abstract topics into navigable, interconnected galaxies of information.</p>
            </div>
            <div class="feature-card">
                <h3>⚡ AI Architect</h3>
                <p>Generate instant, structured learning paths tailored to your specific goals.</p>
            </div>
            <div class="feature-card"><h3>🌌 Scalable Knowledge</h3><p>Seamlessly bridge the gap between absolute beginner and true mastery.</p></div>
            <div class="feature-card"><h3>🔒 Personal System</h3><p>Your data is yours. Secure, private, and hosted within your own universe.</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ... rest of philosophy and FAQ ...

    # PHILOSOPHY SECTION
    st.markdown("""
        <div class="section">
            <h2 style="font-size: 46px;">Our Philosophy</h2>
            <p style="color:#88ccff; font-size:40px; margin-top:30px;">“Build systems. Not notes.”</p>
            <p style="color:#88ccff; font-size:40px;">“Clarity is engineered.”</p>
            <p style="color:#88ccff; font-size:40px;">“Learning is architecture.”</p>
        </div>
    """, unsafe_allow_html=True)

    # FAQ SECTION
    st.markdown("""
        <div class="section-dark" style="margin-top: 50px;">
            <h2 style="text-align: center;">Frequently Asked Questions</h2>
            <div style="max-width: 800px; margin: 40px auto; text-align: left;">
                <h4 style="color:#00d0ff;">❓ What is Nebula?</h4>
                <p>An AI-powered knowledge mapping system.</p>
                <br>
                <h4 style="color:#00d0ff;">❓ Who is it for?</h4>
                <p>Students, researchers, and self-learners.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- UPDATED PERSISTENCE HELPERS ---
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_user(username, password):
    users = load_users()
    # Store as a dict to hold password AND history
    if username not in users:
        users[username] = {"password": password, "history": {}}
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

def save_map_to_history(username, topic, map_data):
    users = load_users()
    if username in users:
        # Save map data under the topic name
        users[username]["history"][topic] = {
            "data": map_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(DB_FILE, "w") as f:
            json.dump(users, f)

# --- REFACTORED SIGNUP/LOGIN PAGE ---
def signup_page():
    # Make sure this line is on its own line and indented correctly
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    
    with col2:
        st.markdown('<br><br><div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-weight:900;'>ACCESS</h1>", unsafe_allow_html=True)
        
        u = st.text_input("USER ID").strip()
        p = st.text_input("PASSWORD", type="password").strip()
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("INITIALIZE SESSION", use_container_width=True):
                if u and p:
                    users = load_users()
                    users = load_users()
                    if u in users:
                        # Check password within the new dict structure
                        if users[u]["password"] == p:
                            st.session_state.user = {"name": u}
                            st.session_state.page = "generator"
                            st.rerun()
                        else:
                            st.error("CREDENTIAL MISMATCH")
                    else:
                        save_user(u, p)
                        st.session_state.user = {"name": u}
                        st.session_state.page = "generator"
                        st.rerun()
                else:
                    st.error("INPUT REQUIRED")

        with btn_col2:
            if st.button("TERMINATE", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def generator_page():
    username = st.session_state.user['name']
    st.markdown(f"### SYSTEM LOG: {username.upper()}")
    st.markdown("<h1 style='font-weight:900;'>COMMAND_CENTER</h1><hr style='border: 2px solid white;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3]) 
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topic = st.text_input("SUBJECT TARGET")
        if st.button("RUN_ARCHITECT"):
            if topic:
                with st.spinner("INITIATING GEMINI ARCHITECT..."):
                    raw_tree = generate_learning_map(topic)
                    map_result = parse_tree_to_physics(raw_tree)
                    st.session_state.map_data = map_result
                    # SAVE TO JSON HISTORY
                    save_map_to_history(username, topic, map_result)
                st.success("MAP DEPLOYED")
            else:
                st.error("INPUT REQUIRED")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.map_data:
            render_force_graph(st.session_state.map_data)
        else:
            st.markdown("<div style='height: 800px; display: flex; align-items: center; justify-content: center; opacity: 0.3; border: 1px dashed #0088ff; border-radius: 8px; font-family: monospace;'>AWAITING ARCHITECT COMMAND...</div>", unsafe_allow_html=True)

    # --- SIDEBAR HISTORY ---
    with st.sidebar:
        st.markdown("### ARCHIVE_LOGS")
        users = load_users()
        user_data = users.get(username, {})
        history = user_data.get("history", {})

        if history:
            for saved_topic in reversed(list(history.keys())):
                if st.button(f"📂 {saved_topic.upper()}", use_container_width=True):
                    st.session_state.map_data = history[saved_topic]["data"]
                    st.rerun()
        else:
            st.write("No archives found.")

        st.markdown("---")
        if st.button("SHUTDOWN"):
            st.session_state.user = None
            st.session_state.map_data = None
            st.session_state.page = "home"
            st.rerun()

# --------------------
# 6. MAIN EXECUTION
# --------------------
def main():
    if "page" not in st.session_state: 
        st.session_state.page = "home"
    
    # Force the sidebar to be completely tucked away unless we are in the generator
    if st.session_state.page == "generator":
        s_state = "expanded"
    else:
        s_state = "collapsed"

    st.set_page_config(
        page_title="MindMap Noir", 
        page_icon="🧠", 
        layout="wide", 
        initial_sidebar_state=s_state
    )
    
    load_css()
    # ... rest of your code ...

    if "user" not in st.session_state: st.session_state.user = None
    if "map_data" not in st.session_state: st.session_state.map_data = None

    # Handle page routing
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "generator":
        generator_page()

if __name__ == "__main__":
    main()