# =========================
# GraphIQ — AI Data Viz Agent
# Created by Sidd Bhattacharjee
# =========================

# ---- CRITICAL: ENV FIRST ----
import os
import streamlit as st

os.environ["E2B_API_KEY"] = st.secrets["E2B_API_KEY"]

# ---- STANDARD IMPORTS ----
import pandas as pd
import plotly.express as px
from groq import Groq
from e2b_code_interpreter import CodeInterpreterSession


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="GraphIQ | AI Data Storytelling",
    page_icon="⚛️",
    layout="wide"
)


# =========================
# STYLING (SAFE CSS)
# =========================
st.markdown("""
<style>
.stApp { background-color: #050505; color: white; }
[data-testid="stSidebar"] { background-color: #000000; }
button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown(
    """
    <h1 style="color:#39FF14; font-size:3.2rem;">⚛️ GraphIQ</h1>
    <p style="color:#9ca3af;">AI agent that understands data and builds charts</p>
    """,
    unsafe_allow_html=True
)


# =========================
# FILE UPLOAD
# =========================
file = st.file_uploader(
    "📂 Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if not file:
    st.info("Upload a dataset to begin.")
    st.stop()


# =========================
# LOAD DATA
# =========================
try:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
except Exception as e:
    st.error(f"Failed to read file: {e}")
    st.stop()

st.success(f"Loaded **{df.shape[0]} rows × {df.shape[1]} columns**")

with st.expander("🔍 Preview data"):
    st.dataframe(df.head(), width="stretch")


# =========================
# USER QUERY
# =========================
query = st.text_input(
    "💬 What do you want to visualize?",
    placeholder="Example: Show revenue trend by month"
)

if not query:
    st.stop()


# =========================
# RUN BUTTON
# =========================
if st.button("🚀 Generate Visualization", width="stretch"):

    with st.status("🧠 Thinking & generating chart...", expanded=True):

        try:
            # ---- GROQ CLIENT ----
            groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            MODEL_ID = "llama-3.3-70b-versatile"

            # ---- PROMPT ----
            system_prompt = f"""
You are a Python data visualization expert.

Rules:
- Use ONLY plotly.express
- Data file is named data.csv
- Columns available: {list(df.columns)}
- Use template='plotly_dark'
- Use color_discrete_sequence=['#39FF14', '#00F2FE', '#F97316']
- Return ONLY executable Python code
- Final line MUST be fig.show()

User request:
{query}
"""

            response = groq_client.chat.completions.create(
                model=MODEL_ID,
                messages=[{"role": "user", "content": system_prompt}],
                temperature=0.1
            )

            raw_code = response.choices[0].message.content
            code = raw_code.replace("```python", "").replace("```", "").strip()

        except Exception as e:
            st.error(f"LLM generation failed: {e}")
            st.stop()

        # =========================
        # E2B EXECUTION
        # =========================
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
                    st.error("Code ran, but no chart was produced.")

        except Exception as e:
            st.error(f"Execution error: {e}")


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("### 🧬 GraphIQ Engine")
    st.markdown("- LLM: Llama 3.3 (Groq)")
    st.markdown("- Sandbox: E2B v2.x")
    st.markdown("- Charts: Plotly")
    st.markdown("---")
    st.markdown(
        "Built by **Sidd Bhattacharjee**  \n"
        "[LinkedIn](https://www.linkedin.com/in/jedisuperman)"
    )
