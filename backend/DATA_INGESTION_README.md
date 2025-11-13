# Reverse RAG Data Validation Scripts

This directory contains scripts for ingesting Dutch source documents into Qdrant and running gap analysis tests.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your_qdrant_api_key_here  # Optional if Qdrant is local
   ```

3. **Prepare source documents:**
   - Create a folder named `source_documents/` in the `backend/` directory
   - Place all your PDF, HTML, DOCX, and TXT files in this folder
   - The scripts will automatically detect and process all supported file types

## Script 1: ingest_data.py

**Purpose:** Ingests PDF, HTML, DOCX, and TXT files from `./source_documents/` into Qdrant collection `netherlands_pilot`.

**Features:**
- Supports multiple file formats: PDF, HTML, DOCX, TXT
- Automatic chunking (1000 chars, 200 overlap)
- Adds metadata: `source_filename` to each chunk
- Uses `text-embedding-3-small` for efficient cross-lingual embeddings
- Creates collection if it doesn't exist

**Usage:**
```bash
cd backend
python ingest_data.py
```

**What it does:**
1. Validates that `OPENAI_API_KEY` is set in environment variables
2. Scans `./source_documents/` for PDF, HTML, DOCX, and TXT files
2. Loads all documents using appropriate loaders
3. Splits documents into chunks (1000 chars, 200 overlap)
4. Generates embeddings using OpenAI `text-embedding-3-small`
5. Upserts all chunks into Qdrant collection `netherlands_pilot`

**Expected Output:**
```
📂 Scanning ./source_documents for PDF, HTML, and DOCX files...
Loading PDFs...
  - Found 150 PDF pages.
Loading HTML files...
  - Found 5 HTML documents.
Loading Word (.docx) files...
  - Found 10 Word documents.
Loading Text (.txt) files...
  - Found 5 text documents.
✅ TOTAL documents to process: 170
✂️ Splitting documents into chunks...
🧩 Created 450 vector-ready chunks.
🧠 Initializing embeddings and Qdrant connection...
Creating new collection: netherlands_pilot
🚀 Uploading 450 chunks to Qdrant (this may take a while)...
🎉 SUCCESS! All PDFs, HTML, and Word documents have been ingested.
```

## Script 2: test_coverage.py

**Purpose:** Runs gap analysis tests using English queries against Dutch documents to validate coverage.

**Test Queries:**
1. "What are the WBSO R&D tax credit rates for 2025?"
2. "What are the GDPR (AVG) requirements for small businesses?"
3. "Explain the participation exemption (deelnemingsvrijstelling) for holding companies."
4. "What is the difference between a BV and NV legal structure?"
5. "What are the current 2025 Corporate Income Tax (VPB) rates?"

**Usage:**
```bash
cd backend
python test_coverage.py
```

**What it does:**
1. Connects to Qdrant collection `netherlands_pilot`
2. For each test query:
   - Converts English query to embedding
   - Searches for top 2 matching Dutch document chunks
   - Displays source filename and preview of matched content

**Expected Output:**
```
🔍 Starting Gap Analysis Test Coverage...
================================================================================
✅ Connected to Qdrant collection: netherlands_pilot

================================================================================
TEST 1/5
================================================================================
Query: What are the WBSO R&D tax credit rates for 2025?
--------------------------------------------------------------------------------

📄 Match #1 (Score: 0.8234)
   Source: wbso_2025_guide.pdf
   Preview: De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) biedt fiscale voordelen voor onderzoek en ontwikkeling. In 2025 zijn de tarieven...

📄 Match #2 (Score: 0.7891)
   Source: tax_incentives_netherlands.pdf
   Preview: ...
```

## How It Works (Reverse RAG)

The system uses **cross-lingual embeddings** to match English queries to Dutch documents:

1. **English Query** → OpenAI Embedding (text-embedding-3-small)
2. **Dutch Documents** → Already embedded and stored in Qdrant
3. **Vector Similarity Search** → Finds most relevant Dutch chunks
4. **Gap Analysis** → Identifies which topics are well-covered vs. missing

The `text-embedding-3-small` model is excellent at cross-lingual retrieval, meaning English queries can effectively match Dutch content without translation.

## Troubleshooting

### "No documents found!"
- Ensure `source_documents/` folder exists in the `backend/` directory
- Check that files have correct extensions: `.pdf`, `.html`, `.docx`, `.txt`

### "OPENAI_API_KEY not found" error
- Ensure `.env` file exists in the `backend/` directory
- Add `OPENAI_API_KEY=your_key_here` to the `.env` file
- Or set it as an environment variable before running the script

### "Collection does not exist" error in test_coverage.py
- Run `ingest_data.py` first to create and populate the collection

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- For Word files, ensure `docx2txt` is installed: `pip install docx2txt`

### Qdrant connection errors
- Verify Qdrant is running: `http://localhost:6333`
- Check `QDRANT_URL` in `.env` file
- If using Qdrant Cloud, ensure `QDRANT_API_KEY` is set

## Notes

- The collection uses **1536-dimensional vectors** (text-embedding-3-small default)
- Chunks are **1000 characters** with **200 character overlap**
- Each chunk includes metadata: `source_filename` for traceability
- The system retrieves **top 2 matches** per query for gap analysis

