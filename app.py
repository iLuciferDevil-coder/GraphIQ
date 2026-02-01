import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- PREMIUM BRANDING & UI CONFIG ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="🚀", layout="wide")

# Futuristic CSS with Sid's Branding styles
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #0b0e14; color: #e2e8f0; }
    
    /* Sid's Branding Footer */
    .sid-footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 14px;
        color: #94a3b8;
        background: rgba(15, 23, 42, 0.8);
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid #334155;
        backdrop-filter: blur(5px);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Moving Icon Animation */
    .moving-icon {
        animation: rotate 3s linear infinite;
        display: inline-block;
        font-size: 20px;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    
    /* Premium Dashboard Cards */
    .data-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
    }
    </style>
    
    <div class="sid-footer">
        Created by <strong>Sidd Bhattacharjee</strong> 
        <span style="color:#3b82f6;">"your next gen AI tech marketer"</span> 
        <span class="moving-icon">⚛️</span>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PRODUCT CONFIGURATION ---
with st.sidebar:
    st.title("⚙️ GraphIQ Pro")
    st.markdown("---")
    
    with st.expander("🛠 Engine Settings", expanded=True):
        model_choice = st.selectbox("LLM Brain", ["Llama3-70b-8192 (Genius)", "Llama3-8b-8192 (Fast)"])
        temp = st.slider("Creativity Level", 0.0, 1.0, 0.2)
    
    with st.expander("🎨 Visual Identity"):
        viz_theme = st.selectbox("Color Palette", ["Neon Night", "Deep Space", "Arctic Frost", "Solaris"])
        show_code = st.checkbox("Show AI Logic (Code)", value=False)

    st.markdown("---")
    if st.button("🗑 Clear Session"):
        st.rerun()

# --- MAIN WORKSPACE ---
col_main, col_stats = st.columns([3, 1])

with col_main:
    st.markdown("# ⚛️ GraphIQ Intelligence")
    st.caption("Advanced Data Visualization for the Next Gen Enterprise")
    
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # UI: Smart Data Preview
        st.markdown('<div class="data-card"><h4>Live Data Stream</h4></div>', unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)
        
        # User Interaction
        query = st.text_input("Describe the visualization or business question:", placeholder="e.g., 'Compare quarterly growth
