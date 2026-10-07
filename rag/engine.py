import os

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------
# Configuration
# ---------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "agriculture"


# ---------------------------------------
# Groq
# ---------------------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ---------------------------------------
# ChromaDB
# ---------------------------------------

embedding_function = (
    embedding_functions.DefaultEmbeddingFunction()
)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


# ---------------------------------------
# Retrieval
# ---------------------------------------

def retrieve(query, top_k=5):
    """
    Find the most relevant chunks
    from the agriculture knowledge base.
    """

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas


# ---------------------------------------
# RAG
# ---------------------------------------

def ask(query):
    """
    Complete RAG pipeline:

    Question
       ↓
    Retrieval
       ↓
    Context
       ↓
    Groq LLM
       ↓
    Answer
    """

    documents, metadatas = retrieve(query)

    # Build context
    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"""
Source: {metadata['source']}
Page: {metadata['page']}

{document}
"""
        )

    context = "\n\n".join(context_parts)

    # ---------------------------------------
    # Prompt
    # ---------------------------------------

    system_prompt = """
You are AgriBot, an agriculture assistant
designed to help beginners learn agriculture.

Answer the user's question using the provided
knowledge base context.

Important rules:

1. Use the provided context as your primary
   source of information.

2. Do not invent facts that are not supported
   by the context.

3. If the answer cannot be found in the
   provided context, say:

   "I couldn't find that information in
   my agriculture knowledge base."

4. Explain concepts clearly for someone who
   is new to agriculture.

5. When possible, mention the source page.
"""

    user_prompt = f"""
Knowledge Base Context:

{context}

--------------------------------

User Question:

{query}
"""

    # ---------------------------------------
    # Groq
    # ---------------------------------------

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    # ---------------------------------------
    # Sources
    # ---------------------------------------

    sources = []

    for metadata in metadatas:

        source = (
            f"{metadata['source']} "
            f"(Page {metadata['page']})"
        )

        if source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }
