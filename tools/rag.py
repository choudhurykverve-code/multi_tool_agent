import os
from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DOCUMENTS_DIR="documents"
VECTORSTORE_DIR="vectorstore/faiss_index"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

_vectorstore = None

def build_or_load_vectorstore():
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    if os.path.exists(VECTORSTORE_DIR):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return _vectorstore

    if not os.path.exists(DOCUMENTS_DIR) or not os.listdir(DOCUMENTS_DIR):
        return None

    all_docs=[]
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(DOCUMENTS_DIR,  filename)
            loader = PyPDFLoader(filepath)
            all_docs.extend(loader.load())

    if not all_docs:
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(all_docs)

    _vectorstore = FAISS.from_documents(chunks, embeddings)
    _vectorstore.save_local(VECTORSTORE_DIR)

    return _vectorstore

@tool
def rag_tool(query: str) -> str:
    """
    Answer questions using uploaded PDF documents.

    Use this tool when the user asks about content from
    uploaded documents, files, or PDFs.
    """

    if not query or not query.strip():
        return "Error: Query cannot be empty."

    try:
        vectorstore = build_or_load_vectorstore()

        if vectorstore is None:
            return "Error: No PDF documents found. Please add PDFs to the documents folder."

        results = vectorstore.similarity_search(query.strip(), k=3)

        if not results:
            return "No relevant information found in the documents."

        context = "\n\n".join([doc.page_content for doc in results])
        return f"Relevant information from documents:\n\n{context}"

    except FileNotFoundError:
        return "Error: Documents not found."

    except Exception as e:
        return f"Error while searching documents: {e}"


    