import os

import chromadb
from chromadb.utils import embedding_functions
import pymupdf
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PDF_PATH = os.path.join(
    BASE_DIR,
    "knowledge",
    "agriculture.pdf"
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "agriculture"


# Chroma will handle the embedding model for us.
embedding_function = (
    embedding_functions.DefaultEmbeddingFunction()
)


chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


def extract_pages(pdf_path):
    """Extract text from every page of the PDF."""

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest():

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    print("================================")
    print("AGRIBOT RAG INGESTION")
    print("================================")

    print(f"PDF: {PDF_PATH}")

    # ---------------------------------
    # 1. Extract PDF
    # ---------------------------------

    pages = extract_pages(PDF_PATH)

    print(f"Pages extracted: {len(pages)}")

    # ---------------------------------
    # 2. Chunk document
    # ---------------------------------

    documents = []
    metadatas = []
    ids = []

    for page in pages:

        chunks = chunk_text(page["text"])

        for chunk_number, chunk in enumerate(chunks):

            documents.append(chunk)

            metadatas.append({
                "source": "agriculture.pdf",
                "page": page["page"],
                "chunk": chunk_number
            })

            ids.append(
                f"page_{page['page']}_chunk_{chunk_number}"
            )

    print(f"Chunks created: {len(documents)}")

    # ---------------------------------
    # 3. Create Chroma collection
    # ---------------------------------

    try:
        chroma_client.delete_collection(
            COLLECTION_NAME
        )
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    # ---------------------------------
    # 4. Add documents
    # ---------------------------------

    print("Creating embeddings and storing vectors...")

    batch_size = 100

    for start in range(
        0,
        len(documents),
        batch_size
    ):

        end = start + batch_size

        collection.add(
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            ids=ids[start:end]
        )

        print(
            f"Indexed "
            f"{min(end, len(documents))}"
            f"/{len(documents)} chunks"
        )

    print()
    print("================================")
    print("INGESTION COMPLETE")
    print("================================")
    print(f"Pages:       {len(pages)}")
    print(f"Chunks:      {len(documents)}")
    print(f"Database:    {CHROMA_PATH}")
    print(f"Collection:  {COLLECTION_NAME}")


if __name__ == "__main__":
    ingest()
