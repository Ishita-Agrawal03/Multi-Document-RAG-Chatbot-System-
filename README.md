# 📄 Multi-Document RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that enables users to upload and query multiple PDF documents using semantic search. The application retrieves the most relevant document chunks using a FAISS vector database and generates context-aware responses using Groq LLMs.

---

## 🚀 Features

- 📂 Query multiple PDF documents
- 🔍 Semantic search using FAISS Vector Database
- 🤖 Context-aware question answering with Groq LLM
- 🧠 Hugging Face Sentence Transformers for embeddings
- 📄 Automatic PDF text extraction and chunking
- 💬 Interactive Streamlit chat interface
- 📚 Source citations for generated responses

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq (Llama 3.3)
- Hugging Face Sentence Transformers
- FAISS
- PyPDF
- Python Dotenv

---

## 📂 Project Structure

```
rag-chatbot/
│
├── docs/                  # PDF documents
├── vectorstore/           # FAISS index
├── app.py                 # Main application
├── .env                   # API Key
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/rag-chatbot.git
cd rag-chatbot
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## 🧩 How It Works

1. Upload one or more PDF documents.
2. Extract text from PDFs.
3. Split documents into chunks.
4. Generate embeddings using Hugging Face Sentence Transformers.
5. Store embeddings in a FAISS Vector Database.
6. Retrieve the most relevant chunks based on the user's query.
7. Send retrieved context to the Groq LLM.
8. Generate an accurate response with source citations.

---

## 🖥️ Workflow

```
PDFs
   │
   ▼
PyPDFLoader
   │
   ▼
Text Chunking
   │
   ▼
Sentence Transformer Embeddings
   │
   ▼
FAISS Vector Database
   │
   ▼
Retriever
   │
   ▼
Groq LLM
   │
   ▼
Answer + Source Citations
```

---

## 📌 Example Questions

- What is supervised learning?
- Explain overfitting.
- What are the types of machine learning?
- Summarize Chapter 2.
- Compare supervised and unsupervised learning.

---

## 📈 Future Improvements

- Chat memory for follow-up conversations
- Persistent vector database
- Hybrid Search (BM25 + Dense Retrieval)
- Re-ranking using Cross Encoder
- Support for DOCX and TXT files
- Conversation export
- Docker deployment

---

## 👩‍💻 Author

**Ishita Agrawal**

- GitHub: https://github.com/Ishita-Agrawal03


---

## ⭐ If you found this project useful, consider giving it a star!
