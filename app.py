import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS

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

def  get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    return vectorstore


def main():
    load_dotenv()
    st.set_page_config("AI Document Assistant", page_icon=":books:")

    st.header("AI Document Assistant" ":books:")
    st.text_input("What can I help you with?")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
            # get pdf text
                raw_text = get_pdf_text(pdf_docs) 
                
                

            # get the text chunks 
            text_chunks = get_text_chunks(raw_text)
            

            # create vector store
            vectorstore = get_vectorstore(text_chunks)


if __name__ == '__main__':
    main()