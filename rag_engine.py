import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def load_and_vectorize_data(folder_path, collection_name):
    """Loads PDFs or TXT files from a folder and creates a local Chroma vector store."""
    documents = []

    if os.path.exists(folder_path):
        pdf_loader = PyPDFDirectoryLoader(folder_path)
        documents.extend(pdf_loader.load())

        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                txt_loader = TextLoader(os.path.join(folder_path, file), encoding='utf-8')
                documents.extend(txt_loader.load())

    if not documents:
        raise ValueError(f"No documents found in {folder_path}. Please add PDFs or TXT files.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=f"./chroma_db/{collection_name}",
        collection_name=collection_name
    )
    return vectorstore


def format_docs(docs):
    """Helper to format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


def query_vectorstore(vectorstore, query):
    """Retrieves relevant context and generates an answer using LCEL (no chains module needed)."""
    llm = ChatOllama(model="llama3", temperature=0.3)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Use the given context to answer the question. If you don't know the answer, say you don't know. Keep the answer concise.\n\nContext: {context}"),
        ("human", "{input}")
    ])

    # LCEL pipeline — no langchain.chains module required
    rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    # Get source documents separately
    source_docs = retriever.invoke(query)
    answer = rag_chain.invoke(query)

    return {
        'result': answer,
        'source_documents': source_docs
    }