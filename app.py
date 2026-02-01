# =========================================================
# GraphIQ — Stable AI Data Visualization App
# =========================================================

import os
import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import run

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="GraphIQ",
    page_icon="⚛️",
    layout="wide"
)

# ---------------------------------------------------------
# ENV (Streamlit-safe)
# ---------------------------------------------------------
E2B_API_KEY = st.secrets["E2B_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.markdown(
    "<h1 style='color:#39FF14'>⚛️ GraphIQ</h1>"
    "<p>Ask questions → Get instant visualizations</p>",
    unsafe_allow_html=True
)

file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
if not file:
    st.stop()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
try:
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
except Exception as e:
    st.error(f"Failed to load file: {e}")
    st.stop()

st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
st.dataframe(df.head(), width="stretch")

# ---------------------------------------------------------
# USER QUERY
# ---------------------------------------------------------
query = st.text_input(
    "What do you want to visualize?",
    placeholder="Example: Show monthly sales trend by category"
)

if not query:
    st.stop()

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if st.button("🚀 Generate Visualization", width="stretch"):

    with st.status("Thinking and executing...", expanded=True):

        # ---- LLM ----
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are a Python data visualization expert.

Rules:
- Use ONLY plotly.express
- File name is data.csv
- Available columns: {list(df.columns)}
- Use template='plotly_dark'
- Final line MUST be fig.show()
- Return ONLY Python code

User request:
{query}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        code = (
            response.choices[0].message.content
            .replace("```python", "")
            .replace("```", "")
            .strip()
        )

        # ---- E2B EXECUTION ----
        result = run(
            code,
            files={
                "data.csv": df.to_csv(index=False)
            },
            env={
                "E2B_API_KEY": E2B_API_KEY
            }
        )

        if result.results and result.results[0].plotly:
            st.plotly_chart(result.results[0].plotly, width="stretch")
            st.success("Visualization generated successfully!")
        else:
            st.error("Code executed but no chart was produced.")
