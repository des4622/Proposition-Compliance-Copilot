import streamlit as st
import os
import pandas as pd
import plotly.express as px
import numpy as np
from rag_engine import load_and_vectorize_data, query_vectorstore
from langchain_ollama import ChatOllama

# Set page config
st.set_page_config(page_title="Zurich Proposition Co-Pilot", page_icon="🛡️", layout="wide")

st.title("🛡️ Life Insurance Proposition Intelligence & Compliance Co-Pilot")
st.markdown(
    "Designed to accelerate market research, drafting, and regulatory compliance for Life Insurance products. (Powered by 100% Local AI)")

# Initialize session state for vectorstores
if 'comp_vectorstore' not in st.session_state:
    with st.spinner("Loading Competitor Data (this may take 10-20 seconds on first run)..."):
        try:
            st.session_state.comp_vectorstore = load_and_vectorize_data("./data/competitors", "competitors")
        except Exception as e:
            st.error(f"Error loading competitors: {e}. Please ensure PDFs are in the ./data/competitors folder.")

if 'reg_vectorstore' not in st.session_state:
    with st.spinner("Loading Regulatory Guidelines (GN16, FTC)..."):
        try:
            st.session_state.reg_vectorstore = load_and_vectorize_data("./data/regulations", "regulations")
        except Exception as e:
            st.error(
                f"Error loading regulations: {e}. Please ensure TXT/PDF files are in the ./data/regulations folder.")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Market Intelligence", "📝 Brochure & Compliance Checker", "📊 Product Analytics"])

# --- TAB 1: Market Intelligence ---
with tab1:
    st.header("Competitor Product Analysis")
    query = st.text_input("Ask a question about the uploaded competitor products:",
                          placeholder="e.g., What are the key exclusions and waiting periods for young professionals?")
    if st.button("Analyze"):
        if query and 'comp_vectorstore' in st.session_state:
            with st.spinner("Analyzing documents..."):
                result = query_vectorstore(st.session_state.comp_vectorstore, query)
                st.write("**Answer:**", result['result'])
                with st.expander("View Source Documents"):
                    for doc in result['source_documents']:
                        st.write(f"- {doc.metadata.get('source', 'Unknown')}")

# --- TAB 2: Brochure Drafting & Compliance ---
with tab2:
    st.header("AI Brochure Drafting & Compliance Gatekeeper")
    product_name = st.text_input("Product Name:", "Zurich Wealth Guardian CI Plan")
    target_audience = st.text_input("Target Audience:", "Young professionals aged 25-35 in Hong Kong")

    if st.button("Draft & Check Compliance"):
        with st.spinner("Drafting brochure and running local compliance checks..."):
            llm = ChatOllama(model="llama3", temperature=0.7)

            # 1. Draft Brochure
            draft_prompt = f"Draft a 1-page customer brochure summary for '{product_name}' targeting {target_audience}. Include key benefits, a brief risk disclaimer, and a call to action."
            draft_response = llm.invoke(draft_prompt).content
            st.subheader("📄 Drafted Brochure")
            st.markdown(draft_response)

            # 2. Compliance Check
            compliance_prompt = f"""Act as a Hong Kong Insurance Authority compliance officer. Review the following product brochure draft against GN16 and Fair Treatment of Customers (FTC) guidelines. 
            Flag any risky language (e.g., absolute guarantees, missing risk disclaimers, misleading yield projections). 
            Provide a 'Risk Level' (Low/Medium/High) and specific recommendations for revision.

            Draft: {draft_response}"""

            reg_result = query_vectorstore(st.session_state.reg_vectorstore, compliance_prompt)

            st.subheader("⚠️ Compliance Risk Report")
            st.markdown(reg_result['result'])

# --- TAB 3: Product Analytics ---
with tab3:
    st.header("Post-Launch Product Performance Dashboard")
    st.markdown("Monitor ongoing product maintenance KPIs (Synthetic Data for Demonstration).")

    # Generate synthetic data
    months = pd.date_range(start="2023-01-01", periods=12, freq='ME').strftime('%b %Y')
    uptake_rate = np.linspace(5, 12, 12) + np.random.normal(0, 1, 12)
    lapse_rate = np.linspace(8, 5, 12) + np.random.normal(0, 0.5, 12)

    df = pd.DataFrame({
        "Month": months,
        "Uptake Rate (%)": uptake_rate,
        "Lapse Rate (%)": lapse_rate
    })

    col1, col2 = st.columns(2)
    with col1:
        fig_uptake = px.line(df, x="Month", y="Uptake Rate (%)", title="Monthly Policy Uptake Rate", markers=True)
        st.plotly_chart(fig_uptake, use_container_width=True)
    with col2:
        fig_lapse = px.line(df, x="Month", y="Lapse Rate (%)", title="Monthly Lapse Rate", markers=True,
                            color_discrete_sequence=["red"])
        st.plotly_chart(fig_lapse, use_container_width=True)

    st.info(
        "💡 **Insight:** Lapse rates are trending downward due to the new customer engagement initiative, while uptake is steadily increasing. Recommend maintaining current proposition strategy.")