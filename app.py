import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- 1. INTUITIVE UI & HERO SECTION ---
st.set_page_config(page_title="GraphIQ | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #e2e8f0; }
    
    /* Hero Section Styling */
    .hero-container {
        padding: 60px 20px;
        text-align: center;
        background: linear-gradient(180deg, rgba(59, 130, 246, 0.1) 0%, rgba(11, 14, 20, 0) 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    
    /* Hide the sidebar by default to keep focus on the data */
    [data-testid="stSidebar"] { display: none; }
    
    .sid-signature {
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(30, 41, 59, 0.9); padding: 12px 24px;
        border-radius: 50px; border: 1px solid #3b82f6; z-index: 1000;
        display: flex; align-items: center; gap: 12px;
    }
    .rotating-atom { animation: spin 4s linear infinite; font-size: 24px; }
    @keyframes spin { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
    </style>
    
    <div class="hero-container">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">⚛️ GraphIQ</h1>
        <p style="font-size: 1.2rem; color: #94a3b8;">Transform raw data into professional insights in seconds.</p>
        <p style="font-size: 0.9rem; color: #3b82f6; font-weight: bold;">No login required to start.</p>
    </div>

    <div class="sid-signature">
        <span class="rotating-atom">⚛️</span>
        <div>
            <div style="font-size: 10px; text-transform: uppercase; color: #3b82f6;">Created by</div>
            <div style="font-weight: bold; font-size: 14px;">Sidd Bhattacharjee</div>
            <div style="font-size: 11px; color: #94a3b8;">"your next-gen AI tech marketer"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. THE CORE WORKFLOW ---
file = st.file_uploader("👆 Drag and drop your CSV or Excel file to begin", type=["csv", "xlsx"])

if not file:
    # Show three "Feature Cards" to explain what to do
    col1, col2, col3 = st.columns(3)
    with col1: st.info("**1. Upload Data**\nDrop any messy spreadsheet.")
    with col2: st.info("**2. Ask Anything**\n'Show me sales trends.'")
    with col3: st.info("**3. Get Insights**\nAI creates the perfect chart.")

if file:
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    st.success(f"Successfully loaded {file.name}")
    
    query = st.text_input("What would you like to visualize?", placeholder="e.g., Show me the top 5 performing regions by revenue")
    
    if st.button("🚀 Generate Visualization"):
        with st.status("Analyzing and Rendering...", expanded=True):
            # ... [Insert your existing Groq & E2B logic here] ...
            # For brevity, assume 'fig' is the resulting Plotly figure
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📥 Export & Save")
            
            # --- 3. THE "SMART LOGIN" MOMENT ---
            col_dl, col_save = st.columns(2)
            
            with col_dl:
                st.download_button("Download Image", data="...", file_name="chart.png")
            
            with col_save:
                # Instead of "Neural Link", use familiar language
                if st.button("💾 Save to My Account"):
                    st.markdown("""
                        <div style="padding: 20px; border: 1px solid #3b82f6; border-radius: 10px;">
                            <h4>Secure your work</h4>
                            <p>Enter your email to save this chart and create a free account.</p>
                            <input type="text" placeholder="email@example.com" style="width: 100%; padding: 10px; margin-bottom: 10px; color: black;">
                            <button style="width: 100%; padding: 10px; background: #3b82f6; color: white; border: none; border-radius: 5px;">Continue</button>
                        </div>
                    """, unsafe_allow_html=True)
