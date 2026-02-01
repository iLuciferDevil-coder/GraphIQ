import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import CodeInterpreter
import os

# --- 1. CYBERPUNK UI & LINKEDIN BRANDING ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff !important; }
    
    /* Sidebar Visibility & Neon Green Contrast */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #39FF14 !important;
    }
    [data-testid="stSidebar"] * {
        color: #39FF14 !important;
    }
    
    /* Global High-Contrast Text */
    label, .stMarkdown, .stSubheader, p, span, .stMetric { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
    }

    /* Futuristic Neon Green Buttons */
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

    /* Hero Branding Section */
    .hero-box {
        padding: 50px 20px;
        text-align: center;
        background: radial-gradient(circle at center, rgba(57, 255, 20, 0.1) 0%, rgba(5, 5, 5, 0) 75%);
        margin-bottom: 20px;
    }

    /* Clickable Sid Signature Pill */
    .sid-link { 
        position: fixed; bottom: 25px; right: 25px; 
        text-decoration: none !important; z-index: 1000; 
        transition: transform 0.3s ease; 
    }
    .sid-link:hover { transform: scale(1.05); }
    .sid-pill {
        background: rgba(0, 0, 0, 0.95); padding: 12px 24px;
        border-radius: 50px; border: 1px solid #39FF14;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.4);
        display: flex; align-items: center; gap: 12px;
    }
    .rotating-atom { animation: spin 4s linear infinite; font-size: 24px; color: #39FF14; }
    @keyframes spin { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
    </style>

    <div class="hero-box">
        <h1 style="font-size: 4rem; font-weight: 800; color: #39FF14; margin-bottom:0; text-shadow: 0 0 15px rgba(57, 255, 20, 0.6);">GraphIQ</h1>
        <p style="font-size: 1.4rem; color: #888888;">Next-Gen Data Storytelling Agent</p>
    </div>

    <a href="https://www.linkedin.com/in/jedisuperman" target="_blank" class="sid-link">
        <div class="sid-pill">
            <span class="rotating-atom">⚛️</span>
            <div>
                <div style="font-size: 9px; text-transform: uppercase; color: #39FF14; letter-spacing: 1.2px;">Created by</div>
                <div style="font-weight: 700; font-size: 14px; color: white;">Sidd Bhattacharjee</div>
                <div style="font-size: 10px; color: #94a3b8;">your next gen AI tech marketer</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- 2. MAIN WORKFLOW ---
file = st.file_uploader("📂 Upload Dataset (CSV/XLSX)", type=["csv", "xlsx"])

if not file:
    cols = st.columns(3)
    with cols[0]: st.markdown("#### 🟢 Step 1: Ingest\nUpload messy spreadsheets effortlessly.")
    with cols[1]: st.markdown("#### 🧠 Step 2: Ask\n'Show me sales trends over time'.")
    with cols[2]: st.markdown("#### 🎨 Step 3: Visualize\nAI builds interactive neon charts.")
else:
    try:
        # Data Processing
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        with st.expander("🔍 View Raw Data Preview"):
            st.dataframe(df.head(5), width='stretch')

        query = st.text_input("💬 What insight should GraphIQ reveal?", placeholder="e.g., Show a 3D scatter plot of Revenue vs Marketing Spend")

        col_run, col_reset = st.columns([4, 1])
        
        with col_run:
            if st.button("🚀 Synthesize Visualization", width='stretch'):
                if not query:
                    st.warning("Please enter a question first.")
                else:
                    with st.status("Engine: Llama 3.3 Versatile Processing...", expanded=True):
                        try:
                            # Setting key globally fixes the init() argument error
                            os.environ["E2B_API_KEY"] = st.secrets["E2B_API_KEY"]
                            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                            
                            MODEL_ID = "llama-3.3-70b-versatile"
                            
                            sys_prompt = f"""
                            You are a Data Scientist. Write ONLY python code using plotly.express. 
                            Data: 'data.csv'. Columns: {df.columns.tolist()}. 
                            Goal: {query}.
                            Force template='plotly_dark' and neon green (#39FF14) accents.
                            The final line must be 'fig.show()'.
                            """
                            
                            response = client.chat.completions.create(
                                messages=[{"role": "user", "content": sys_prompt}],
                                model=MODEL_ID,
                                temperature=0.1
                            )
                            code = response.choices[0].message.content.replace("```python", "").replace("```", "").strip()
                            
                            # THE FIX: CodeInterpreter handles background arguments automatically
                            with CodeInterpreter() as sandbox:
                                sandbox.upload_file(file)
                                result = sandbox.notebook.exec_cell(code)
                                
                                if result.results:
                                    st.plotly_chart(result.results[0].plotly, width='stretch')
                                    st.success("Vision synthesized successfully!")
                                else:
                                    st.error("Engine failure: Logic executed but no chart produced.")
                        except Exception as e:
                            st.error(f"⚠️ Neural Link Error: {str(e)}")
        
        with col_reset:
            if st.button("🗑 Reset", width='stretch'):
                reset_app()

    except Exception as e:
        st.error(f"File loading error: {e}")

# Sidebar Persistence
with st.sidebar:
    st.markdown("### 🧬 Memory Bank")
    if st.button("Connect Neural Link"):
        st.info("Cloud sync coming soon.")
    st.markdown("---")
    st.markdown("### 🛠 Tools")
    if st.button("🗑 Reset Engine"):
        reset_app()
