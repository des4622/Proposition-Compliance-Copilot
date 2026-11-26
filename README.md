# 🛡️ Life Insurance Proposition Intelligence & Compliance Co-Pilot

> A privacy-first, locally-hosted AI application designed to accelerate the product proposition lifecycle for Life Insurance. It automates market research, drafts customer-facing materials, and embeds first-line regulatory compliance checks directly into the workflow.

## 🎯 Business Objective
In the highly regulated insurance industry, Product/Proposition Managers spend countless hours on manual competitor research, drafting marketing materials, and ensuring those materials comply with strict regulatory frameworks (like HKIA guidelines). 

This tool acts as an intelligent co-pilot, leveraging local Large Language Models (LLMs) to enhance productivity and decision-making while ensuring **zero data leakage** to third-party cloud APIs.

## 💡 Key Features

### 🔍 1. Market Intelligence (RAG)
* Instantly query and summarize uploaded competitor product PDFs.
* Identify trends, exclusions, pricing structures, and target demographics without reading hundreds of pages manually.

### 📝 2. AI Brochure Drafting & Compliance Gatekeeper
* Auto-generates 1-page customer product summaries based on target audiences.
* **First-Line Compliance Check:** Automatically cross-references the drafted text against regulatory guidelines (e.g., GN16, Fair Treatment of Customers) to flag risky language (e.g., absolute guarantees, missing risk disclaimers) *before* it reaches the legal team.

### 📊 3. Post-Launch Product Analytics
* Interactive dashboard tracking ongoing product maintenance KPIs (Policy Uptake Rates, Lapse Rates).
* Demonstrates the ability to monitor product performance post-launch to support data-driven proposition adjustments.

## 🛡️ Why This Matters for Insurance

**100% On-Premise Deployment**: Built using local, open-source models (Llama 3 via Ollama) to ensure:
- ✅ No sensitive competitor data leaves the network
- ✅ No draft product materials sent to third-party cloud APIs
- ✅ Full compliance with insurance data privacy and information security constraints

This is not just an AI demo—it's a **risk-aware solution** designed for regulated financial institutions.


## 🔒 Data Privacy & Security
Built specifically with the financial services sector in mind, this application runs **100% locally**. No competitor data, draft materials, or regulatory queries are ever sent to external cloud APIs (like OpenAI), ensuring strict adherence to enterprise information security policies.


## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI/LLM | LangChain, Ollama (Llama 3) |
| Embeddings | HuggingFace (sentence-transformers/all-MiniLM-L6-v2) |
| Vector Database | ChromaDB (local, zero-cost persistence) |
| Data Visualization | Pandas, Plotly |
| Language | Python 3.12 |

## 📁 Project Structure

zurich_proposition_copilot/
├── data/

│ ├── competitors/ # PDF brochures from HK insurers

│ └── regulations/ # HKIA guidelines (GN16, FTC)

├── app.py # Main Streamlit application

├── rag_engine.py # Core RAG logic (ingestion & retrieval)

├── requirements.txt # Python dependencies

└── README.md # This file

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI/LLM Orchestration:** LangChain (LCEL), LangChain-Ollama
* **Local LLM:** Llama 3 (via Ollama)
* **Vector Database:** ChromaDB (Local, persistent storage)
* **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
* **Data Visualization:** Pandas, Plotly


## 🚀 How to Run Locally

### Prerequisites
- Python 3.12 (recommended)
- Anaconda (for environment management)
- Ollama installed locally ([download here](https://ollama.com/download))

### Setup Steps

1. **Clone or download this repository**

2. **Create Conda environment**:
   ```bash
   conda create -n personal_projects python=3.12 -y
   conda activate personal_projects
   ollama pull llama3

3. **Install Ollama and download models**:
   ollama pull nomic-embed-text

4. **Install Python dependencies**:
   pip install streamlit langchain langchain-core langchain-community langchain-ollama langchain-huggingface chromadb pypdf pandas plotly sentence-transformers

5. **Add your data**:
   Place 2-3 competitor product PDFs in data/competitors/
   Place HKIA guideline text files (e.g., gn16.txt, ftc.txt) in data/regulations/

6. **Run the application**:
   streamlit run app.py

7. **Open your browser to** http://localhost:8501

   
