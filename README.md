# 🧑‍🔧 AI Document Assistant

An AI-powered document assistant built with **Streamlit, Python, LangChain, FAISS, Hugging Face embeddings, and OpenAI**. The application allows authorized repair technicians to upload PDF documentation and ask questions about repair procedures, safety information, and technical specifications.

The assistant uses **retrieval-augmented generation (RAG)** to retrieve relevant sections of uploaded documents and provide answers grounded in the available documentation.

## ✨ Features

* 📄 Upload multiple PDF documents
* 🔎 Extract and split document text into searchable chunks
* 🧠 Generate semantic embeddings using Hugging Face
* 🗂️ Store document embeddings using FAISS
* 💬 Ask questions through an interactive Streamlit chat interface
* 🤖 Generate technician-focused responses using OpenAI
* 📚 Display the source document and page number used for each answer
* 🛡️ Prompt the AI to only use information contained in the uploaded documentation
* 🔧 Provide concise, step-by-step repair guidance when available

## 🏗️ How It Works

The application follows a retrieval-augmented generation workflow:

```text
PDF Documents
      ↓
Extract Text with PyPDF2
      ↓
Split Text into Chunks
      ↓
Generate Hugging Face Embeddings
      ↓
Store Embeddings in FAISS
      ↓
User Asks a Question
      ↓
Retrieve Relevant Document Chunks
      ↓
Send Retrieved Context to OpenAI
      ↓
Generate Technician-Focused Answer
      ↓
Display Answer + Sources
```

This approach allows the assistant to search the uploaded documentation and provide responses based on the most relevant sections rather than relying solely on the model's general knowledge.

## 🛠️ Tech Stack

### Frontend

* **Streamlit** — web application and chat interface
* **HTML/CSS** — custom chat message styling

### Document Processing

* **PyPDF2** — PDF text extraction
* **LangChain Text Splitters** — document chunking

### Retrieval

* **Hugging Face Sentence Transformers**

  * `sentence-transformers/all-MiniLM-L6-v2`
* **FAISS** — vector similarity search

### AI

* **LangChain**
* **OpenAI**
* **Conversational Retrieval Chain**
* **Conversation Buffer Memory**

## 📁 Project Structure

```text
AI_Document_Assistant/
│
├── app.py
├── httmlTemplates.py
├── requirements.txt
├── README.md
└── .gitignore
```

### `app.py`

Contains the main Streamlit application, including:

* PDF processing
* Text extraction
* Text chunking
* Embedding generation
* FAISS vector store creation
* Conversational retrieval
* OpenAI integration
* Chat interface
* Source display

### `httmlTemplates.py`

Contains the custom HTML/CSS templates used to display:

* User messages
* AI responses
* Chat styling

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hsoong-jpg/AI_Document_Assistant.git
cd AI_Document_Assistant
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the OpenAI API Key

For local development, configure your OpenAI API key using an environment variable or your local Streamlit secrets file.

For Streamlit deployment, use **Streamlit Secrets** rather than committing an API key to GitHub.

Example:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

**Never commit API keys, passwords, or other credentials to the repository.**

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💬 Using the Assistant

1. Open the application.
2. Upload one or more PDF repair documents from the sidebar.
3. Click **Process**.
4. Wait for the documents to be processed and indexed.
5. Enter a question in the chat box.
6. The assistant retrieves relevant sections from the uploaded documents.
7. The response is generated using the retrieved context.
8. The source document and page number are displayed below the response.

## 🔐 AI Response Guidelines

The assistant is designed specifically for authorized repair technicians.

Its prompt instructs the model to:

* Only use the provided documentation.
* Provide technician-facing answers.
* Give step-by-step repair instructions when available.
* Avoid inventing repair procedures, tools, parts, measurements, or specifications.
* Avoid consumer-oriented recommendations unless they appear in the documentation.
* Include documented safety warnings when relevant.
* State when the available documentation does not contain enough information to answer a question.
* Identify relevant source documents when possible.

These constraints are intended to reduce unsupported or hallucinated repair instructions.

## 🔒 Security Considerations

This application uses an external AI API and should not be used with confidential or sensitive documents unless the appropriate authorization and security controls are in place.

Important security considerations include:

* Keep OpenAI API keys outside the source code.
* Never commit API keys to GitHub.
* Do not commit `.env` files or Streamlit secrets.
* Do not upload confidential company documentation without authorization.
* Restrict access to the deployed application when documents contain sensitive information.
* Use authentication and authorization for production deployments.
* Protect uploaded documents and vector stores from unauthorized access.

For a public demonstration, use sample or non-confidential documents.

## ⚠️ Limitations

The assistant's responses depend on the information contained in the uploaded documents.

If the relevant repair procedure or technical information is not present in the retrieved document context, the assistant is instructed to indicate that the available documentation is insufficient.

Additional limitations include:

* PDF text extraction may not work correctly with scanned/image-only PDFs.
* Retrieval quality depends on document chunking and embedding quality.
* The current vector store is created when documents are processed and is not intended as a persistent production database.
* Conversation memory exists within the current Streamlit session.
* Production use would require additional security, authentication, monitoring, and data-management controls.


## 👩‍💻 Author

**Hannah Soong**

Computer Science & Business
Oberlin College

[GitHub Repository](https://github.com/hsoong-jpg/AI_Document_Assistant)
