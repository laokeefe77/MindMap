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
        .main-title {
            text-shadow: 0 0 20px rgba(0, 136, 255, 0.6);
            animation: flicker 3s infinite;
        }

        @keyframes flicker {
            0% { opacity: 1; }
            5% { opacity: 0.9; }
            10% { opacity: 1; }
            15% { opacity: 0.8; }
            20% { opacity: 1; }
            100% { opacity: 1; }
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
                    'font-size': '10px', 
                    'text-valign': 'center', 
                    'text-halign': 'right', 
                    'font-family': 'monospace', 
                    'border-width': 1, 
                    'border-color': '#00a0ff', 
                    'shadow-blur': 10, 
                    'shadow-color': '#0088ff' 
                }} }},
                {{ selector: 'edge', style: {{ 
                    'width': 1, 
                    'line-color': 'rgba(0, 150, 255, 0.15)', 
                    'curve-style': 'haystack', /* Haystack is faster and helps prevent clumping */
                }} }},
                {{ selector: ':selected', style: {{ 'background-color': '#00ffff', 'shadow-blur': 20 }} }}
            ],
            layout: {{ 
                name: 'cose', 
                animate: true, 
                refresh: 4,
                fit: true, 
                padding: 80,
                
                /* --- THE CLUMP KILLER SETTINGS --- */
                nodeOverlap: 100,           // Physical buffer: nodes literally cannot touch
                nodeRepulsion: 10000000,    // Force pushing all nodes apart
                idealEdgeLength: 150,       // Distance of the connections
                edgeElasticity: 100,        // Force that pulls them back (increased for stability)
                nestingFactor: 1.2,         // Multiplier for repulsion of nested (small) nodes
                gravity: 1,                 // Pulls everything to center so they don't fly off
                numIter: 4000,              // More time to resolve overlaps
                initialTemp: 1000,          // Explosive start to separate overlapping nodes
                coolingFactor: 0.95         // Slow settle down
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
    
    # Custom CSS for the Space Title
    st.markdown("""
        <style>
        .hero-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
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

        .section {
            padding: 100px 10%;
            text-align: center;
        }

        .section-dark {
            background: rgba(0,0,0,0.6);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit,minmax(250px,1fr));
            gap: 40px;
            margin-top: 50px;
        }

        .feature-card {
            padding: 25px;
            border: 1px solid rgba(0,150,255,0.3);
            box-shadow: 0 0 15px rgba(0,150,255,0.2);
        }

        .faq-item {
            max-width: 800px;
            margin: 40px auto;
            text-align: left;
        }
        </style>
        
        
        <!-- HERO -->
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


    # ✅ KEEP BUTTON FUNCTIONAL
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 LAUNCH ARCHITECT"):
            st.session_state.page = "signup"
            st.rerun()


    # ----------------------------
    # FEATURES
    # ----------------------------
st.markdown("""
<style>
    /* Container Styling */
    .section-dark {
        background-color: #0e1117;
        padding: 50px 20px;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
    }
    
    .section-dark h2 {
        text-align: center;
        color: #ffffff;
        font-size: 2.5rem;
        margin-bottom: 40px;
        letter-spacing: -1px;
    }

    /* Grid Layout */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 25px;
        max-width: 1100px;
        margin: 0 auto;
    }

    /* Card Styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        transition: all 0.3s ease;
        text-align: left;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.1);
        border-color: #7d2ae8; /* Space purple glow */
        box-shadow: 0 10px 30px rgba(125, 42, 232, 0.2);
    }

    .feature-card h3 {
        color: #ffffff;
        font-size: 1.4rem;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .feature-card p {
        color: #a1a1aa;
        line-height: 1.6;
        font-size: 1rem;
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
        <div class="feature-card">
            <h3>🌌 Scalable Knowledge</h3>
            <p>Seamlessly bridge the gap between absolute beginner and true mastery.</p>
        </div>
        <div class="feature-card">
            <h3>🔒 Personal System</h3>
            <p>Your data is yours. Secure, private, and hosted within your own universe.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


    # ----------------------------
    # PHILOSOPHY / SLOGANS
    # ----------------------------
st.markdown("""
        <div class="section">

            <h2>Our Philosophy</h2>

            <p style="color:#88ccff; font-size:20px; margin-top:30px;">
                “Build systems. Not notes.”
            </p>

            <p style="color:#88ccff; font-size:20px;">
                “Clarity is engineered.”
            </p>

            <p style="color:#88ccff; font-size:20px;">
                “Learning is architecture.”
            </p>

        </div>
    """, unsafe_allow_html=True)


    # ----------------------------
    # FAQ
    # ----------------------------
st.markdown("""
        <div class="section section-dark">

            <h2>Frequently Asked Questions</h2>

            <div class="faq-item">
                <h4>❓ What is Nebula?</h4>
                <p>An AI-powered knowledge mapping system.</p>
            </div>

            <div class="faq-item">
                <h4>❓ Who is it for?</h4>
                <p>Students, researchers, and self-learners.</p>
            </div>

            <div class="faq-item">
                <h4>❓ Is my data safe?</h4>
                <p>Your maps remain private.</p>
            </div>

            <div class="faq-item">
                <h4>❓ Is it free?</h4>
                <p>Currently in beta access.</p>
            </div>

        </div>
    """, unsafe_allow_html=True)


    # ----------------------------
    # CALL TO ACTION
    # ----------------------------
st.markdown("""
        <div class="section">

            <h2>Start Building Your Knowledge System</h2>

            <p style="color:#99ccff; max-width:600px; margin:20px auto;">
                Transform how you learn. Design how you think.
            </p>

        </div>
    """, unsafe_allow_html=True)


    # ✅ KEEP SECOND BUTTON WORKING
col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("✨ GET STARTED"):
            st.session_state.page = "signup"
            st.rerun()


    # Centering the button using Streamlit columns
    _, col2, _ = st.columns([1, 0.6, 1])
    with col2:
        if st.button("LAUNCH ARCHITECT"): 
            st.session_state.page = "signup"
            st.rerun()

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