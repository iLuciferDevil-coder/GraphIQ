# =========================================================
# GraphIQ — AI Data Visualization Agent
# Author: Sidd Bhattacharjee
# =========================================================

# -------- ENV FIRST (ABSOLUTELY REQUIRED) --------
import os
import streamlit as st

os.environ["E2B_API_KEY"] = st.secrets["E2B_API_KEY"]

# -------- STANDARD IMPORTS --------
import pandas as pd
import plotly.express as px
from groq import Groq
from e2b import CodeInterpreterSession


# =========================================================
# STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="GraphIQ | AI Data Storytelling",
    page_icon="⚛️",
    layout="wide"
)

# -------- BASIC DARK THEME --------
st.markdown(
    """
    <style>
        .stApp { background-color: #050505; color: white; }
        [data-testid="stSidebar"] { background-color: #000000; }
        button { border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <h1 style="color:#39FF14; font-size:3rem;">⚛️ GraphIQ</h1>
    <p style="color:#9ca3af;">
        Upload data → ask a question → get an intelligent chart
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FILE UPLOAD
# =========================================================
file = st.file_uploader(
    "📂 Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

if not file:
    st.info("Please upload a dataset to begin.")
    st.stop()

# =========================================================
# LOAD DATA
# =========================================================
try:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
except Exception as e:
    st.error(f"Failed to load file: {e}")
    st.stop()

st.success(f"Loaded **{df.shape[0]} rows × {df.shape[1]} columns**")

with st.expander("🔍 Preview data"):
    st.dataframe(df.head(), width="stretch")

# =========================================================
# USER QUERY
# =========================================================
query = st.text_input(
    "💬 What would you like to visualize?",
    placeholder="Example: Show monthly revenue trend by category"
)

if not query:
    st.stop()

# =========================================================
# ACTION BUTTON
# =========================================================
if st.button("🚀 Generate Visualization", width="stretch"):

    with st.status("🧠 Thinking and building chart...", expanded=True):

        # -----------------------------
        # 1. CALL GROQ (LLM → CODE)
        # -----------------------------
        try:
            groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            MODEL_ID = "llama-3.3-70b-versatile"

            prompt = f"""
You are a senior Python data visualization engineer.

STRICT RULES:
- Use ONLY plotly.express
- Data file name is data.csv
- Available columns: {list(df.columns)}
- Use template='plotly_dark'
- Use color_discrete_sequence=['#39FF14', '#00F2FE', '#F97316']
- Return ONLY executable Python code
- Final line MUST be fig.show()

User request:
{query}
"""

            response = groq_client.chat.completions.create(
                model=MODEL_ID,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )

            raw_code = response.choices[0].message.content
            code = raw_code.replace("```python", "").replace("```", "").strip()

        except Exception as e:
            st.error(f"LLM generation failed: {e}")
            st.stop()

        # -----------------------------
        # 2. EXECUTE SAFELY VIA E2B
        # -----------------------------
        try:
            with CodeInterpreterSession() as session:
                session.upload_file(
                    "data.csv",
                    df.to_csv(index=False)
                )

                execution = session.run(code)

                if execution.results and execution.results[0].plotly:
                    st.plotly_chart(
                        execution.results[0].plotly,
                        width="stretch"
                    )
                    st.success("Visualization generated successfully!")
                else:
                    st.error("Code executed but no chart was produced.")

        except Exception as e:
            st.error(f"Execution error: {e}")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### 🧬 GraphIQ Engine")
    st.markdown("- **LLM:** Groq · Llama 3.3")
    st.markdown("- **Execution:** E2B Code Interpreter")
    st.markdown("- **Charts:** Plotly")
    st.markdown("---")
    st.markdown(
        "Built by **Sidd Bhattacharjee**  \n"
        "[LinkedIn](https://www.linkedin.com/in/jedisuperman)"
    )
