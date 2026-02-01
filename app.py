import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- 1. CYBERPUNK UI & HIGH-CONTRAST TEXT ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    /* Main App Background */
    .stApp { background: #050505; color: #ffffff !important; }
    
    /* FIX: Sidebar Contrast & Visibility */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #39FF14 !important;
    }
    [data-testid="stSidebar"] * {
        color: #39FF14 !important; /* Neon Green for Sidebar text */
    }
    
    /* Global Text Overrides */
    label, .stMarkdown, .stSubheader, p, span, .stMetric { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
    }

    /* Futuristic Buttons */
    button[kind="secondary"] {
        color: #39FF14 !important;
        border-color: #39FF14 !important;
        background-color: rgba(57, 255, 20, 0.05) !important;
    }
    
    .stFileUploader section {
        background-color: #111111 !important;
        border: 1px dashed #39FF14 !important;
        color: #ffffff !important;
    }

    /* Hero Section */
    .hero-box {
        padding: 50px 20px;
        text-align: center;
        background: radial-gradient(circle at center, rgba(57, 255, 20, 0.1) 0%, rgba(5, 5, 5, 0) 75%);
        margin-bottom: 20px;
    }

    /* Clickable Sid Signature */
    .sid-link { position: fixed; bottom: 25px; right: 25px; text-decoration: none !important; z-index: 1000; }
    .sid-pill {
        background: rgba(0, 0, 0, 0.9); padding: 12px 24px;
        border-radius: 50px; border: 1px solid #39FF14;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.4);
        display: flex; align-items: center; gap: 12px;
    }
    .rotating-atom { animation: spin 4s linear infinite; font-size: 24px; color: #39FF14; }
    @keyframes spin { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
    </style>

    <div class="hero-box">
        <h1 style="font-size: 3.5rem; font-weight: 800; color: #39FF14; margin-bottom:0; text-shadow: 0 0 10px rgba(57, 255, 20, 0.5);">GraphIQ</h1>
        <p style="font-size: 1.2rem; color: #888888;">Instant Data Storytelling Agent</p>
    </div>

    <a href="https://www.linkedin.com/in/jedisuperman" target="_blank" class="sid-link">
        <div class="sid-pill">
            <span class="rotating-atom">⚛️</span>
            <div>
                <div style="font-size: 9px; text-transform: uppercase; color: #39FF14; letter-spacing: 1.2px;">Created by</div>
                <div style="font-weight: 700; font-size: 14px; color: white;">Sidd Bhattacharjee</div>
                <div style="font-size: 10px; color: #888888;">your next gen AI tech marketer</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# --- 2. THE RESET ENGINE ---
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- 3. MAIN WORKFLOW ---
file = st.file_uploader("📂 Upload your dataset to begin", type=["csv", "xlsx"])

if not file:
    cols = st.columns(3)
    with cols[0]: st.markdown("#### 🟢 Step 1: Ingest\nUpload messy spreadsheets effortlessly.")
    with cols[1]: st.markdown("#### 🧠 Step 2: Ask\n'Show me sales trends over time'.")
    with cols[2]: st.markdown("#### 🎨 Step 3: Visualize\nAI builds interactive neon charts.")
else:
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.markdown("### 🔍 Data Preview")
        st.dataframe(df.head(5), use_container_width=True)

        query = st.text_input("💬 What insight should GraphIQ reveal?", placeholder="e.g., Show me a 3D scatter plot of the revenue")

        col_run, col_reset = st.columns([4, 1])
        
        with col_run:
            if st.button("🚀 Synthesize Visualization", use_container_width=True):
                with st.status("Agent is synthesizing...", expanded=True):
                    try:
                        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                        sys_prompt = f"Write ONLY python code using plotly.express. Data is in 'data.csv'. Columns: {df.columns.tolist()}. User wants: {query}. Force template='plotly_dark' with color_discrete_sequence=['#39FF14', '#00F2FE']. The final line must be 'fig.show()'."
                        
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": sys_prompt}],
                            model="llama3-70b-8192",
                            temperature=0.1
                        )
                        code = response.choices[0].message.content.replace("```python", "").replace("```", "").strip()
                        
                        with Sandbox(api_key=os.getenv("E2B_API_KEY")) as sandbox:
                            sandbox.upload_file(file)
                            result = sandbox.notebook.exec_cell(code)
                            if result.results:
                                st.plotly_chart(result.results[0].plotly, use_container_width=True)
                                st.success("Vision synthesized successfully!")
                            else:
                                st.error("Engine failure: Code executed but no chart was produced.")
                    except Exception as e:
                        st.error(f"⚠️ Error Detected: {str(e)}")
        
        with col_reset:
            if st.button("🗑 Reset", use_container_width=True):
                reset_app()

    except Exception as e:
        st.error(f"File loading error: {e}")

# Sidebar reset (Now visible with Neon Green text)
with st.sidebar:
    st.markdown("### 🧬 Memory Bank")
    st.write("Your sessions are volatile. Link your identity to save.")
    if st.button("Connect Neural Link"):
        st.info("Auth integration coming soon.")
    st.markdown("---")
    if st.button("🗑 Reset Engine"):
        reset_app()
