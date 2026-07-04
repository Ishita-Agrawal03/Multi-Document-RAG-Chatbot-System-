import streamlit as st
import hashlib
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os
load_dotenv()
from database.db import (
    init_db,
    create_chat,
    get_all_chats
)

init_db()
print(os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="RAG Chatbot")
st.title("📄 RAG Chatbot")
with st.sidebar:

    st.header("Chats")

    if st.button("➕ New Chat"):

        create_chat()

        st.rerun()

    chats = get_all_chats()

    for chat in chats:

        st.button(
            chat[1],
            key=chat[0]
        )

def get_file_hash(uploaded_files):
    md5 = hashlib.md5()

    for file in uploaded_files:
        md5.update(file.getvalue())

    return md5.hexdigest()


uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type="pdf",
    accept_multiple_files=True
)
if uploaded_files:
    file_hash = get_file_hash(uploaded_files)

    vectorstore_path = os.path.join(
    "vectorstores",
    "chroma",
    file_hash
    )

    if st.button("Process Documents"):

        docs = []

        for uploaded_file in uploaded_files:

            # Save uploaded file temporarily
            temp_path = os.path.join(
                "temp",
                f"{file_hash}_{uploaded_file.name}"
            )

            os.makedirs("temp", exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            loader = PyPDFLoader(temp_path)
            loaded_docs = loader.load()

            for doc in loaded_docs:
                doc.metadata["source_file"] = uploaded_file.name

            docs.extend(loaded_docs)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(docs)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
    
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        


        os.makedirs(vectorstore_path, exist_ok=True)

        vectorstore = Chroma(
        persist_directory=vectorstore_path,
        embedding_function=embeddings,
        )

# Check whether this Chroma collection already has documents
        existing_docs = vectorstore.get()

        if len(existing_docs["ids"]) == 0:

            vectorstore.add_documents(chunks)

            st.success("Created new vector database.")

        else:

            st.success("Loaded existing vector database.")


        st.session_state.vectorstore = vectorstore
        st.session_state.messages = []



llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
if "vectorstore" in st.session_state:

    retriever = st.session_state.vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )



if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("Ask your PDF")
if question:

    if "vectorstore" not in st.session_state:
        st.warning("Please upload and process PDFs first.")
        st.stop()

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