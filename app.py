import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #0b0e14; color: #e2e8f0; }
    
    /* Hide sidebar on landing */
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1f2937; }

    /* Hero Section */
    .hero-box {
        padding: 60px 20px;
        text-align: center;
        background: radial-gradient(circle at center, rgba(59, 130, 246, 0.12) 0%, rgba(11, 14, 20, 0) 70%);
        margin-bottom: 30px;
    }

    /* Clickable Sid Signature */
    .sid-link {
        position: fixed; bottom: 25px; right: 25px;
        text-decoration: none !important; z-index: 1000;
        transition: transform 0.3s ease;
    }
    .sid-link:hover { transform: scale(1.05); }
    .sid-pill {
        background: rgba(17, 24, 39, 0.9); padding: 12px 24px;
        border-radius: 50px; border: 1px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        display: flex; align-items: center; gap: 12px;
    }
    
    .rotating-atom { animation: spin 4s linear infinite; font-size: 24px; }
    @keyframes spin { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
    
    /* Input Styling */
    .stTextInput>div>div>input { background: #1f2937; color: white; border: 1px solid #374151; }
    </style>

    <div class="hero-box">
        <h1 style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(to right, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:0;">
            GraphIQ
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; margin-top: 10px;">
            The next-gen AI agent for instant data storytelling. 
        </p>
    </div>

    <a href="https://www.linkedin.com/in/jedisuperman" target="_blank" class="sid-link">
        <div class="sid-pill">
            <span class="rotating-atom">⚛️</span>
            <div>
                <div style="font-size: 9px; text-transform: uppercase; color: #3b82f6; letter-spacing: 1.2px;">Created by</div>
                <div style="font-weight: 700; font-size: 14px; color: white;">Sidd Bhattacharjee</div>
                <div style="font-size: 10px; color: #94a3b8;">your next gen AI tech marketer</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# --- 2. LOGIC & WORKFLOW ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")

# Initialization of Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Main Layout
file = st.file_uploader("📂 Drop your dataset here (CSV or XLSX)", type=["csv", "xlsx"])

if not file:
    cols = st.columns(3)
    with cols[0]: st.markdown("### 1. Ingest\nUpload messy spreadsheets effortlessly.")
    with cols[1]: st.markdown("### 2. Ask\nAsk anything: 'Show me YoY growth'.")
    with cols[2]: st.markdown("### 3. Visualize\nAI builds interactive Plotly charts.")
else:
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    
    with st.expander("🔍 View Raw Data Preview"):
        st.dataframe(df.head(10), use_container_width=True)

    query = st.text_input("💬 What insight should GraphIQ reveal?", placeholder="e.g., Show a correlation heatmap of all numerical columns")

   if st.button("🚀 Synthesize Visualization"):
        if not query:
            st.warning("Please enter a question first.")
        else:
            with st.status("GraphIQ Agent is thinking...", expanded=True):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    
                    # Updated Model String and escaped braces for safety
                    model_to_use = "llama3-70b-8192" 
                    
                    sys_msg = f"""
                    You are a Senior Data Scientist. Write Python code using Plotly to visualize: {query}.
                    Data is in 'data.csv'. Columns: {df.columns.tolist()}.
                    - Use a dark theme (plotly_dark).
                    - Use vibrant colors like #00f2fe and #4facfe.
                    - Output ONLY the python code starting with 'import plotly'. 
                    - Do not include any markdown backticks or explanations.
                    """
                    
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": sys_msg},
                            {"role": "user", "content": query}
                        ],
                        model=model_to_use,
                        temperature=0.2 # Lower temperature for more stable code generation
                    )
                    
                    # Clean the response to ensure only pure code remains
                    raw_code = response.choices[0].message.content
                    code = raw_code.replace("```python", "").replace("```", "").strip()
                    
                    with Sandbox(api_key=E2B_API_KEY) as sandbox:
                        sandbox.upload_file(file)
                        result = sandbox.notebook.exec_cell(code)
                        
                        if result.results:
                            st.plotly_chart(result.results[0].plotly, use_container_width=True)
                            
                            # Export Section
                            st.markdown("---")
                            html_bytes = result.results[0].plotly.to_html().encode()
                            st.download_button("💾 Download Interactive Chart", data=html_bytes, file_name="graphiq_viz.html", mime="text/html")
                        else:
                            st.error("The agent generated code, but it didn't produce a chart. Try rephrasing your request.")
                            
                except Exception as e:
                    st.error(f"Neural Link Error: {str(e)}")
                    st.info("Tip: Ensure your GROQ_API_KEY is correct in Streamlit Secrets.")
