🌾 AgriBot — RAG-Powered Agriculture Assistant 🤖

AgriBot is a web-based agriculture assistant built with Django and Retrieval-Augmented Generation (RAG).

The project allows users to ask questions about agriculture and receive answers based on information retrieved from an agricultural knowledge base. Instead of relying entirely on an LLM's general knowledge, AgriBot first searches its knowledge base for relevant information and then uses an LLM to generate a clear, natural-language response from the retrieved context.

🚀 What AgriBot Does

A user can ask questions such as:

"How do I grow wheat?"

"What type of soil is suitable for rice?"

"What are the major factors affecting crop growth?"

AgriBot processes the question, retrieves the most relevant sections from its agricultural knowledge base, and generates an answer using that retrieved information.

Each response also includes the source pages used to produce the answer.

🧠 How the RAG System Works

The project has two main stages:

1. Knowledge Ingestion

The agricultural PDF is processed before the chatbot is used.

The ingestion pipeline:

Agriculture PDF
      ↓
PDF Text Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
ChromaDB Vector Storage


The current knowledge base contains:

138 PDF pages

445 text chunks

Vector embeddings stored in ChromaDB

The ingestion process is implemented in:

rag/ingest.py

2. Question Answering

When a user asks a question:

User Question
      ↓
Question Embedding
      ↓
ChromaDB Similarity Search
      ↓
Relevant Chunks Retrieved
      ↓
Context + Question
      ↓
LLM
      ↓
Final Answer


The retrieval and answer-generation logic is implemented in:

rag/engine.py


The LLM is primarily used to turn the retrieved context into a readable and useful answer rather than requiring it to provide all agricultural knowledge from its own memory.

📚 Knowledge Base

The current knowledge source is:

knowledge/agriculture.pdf


The PDF is processed during ingestion and converted into smaller text chunks.

Each chunk is converted into a numerical vector called an embedding. These embeddings allow the system to compare the meaning of a user's question with the meaning of stored pieces of agricultural information.

For example, a question such as:

"What climate is good for wheat?"

does not need to exactly match the wording inside the PDF.

Instead, the system searches for chunks that are semantically similar to the question.

🔎 Retrieval

AgriBot uses ChromaDB as its vector database.

The collection currently used by the project is:

agriculture


The database stores the embedded document chunks along with their associated document information, such as the original PDF and page number.

When a question is submitted, the system retrieves the most relevant chunks from the vector database.

This allows AgriBot to focus the LLM on the relevant parts of the agricultural document rather than passing the entire PDF to the model.

🤖 Answer Generation

After retrieving the relevant chunks, AgriBot creates a prompt containing:

The user's question

Relevant information retrieved from the knowledge base

Instructions for generating the response

The LLM then uses this context to produce the final answer.

This separation gives the project two distinct components:

Retrieval

Find the relevant agricultural information.

Generation

Turn that information into a clear answer.

🖥️ Web Application

The application is built using Django.

The web interface currently contains:

🏠 Home page

💬 RAG-powered chatbot

📚 Project/About page

👨‍💻 Developer/Contact page

📄 Resume section

The chatbot provides source information along with its responses.

🛠️ Tech Stack
Backend

Python

Django

RAG / AI

Retrieval-Augmented Generation (RAG)

Sentence embeddings

ChromaDB

Large Language Model (LLM)

Frontend

HTML

CSS

JavaScript

Development Tools

Git

GitHub

VS Code

Python virtual environment

📁 Project Structure
Agribot/
│
├── botapp/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── chat.html
│   │   ├── about.html
│   │   └── contact.html
│   │
│   ├── static/
│   │   └── style.css
│   │
│   ├── urls.py
│   └── views.py
│
├── chatbot_core/
│
├── knowledge/
│   └── agriculture.pdf
│
├── rag/
│   ├── ingest.py
│   ├── engine.py
│   └── test_rag.py
│
├── static/
│   └── files/
│       └── Benny_Thomas_Resume.pdf
│
├── manage.py
├── requirements.txt
└── README.md

⚙️ Running the Project Locally
1. Clone the repository
git clone https://github.com/BenThomasPvt/Agribot.git
cd Agribot

2. Create a virtual environment

Windows:

python -m venv rag_env


Activate it:

.\rag_env\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure the LLM API

The project uses an LLM API for answer generation.

Create a .env file and add the required API key:

GROQ_API_KEY=your_api_key_here


Do not commit API keys or other secrets to GitHub.

5. Build the vector database

From the project root:

python rag\ingest.py


This extracts the agricultural PDF, creates chunks, generates embeddings, and stores them in ChromaDB.

6. Test the RAG pipeline
python rag\test_rag.py

7. Start Django
python manage.py runserver


Then open:

http://127.0.0.1:8000/

🔄 Evolution of the Project

AgriBot originally started as a traditional NLP chatbot using:

User Question
      ↓
TF-IDF
      ↓
Cosine Similarity
      ↓
Intent / Response


The project was later redesigned into a Retrieval-Augmented Generation system:

User Question
      ↓
Embedding
      ↓
Vector Similarity Search
      ↓
Relevant Agricultural Context
      ↓
LLM
      ↓
Generated Answer


This change allows the chatbot to work with a much larger knowledge source and provide answers grounded in the information contained in the agricultural reference material.

🌱 Future Improvements

Possible future improvements include:

 Add support for multiple agricultural documents

 Improve chunking and retrieval strategies

 Add conversation memory

 Add document upload functionality

 Add agricultural image diagnosis

 Add voice interaction

 Experiment with local LLMs

 Improve UI/UX

 Deploy the application online

 Add evaluation metrics for retrieval and answer quality

👨‍💻 Author

Gathala Benny Thomas

Final-year Computer Science & Engineering Student
Web & AI Developer

GitHub: https://github.com/BenThomasPvt

LinkedIn: https://linkedin.com/in/benthomaspvt

Email: benthomaspvt@gmail.com

📌 Project Status

AgriBot is currently an active RAG-based agriculture assistant project.

The core pipeline for document ingestion, embedding generation, vector storage, semantic retrieval, and LLM-based answer generation is implemented.

🌾 AgriBot — Turning agricultural knowledge into accessible answers.