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
    node_size = 60 if parent_id is None else 40
    
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
    <div style="position: relative;">
        <div id="node-info" style="
            position: absolute;
            top: 20px;
            left: 20px;
            width: 250px;
            background: rgba(0, 20, 40, 0.85);
            border-left: 4px solid #00d0ff;
            color: #00d0ff;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            z-index: 10;
            pointer-events: none;
            display: none;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        ">
            <div style="font-weight: bold; text-decoration: underline; margin-bottom: 5px;" id="info-title"></div>
            <div id="info-desc" style="color: #fff; opacity: 0.9;"></div>
        </div>

        <div id="cy" style="
            width: 100%; 
            height: 800px; 
            background: #000; 
            border: 2px solid #0088ff; 
            box-shadow: 0 0 15px rgba(0, 136, 255, 0.3);
            border-radius: 8px;
        "></div>
    </div>

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
                {{ selector: ':selected', style: {{ 
                    'background-color': '#00ffff', 
                    'shadow-blur': 25,
                    'border-color': '#fff',
                    'border-width': 4
                }} }}
            ],
            layout: {{ 
                name: 'cose', 
                animate: true, 
                refresh: 20,
                fit: true, 
                padding: 60,
                nodeOverlap: 150,
                nodeRepulsion: 4000000,
                idealEdgeLength: 50,
                edgeElasticity: 150,
                nestingFactor: 0.1, 
                gravity: 0.35,
                numIter: 2500
            }}
        }});

        // INTERACTION LOGIC
        const infoBox = document.getElementById('node-info');
        const infoTitle = document.getElementById('info-title');
        const infoDesc = document.getElementById('info-desc');

        cy.on('mouseover', 'node', function(evt){{
            var node = evt.target;
            infoTitle.innerText = node.data('label');
            infoDesc.innerText = node.data('description') || 'No description available.';
            infoBox.style.display = 'block';
        }});

        cy.on('mouseout', 'node', function(evt){{
            infoBox.style.display = 'none';
        }});
        
        // Ensure description stays if clicked
        cy.on('select', 'node', function(evt){{
            var node = evt.target;
            infoTitle.innerText = node.data('label');
            infoDesc.innerText = node.data('description') || 'No description available.';
            infoBox.style.display = 'block';
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
    st.markdown("""
    <style>
        .core-summary {
            text-align: center;
            max-width: 900px;
            margin: 100px auto 80px auto;
            padding: 40px 20px;
            border-top: 1px solid rgba(0, 208, 255, 0.1);
            border-bottom: 1px solid rgba(0, 208, 255, 0.1);
        }
        .protocol-label {
            color: #00d0ff;
            font-family: 'Courier New', monospace;
            letter-spacing: 8px;
            font-size: 14px;
            margin-bottom: 20px;
            text-transform: uppercase;
            opacity: 0.8;
        }
        .core-text {
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            font-weight: 800;
            line-height: 1.3;
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        .core-text span {
            color: #00d0ff;
            text-shadow: 0 0 15px rgba(0, 208, 255, 0.4);
        }
    </style>
    <div class="core-summary">
        <div class="protocol-label">Core Protocol</div>
        <div class="core-text">
            Input any subject. <span>Nebula</span> architecturally engineers a 
            visual knowledge map, instantly converting chaotic data into a 
            structured learning path.
        </div>
    </div>
    """, unsafe_allow_html=True)
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
            <h2 style="font-size: 46px;">Our Mission</h2>
            <p style="color:#88ccff; font-size:30px; margin-top:30px;">“In the age of information overload, knowing what to learn is often harder than the learning itself. Nebula acts as your intellectual architect, engineering structured pathways out of the chaotic 'information fog' of the modern web. We transform vast, fragmented data into navigable knowledge galaxies, allowing you to stop searching for the path and start walking it.”</p>
        </div>
    """, unsafe_allow_html=True)

    # FAQ SECTION
    st.markdown("""
    <div class="section-dark" style="margin-top: 50px;">
        <h2 style="text-align: center;">Frequently Asked Questions</h2>
        <div style="max-width: 800px; margin: 40px auto; text-align: left;">
            <h4 style="color:#00d0ff;">❓ What is Nebula?</h4>
            <p>Nebula is an AI-powered architect for your intellectual journey. It transforms the chaotic "information fog" of any topic into a structured, navigable galaxy of nodes and connections.</p>
            <br>
            <h4 style="color:#00d0ff;">❓ Who is it for?</h4>
            <p>Architects of their own education: students, researchers, and self-learners who want to build systems, not just take notes.</p>
            <br>
            <h4 style="color:#00d0ff;">❓ Can I customize the complexity?</h4>
            <p>Yes. Using the <b>Intel Depth</b> slider, you can dictate the resolution of your map. <b>Level 1</b> offers a high-level reconnaissance, while <b>Level 3</b> generates a deep-dive technical extraction for complex mastery.</p>
            <br>
            <h4 style="color:#00d0ff;">❓ Why a visual map instead of notes?</h4>
            <p>Because knowing <i>what</i> to learn is often harder than the learning itself. Visualizing the hierarchy of information helps you see the pillars that support a subject before you dive into the details.</p>
            <br>
            <h4 style="color:#00d0ff;">❓ Can I save my maps?</h4>
            <p>Yes. Every map generated is logged in your <b>Archive Logs</b>. You can instantly redeploy any previous subject target from the sidebar at any time.</p>
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
        
        # --- COMPLEXITY SLIDER ---
        complexity = st.slider(
            "INTEL_DEPTH", 
            min_value=1, 
            max_value=3, 
            value=1, 
            help="1: General Knowledge | 2: Intermediate | 3: Complex Insight"
        )
        
        if st.button("RUN_ARCHITECT"):
            if topic:
                with st.spinner("INITIATING GEMINI ARCHITECT..."):
                    # Pass the complexity value to your Gemini function
                    raw_tree = generate_learning_map(topic, complexity)
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