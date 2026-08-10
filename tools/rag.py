import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

DOCUMENTS_DIR = "documents"
VECTORSTORE_DIR = "vectorstore/faiss_index"

_vectorstore = None


def get_embeddings():
    """Create Gemini embeddings only when RAG is actually used."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return None

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )


def build_or_load_vectorstore():
    global _vectorstore

    if _vectorstore is not None:
        return _vectorstore

    embeddings = get_embeddings()

    if embeddings is None:
        return None

    if os.path.exists(VECTORSTORE_DIR):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return _vectorstore

    if not os.path.exists(DOCUMENTS_DIR) or not os.listdir(DOCUMENTS_DIR):
        return None

    all_docs = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)

            loader = PyPDFLoader(filepath)
            all_docs.extend(loader.load())

    if not all_docs:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(all_docs)

    _vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

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

    if not os.getenv("GOOGLE_API_KEY"):
        return "Error: Google API key is not configured."

    try:
        vectorstore = build_or_load_vectorstore()

        if vectorstore is None:
            return (
                "Error: No PDF documents found. "
                "Please add PDFs to the documents folder."
            )

        results = vectorstore.similarity_search(
            query.strip(),
            k=5
        )

        if not results:
            return "No relevant information found in the documents."

        context = "\n\n".join(
            [
                f"[Source: {os.path.basename(doc.metadata.get('source', 'unknown'))}]\n"
                f"{doc.page_content}"
                for doc in results
            ]
        )

        return f"Relevant information from documents:\n\n{context}"

    except FileNotFoundError:
        return "Error: Documents not found."

    except Exception as e:
        return f"Error while searching documents: {e}"