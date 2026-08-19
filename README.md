# AI_Document_Assistant

# AI Document Assistant

An AI-powered document assistant that allows users to upload documents and ask questions about their contents. The application uses retrieval-augmented generation (RAG) to find relevant information from uploaded documents and provide concise, context-based answers.

## Features

* 📄 Upload and process documents
* 🔎 Search documents using semantic similarity
* 🤖 Ask questions about document contents using OpenAI
* 📚 Retrieval-augmented generation (RAG)
* 💬 Interactive chat interface built with Streamlit
* 🔗 Provide relevant document context to support responses
* 🛡️ Designed to reduce hallucinations by grounding responses in uploaded documents

## How It Works

The application follows a RAG-based workflow:

```text
Upload Document
      ↓
Extract Document Text
      ↓
Split Text into Chunks
      ↓
Create Embeddings
      ↓
Store/Search Embeddings
      ↓
User Asks Question
      ↓
Retrieve Relevant Document Sections
      ↓
Send Relevant Context to OpenAI
      ↓
Generate Answer
```

Instead of sending an entire document to the language model for every question, the application retrieves the most relevant sections and uses those sections as context when generating the response.

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* LangChain

### AI

* OpenAI API
* Hugging Face / Sentence Transformers embeddings

### Document Processing

* PDF/text document processing
* Text chunking
* Semantic search

## Project Structure

```text
AI_Document_Assistant/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .gitignore              # Files excluded from Git
└── README.md               # Project documentation
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hsoong-jpg/AI_Document_Assistant.git
cd AI_Document_Assistant
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the virtual environment:

**macOS/Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the OpenAI API Key

Create a Streamlit secrets file:

```text
.streamlit/secrets.toml
```

Add:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

**Do not commit this file or your API key to GitHub.**

Make sure `.streamlit/secrets.toml` is included in `.gitignore`.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Example Use Cases

The assistant can be adapted for situations where users need to quickly retrieve information from large collections of documents, including:

* Technical documentation
* Repair manuals
* Company policies
* Product documentation
* Knowledge bases
* Research documents
* Internal documentation

## Security Considerations

Because the application uses an external AI API, sensitive information should not be uploaded without appropriate authorization.

The application should also protect:

* OpenAI API credentials
* Uploaded documents
* User questions and responses
* Vector database contents
* Authentication credentials

API keys should be stored using environment variables or Streamlit Secrets rather than committed to source control.

## Limitations

The assistant's responses depend on the quality and contents of the uploaded documents. If relevant information is not present in the retrieved documents, the model may be unable to provide an accurate answer.

For production use, additional security controls such as authentication, authorization, access controls, secure document storage, monitoring, and input validation should be implemented.

## Future Improvements

* 🔐 User authentication and authorization
* 📁 Support for additional document formats
* 🗂️ Persistent vector database
* 📊 Document management dashboard
* 🔍 Improved retrieval and ranking
* 💾 Conversation history
* 📈 Usage and performance monitoring
* 🛡️ Prompt-injection and data-leakage protections
* 👥 Role-based access control

## Author

**Hannah Soong**

Computer Science & Business
Oberlin College

[GitHub Repository](https://github.com/hsoong-jpg/AI_Document_Assistant)
