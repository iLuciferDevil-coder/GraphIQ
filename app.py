import streamlit as st
import pandas as pd
from groq import Groq
from e2b_code_interpreter import Sandbox
import os

# --- UI CONFIG ---
st.set_page_config(page_title="GraphIQ", page_icon="📊", layout="wide")
st.markdown("""
    <style>
    .main { background: #0e1117; color: white; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: #00f2fe; border: 1px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 GraphIQ")

# Load Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")

uploaded_file = st.file_uploader("Upload Data", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(5))
    
    query = st.text_input("Ask GraphIQ to visualize something:", "Show me a distribution of the data")

    if st.button("Generate Vision"):
        with st.status("Agentic Process Running...", expanded=True):
            # 1. Prepare Data Context
            columns = df.columns.tolist()
            
            # 2. Setup the Brain (Groq)
            client = Groq(api_key=GROQ_API_KEY)
            prompt = f"""
            You are a Senior Data Scientist. Write Python code using 'plotly' to visualize: {query}.
            The data is in a file named 'data.csv'. The columns are: {columns}.
            Only output the code. No explanation.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            code = chat_completion.choices[0].message.content.replace("```python", "").replace("```", "")

            # 3. Setup the Hands (E2B)
            with Sandbox(api_key=E2B_API_KEY) as sandbox:
                sandbox.upload_file(uploaded_file) # Uploading data to the sandbox
                execution = sandbox.notebook.exec_cell(code)
                
                if execution.results:
                    # Display the first result (usually the chart)
                    st.plotly_chart(execution.results[0].plotly)
                else:
                    st.error("Visualization failed. Refining logic...")
