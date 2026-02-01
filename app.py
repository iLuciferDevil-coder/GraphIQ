with st.status("Engine: Llama 3.3 Versatile Processing...", expanded=True):
                    try:
                        # 2026 Production Standards: Set API Key globally
                        os.environ["E2B_API_KEY"] = os.getenv("E2B_API_KEY")
                        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                        
                        # Use the most stable production model
                        MODEL_ID = "llama-3.3-70b-versatile"
                        
                        sys_prompt = f"Write ONLY python code using plotly.express. Data: 'data.csv'. Columns: {df.columns.tolist()}. User wants: {query}. Force template='plotly_dark' with color_discrete_sequence=['#39FF14', '#00F2FE']. Final line must be 'fig.show()'."
                        
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": sys_prompt}],
                            model=MODEL_ID,
                            temperature=0.1
                        )
                        code = response.choices[0].message.content.replace("```python", "").replace("```", "").strip()
                        
                        # THE FINAL FIX: Using CodeInterpreter specifically for version 2.4.1+
                        from e2b_code_interpreter import CodeInterpreter
                        with CodeInterpreter() as sandbox:
                            sandbox.upload_file(file)
                            result = sandbox.notebook.exec_cell(code)
                            
                            if result.results:
                                st.plotly_chart(result.results[0].plotly, use_container_width=True)
                                st.success("Vision synthesized successfully!")
                            else:
                                st.error("Engine failure: Logic executed but no chart was produced.")
                    except Exception as e:
                        st.error(f"⚠️ Neural Link Error: {str(e)}")
