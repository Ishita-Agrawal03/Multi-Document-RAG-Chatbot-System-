import streamlit as st
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="RAG Chatbot")
st.title("📄 RAG Chatbot")


pdf_files = glob.glob("docs/*.pdf")

docs = []

for pdf in pdf_files:

    loader = PyPDFLoader(pdf)

    loaded_docs = loader.load()

    for doc in loaded_docs:
        doc.metadata["source_file"] = pdf

    docs.extend(loaded_docs)

print(f"Loaded {len(pdf_files)} PDFs")
print(f"Pages Loaded: {len(docs)}")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

print(f"Chunks Created: {len(chunks)}")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)
vectorstore.save_local("vectorstore")
print("Vector DB Created Successfully")



results = vectorstore.similarity_search(
    "What is this document about?",
    k=3
)

for doc in results:
    print(doc.page_content[:300])



llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

response = qa_chain.invoke(
    {"query": "What is this document about?"}
)

print(response["result"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("Ask your PDF")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    response = qa_chain.invoke(
        {"query": question}
    )

    answer = response["result"]
    sources = response["source_documents"]

    with st.chat_message("assistant"):
      st.write(answer)

    with st.expander("Sources"):

      for i, doc in enumerate(sources):

          st.write(f"Source {i+1}")

          st.write(
              f"PDF: {doc.metadata.get('source_file')}"
          )

          st.write(doc.page_content[:300])


    st.session_state.messages.append(
    {
        "role": "assistant",
        "content": answer,
        "sources": sources
    }
)