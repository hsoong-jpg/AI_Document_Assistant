import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from httmlTemplates import css, bot_template, user_template
from langchain_core.prompts import PromptTemplate

prompt_template = """
You are an internal AI assistant for authorized repair technicians.

Your job is to help technicians perform device repairs using the provided
company documentation.

Rules:
- Answer as a technician-facing repair assistant.
- Only use the provided documents.
- Give clear, practical, step-by-step repair instructions when the documents
  contain them.
- Do not give consumer-oriented advice such as "contact Apple" or "take it
  to a repair shop" unless the documentation specifically says to do so.
- Do not invent repair procedures, tools, parts, measurements, or specifications.
- If the documentation does not contain enough information to answer,
  say that the available documentation does not provide the required procedure.
- Include relevant safety warnings when they are documented.
- Keep answers concise and technical.
- Do not make insurance, fraud, or coverage decisions.
- When relevant, identify the document information used to answer.
- Use ONLY the provided context. If the answer isn't in the context, say you don't have enough information.

Context:
{context}

Question:
{question}

Technician-focused answer:
"""

QA_PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Loops through each pdf in pdf_docs and loops through all pages and extracts text from page and appends it to text var
def get_pdf_text(pdf_docs):
    documents = []

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)

        for page_number, page in enumerate(pdf_reader.pages, start =1):
            text = page.extract_text()

            if text:
                documents.append({
                    "text": text,
                    "source": pdf.name,
                    "page": page_number
                })
    return documents


def get_text_chunks(documents):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000, 
        chunk_overlap = 200,
        length_function =len
    )
    chunks = []

    for document in documents:
        page_chunks = text_splitter.split_text(document["text"])

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "source": document["source"],
                "page": document["page"]
            })
    return chunks

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def  get_vectorstore(text_chunks):
    embeddings = get_embeddings()
    texts = [chunk["text"] for chunk in text_chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"]
        }

        for chunk in text_chunks
    ]

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding = embeddings,
        metadatas=metadatas
    )
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
    model="gpt-5.6-luna",
    temperature=0
)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm =llm,
        retriever=vectorstore.as_retriever(),
        memory = memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={
        "prompt": QA_PROMPT
    }
    

    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation.invoke({"question": user_question}) 
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    st.subheader("Sources")

    for doc in response["source_documents"]:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        st.write(f"📄 {source} — Page {page}")

def main():
    load_dotenv()

    st.set_page_config(
        page_title="AI Document Assistant",
        page_icon="🧑‍🔧"
    )
    st.write(css,unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("AI Document Assistant 🧑‍🔧")

    user_question =st.chat_input("What can I help you with?")
    if user_question:
        if st.session_state.conversation is not None:
            handle_userinput(user_question)
        else:
            st.warning("Please upload and process at least one document first")



    with st.sidebar:
        st.subheader("Your documents")

        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click 'Process'",
            accept_multiple_files=True,
            type=["pdf"]
        )

        if st.button("Process"):

            if not pdf_docs:
                st.warning("Please upload a PDF first.")
                return

            with st.spinner("Processing..."):

                # Get PDF text
                raw_text = get_pdf_text(pdf_docs)

                if not raw_text:
                    st.error("No text could be extracted from the PDF.")
                    return


                # Get text chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store
                vectorstore = get_vectorstore(text_chunks)

                st.session_state.vectorstore = vectorstore

            st.success("Documents processed successfully!")

            # create conversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore)

 
            

if __name__ == '__main__':
    main()