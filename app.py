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


# Loops through each pdf in pdf_docs and loops through all pages and extracts text from page and appends it to text var
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000, 
        chunk_overlap = 200,
        length_function =len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def  get_vectorstore(text_chunks):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
    model="gpt-5.6-luna",
    temperature=0
)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm =llm,
        retriever=vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation.invoke({"question": user_question}) 
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

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

    user_question =st.text_input("What can I help you with?")
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

                if not raw_text.strip():
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