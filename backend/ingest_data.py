"""Data ingestion script for PDF, HTML, DOCX, and TXT files into Qdrant."""
import os
import sys
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, BSHTMLLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

# Load environment variables (look for .env in backend directory)
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback: try current directory
    load_dotenv()

# --- CONFIGURATION ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
COLLECTION_NAME = "netherlands_pilot"
SOURCE_DIR = "../source docs"

# Validate required environment variables
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found in environment variables!")
    print("Please set OPENAI_API_KEY in your .env file or environment.")
    sys.exit(1)

print(f"Scanning {SOURCE_DIR} for PDF, HTML, DOCX, and TXT files...")

# 1. Define Loaders for each file type
pdf_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
html_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.html", loader_cls=BSHTMLLoader)
docx_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.docx", loader_cls=Docx2txtLoader)
txt_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})

# 2. Load Data
print("Loading PDFs...")
pdf_docs = pdf_loader.load()
print(f"  - Found {len(pdf_docs)} PDF pages.")

print("Loading HTML files...")
html_docs = html_loader.load()
print(f"  - Found {len(html_docs)} HTML documents.")

print("Loading Word (.docx) files...")
word_docs = docx_loader.load()
print(f"  - Found {len(word_docs)} Word documents.")

print("Loading Text (.txt) files...")
txt_docs = txt_loader.load()
print(f"  - Found {len(txt_docs)} text documents.")

# 3. Combine ALL documents
all_docs = pdf_docs + html_docs + word_docs + txt_docs
print(f"TOTAL documents to process: {len(all_docs)}")

if len(all_docs) == 0:
    print("ERROR: No documents found! Check your source_documents folder.")
    exit(1)

# 4. Split into Chunks
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents(all_docs)
print(f"Created {len(chunks)} vector-ready chunks.")

# 5. Add metadata with source filename
print("Adding metadata to chunks...")
for chunk in chunks:
    source = chunk.metadata.get("source", "unknown")
    filename = os.path.basename(source)
    chunk.metadata["source_filename"] = filename

# 6. Embed & Upsert to Qdrant
print("Initializing embeddings and Qdrant connection...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Initialize Qdrant client
if QDRANT_API_KEY:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    client = QdrantClient(url=QDRANT_URL)

# ⚠️ This line prevents duplicates!
if client.collection_exists(COLLECTION_NAME):
    print(f"🧹 Found existing collection... Deleting it for a clean start...")
    client.delete_collection(collection_name=COLLECTION_NAME)

# Create collection
print(f"Creating new collection: {COLLECTION_NAME}")
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

print(f"Uploading {len(chunks)} chunks to Qdrant (this may take a while)...")
qdrant = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

qdrant.add_documents(chunks)

print("SUCCESS! All PDFs, HTML, Word, and Text documents have been ingested.")

