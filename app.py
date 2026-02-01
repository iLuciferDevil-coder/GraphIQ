import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- 1. UI & BRANDING ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #39FF14; }
    [data-testid="stSidebar"] * { color: #39FF14 !important; }
    .hero-box { padding: 50px 20px; text-align: center; margin-bottom: 20px; }
    .sid-pill {
        background: rgba(0, 0, 0, 0.95); padding: 12px 24px; border-radius: 50px; 
        border: 1px solid #39FF14; display: flex; align-items: center; gap: 12px;
    }
    </style>
    <div class="hero-box">
        <h1 style="font-size: 4rem; color: #39FF14; margin-bottom:0;">GraphIQ</h1>
        <p style="font-size: 1.4rem; color: #888888;">Next-Gen Data Storytelling Agent</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
file = st.file_uploader("📂 Upload Dataset", type=["csv", "xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    query = st.text_input("💬 What insight should GraphIQ reveal?")

    if st.button("🚀 Synthesize Visualization", use_container_width=True):
        with st.status("Initializing Neural Link...", expanded=True):
            try:
                # Setup Keys
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # LLM Generation
                sys_prompt = f"Write ONLY python code using plotly.express. Data: 'data.csv'. Columns: {df.columns.tolist()}. User wants: {query}. Force template='plotly_dark'. Final line: 'fig.show()'."
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": sys_prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.1
                )
                code = response.choices[0].message.content.replace("```python", "").replace("```", "").strip()

                # THE GITHUB FIX: Use Sandbox.create() instead of Sandbox()
                # This bypasses the SandboxBase.init() bug
                with Sandbox.create(api_key=st.secrets["E2B_API_KEY"]) as sandbox:
                    sandbox.upload_file(file)
                    result = sandbox.notebook.exec_cell(code)
                    if result.results:
                        st.plotly_chart(result.results[0].plotly, use_container_width=True)
                        st.success("Vision synthesized!")
            except Exception as e:
                st.error(f"⚠️ Neural Link Error: {str(e)}")
