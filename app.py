import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os
import base64

# --- PRO-TIER UI & BRANDING ---
st.set_page_config(page_title="GraphIQ Pro | Sidd Bhattacharjee", page_icon="⚛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f1f5f9; }
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    
    /* Branding Footer */
    .sid-signature {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(30, 41, 59, 0.9);
        padding: 12px 24px;
        border-radius: 50px;
        border: 1px solid #3b82f6;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .rotating-atom {
        animation: spin 4s linear infinite;
        font-size: 24px;
    }
    @keyframes spin { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }
    </style>
    
    <div class="sid-signature">
        <span class="rotating-atom">⚛️</span>
        <div>
            <div style="font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #3b82f6;">Created by</div>
            <div style="font-weight: bold; font-size: 14px;">Sidd Bhattacharjee</div>
            <div style="font-size: 11px; font-style: italic; color: #94a3b8;">"your next gen AI tech marketer"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: THE ANALYST'S TOOLKIT ---
with st.sidebar:
    st.title("🚀 GraphIQ Pro")
    st.markdown("---")
    
    with st.expander("🛡️ Data Governance", expanded=True):
        auto_clean = st.toggle("Auto-Fix Missing Values", value=True)
        detect_outliers = st.toggle("Highlight Anomalies", value=False)
    
    with st.expander("🎭 Visual Identity"):
        viz_style = st.selectbox("Style Preset", ["Cyberpunk Neon", "Glassmorphic", "Executive (Clean)", "High-Contrast"])
        chart_res = st.select_slider("Export Resolution", options=["Standard", "4K Ultra"])

# --- MAIN CANVAS ---
col_main, col_tools = st.columns([3, 1])

with col_main:
    st.title("⚛️ Strategic Intelligence Hub")
    
    file = st.file_uploader("Upload Dataset (CSV/XLSX)", type=["csv", "xlsx"])

    if file:
        # Load Data
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        # PRO FEATURE: Smart Tabbed Interface
        tab1, tab2, tab3 = st.tabs(["📊 Visualization Canvas", "🧹 Data Health", "📝 Executive Summary"])
        
        with tab1:
            query = st.text_input("What is your analytical objective?", placeholder="e.g., 'Visualize the Pareto distribution of sales by category'")
            
            if st.button("Generate Pro Visualization"):
                with st.status("Engine: Llama3-70b Processing...", expanded=True):
                    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                    
                    # PRO PROMPT: Includes data cleaning instructions
                    sys_instr = f"""
                    You are a Principal Data Scientist. Write Python code using Plotly.
                    Style: {viz_style}. Data: 'data.csv'. Columns: {df.columns.tolist()}.
                    1. Clean data: Remove NaNs for the requested columns.
                    2. Visualization: Create a stunning {viz_style} chart for {query}.
                    3. Analytics: Add a trendline if applicable.
                    Output ONLY valid code. No text.
                    """
                    
                    res = client.chat.completions.create(
                        messages=[{"role": "system", "content": sys_instr}, {"role": "user", "content": query}],
                        model="llama3-70b-8192"
                    )
                    code = res.choices[0].message.content.replace("```python", "").replace("```", "")
                    
                    with Sandbox(api_key=os.getenv("E2B_API_KEY")) as sandbox:
                        sandbox.upload_file(file)
                        execution = sandbox.notebook.exec_cell(code)
                        if execution.results:
                            st.plotly_chart(execution.results[0].plotly, use_container_width=True)
                            
                            # PRO FEATURE: Download as HTML
                            chart_html = execution.results[0].plotly.to_html()
                            st.download_button("📥 Export Interactive Chart (HTML)", data=chart_html, file_name="graphiq_export.html", mime="text/html")

        with tab2:
            st.subheader("Data Quality Audit")
            st.write(df.describe())
            st.warning(f"Detected {df.isnull().sum().sum()} missing values across all columns.")

        with tab3:
            st.subheader("AI Narrative")
            # This would call the LLM to write a text summary of the df.head() and df.describe()
            st.info("The AI detects a strong upward trend in 'Revenue' particularly in Q4. (Sample Insight)")

with col_tools:
    if file:
        st.markdown("### 🛠️ Quick Actions")
        if st.button("🪄 Auto-Suggest Charts"):
            st.write("1. Revenue vs Time (Line)")
            st.write("2. Category Split (Donut)")
        
        st.markdown("---")
        st.markdown("### 📋 Export Hub")
        st.button("📄 Generate PDF Report (Coming Soon)")
        st.button("📽️ Create Animated GIF")
