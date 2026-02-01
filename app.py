import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import CodeInterpreter
import os

# --- FUTURISTIC UI CONFIG ---
st.set_page_config(page_title="GraphIQ", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 20px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 GraphIQ: AI Data Visionary")
st.subheader("Upload your data and let the agent reveal the story.")

# --- SIDEBAR / CREDENTIALS ---
with st.sidebar:
    st.header("Control Center")
    # In production, we pull from Secrets. For now, we use the ones you provided.
    groq_key = os.getenv("GROQ_API_KEY")
    e2b_key = os.getenv("E2B_API_KEY")
    st.success("GraphIQ Neural Link: Active" if groq_key and e2b_key else "Neural Link: Offline")

# --- DATA UPLOAD ---
uploaded_file = st.file_uploader("Drop your CSV or Excel file here", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.write("### Data Preview", df.head())
    
    user_query = st.text_input("What insight are you looking for?", "Create a beautiful trend chart for sales over time")

    if st.button("Generate Visualization"):
        with st.status("GraphIQ is thinking...", expanded=True) as status:
            st.write("Analyzing data structures...")
            # This is where we will add the AI logic in the next step!
            st.info("Neural engine ready. Awaiting logic injection.")
