import os
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document
import PyPDF2

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return extract_text_from_txt(path)
    elif ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""

def build_vectorstore(file_paths):
    texts = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for path in file_paths:
        text = extract_text(path)
        if text:
            docs = splitter.split_text(text)
            texts.extend(docs)

    embeddings = OpenAIEmbeddings()
    store = FAISS.from_texts(texts, embedding=embeddings)
    store.save_local("data/vectorstore")
    return store

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local("data/vectorstore", embeddings, allow_dangerous_deserialization=True)

