# Quick Start Guide - Tax Memo API

## Prerequisites

1. **Python 3.10+** installed
2. **Qdrant** running (local or cloud)
3. **OpenAI API Key** (for embeddings and GPT-4o)

---

## Step 1: Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cd backend
```

Create `.env` file with:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
# OR for cloud Qdrant:
# QDRANT_URL=https://your-cluster-url.qdrant.io
# QDRANT_API_KEY=your_qdrant_api_key_here
```

**Note:** If using local Qdrant without authentication, you can omit `QDRANT_API_KEY`.

---

## Step 2: Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 3: Start Qdrant (If Using Local)

### Option A: Using Docker (Recommended)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Option B: Using Qdrant Cloud

1. Sign up at https://cloud.qdrant.io
2. Create a cluster
3. Get your cluster URL and API key
4. Add them to `.env` file

---

## Step 4: Ingest Documents into Qdrant

```bash
# Make sure you're in the backend directory
cd backend

# Run the ingestion script
python ingest_data.py
```

**Expected Output:**
```
Scanning ../source docs for PDF, HTML, DOCX, and TXT files...
Loading PDFs...
  - Found 0 PDF pages.
Loading HTML files...
  - Found 1 HTML documents.
Loading Word (.docx) files...
  - Found 42 Word documents.
Loading Text (.txt) files...
  - Found 6 text documents.
TOTAL documents to process: 49
Splitting documents into chunks...
Created 761 vector-ready chunks.
🧹 Found existing collection... Deleting it for a clean start...
Creating new collection: netherlands_pilot
Uploading 761 chunks to Qdrant...
SUCCESS! All PDFs, HTML, Word, and Text documents have been ingested.
```

**Note:** This script automatically prevents duplicates by deleting the old collection before re-ingesting.

---

## Step 5: Start the FastAPI Server

```bash
# Make sure you're in the backend directory
cd backend

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 6: Test the API

### Option A: Using Swagger UI (Recommended)

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see the interactive API documentation where you can:
1. Click on `POST /generate-memo`
2. Click "Try it out"
3. Paste your JSON request
4. Click "Execute"

### Option B: Using cURL

```bash
curl -X POST "http://localhost:8000/generate-memo" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "SaaS Innovators Inc.",
    "industry": "Software & Technology",
    "employeeCount": 5,
    "entryGoals": ["Establish physical presence", "Tax optimization"],
    "primaryJurisdiction": "Netherlands",
    "taxConsiderations": ["Corporate income tax implications"],
    "additionalContext": "We develop our own IP and want to know about R&D incentives."
  }'
```

### Option C: Using Python

```python
import requests

url = "http://localhost:8000/generate-memo"
payload = {
    "companyName": "SaaS Innovators Inc.",
    "industry": "Software & Technology",
    "employeeCount": 5,
    "entryGoals": ["Establish physical presence", "Tax optimization"],
    "primaryJurisdiction": "Netherlands",
    "taxConsiderations": ["Corporate income tax implications"],
    "additionalContext": "We develop our own IP and want to know about R&D incentives."
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## Step 7: Verify Health Check

```bash
# Check if server is running
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

---

## Common Issues & Solutions

### Issue 1: "OPENAI_API_KEY not found"
**Solution:** Make sure `.env` file exists in `backend/` directory with `OPENAI_API_KEY` set.

### Issue 2: "Connection refused" to Qdrant
**Solution:** 
- Check if Qdrant is running: `docker ps` (if using Docker)
- Verify `QDRANT_URL` in `.env` is correct
- For cloud Qdrant, ensure `QDRANT_API_KEY` is set

### Issue 3: "Collection not found"
**Solution:** Run `python ingest_data.py` to create the collection.

### Issue 4: "422 Validation Error"
**Solution:** Check that your request uses correct field names:
- Use `companyName` (camelCase) or `company_name` (snake_case)
- See `backend/API_DOCUMENTATION.md` for all valid fields

### Issue 5: Empty/null responses
**Solution:** 
- Check server logs for errors
- Verify documents were ingested successfully
- Ensure OpenAI API key is valid and has quota

---

## File Structure

```
backend/
├── .env                    # Environment variables (create this)
├── ingest_data.py          # Data ingestion script
├── app/
│   ├── main.py            # FastAPI application
│   ├── core/
│   │   ├── config.py      # Configuration
│   │   └── orchestrator.py # Task planning
│   ├── models/
│   │   ├── request.py     # Request models
│   │   └── response.py    # Response models
│   ├── services/
│   │   ├── qdrant.py      # Qdrant service
│   │   └── rag_engine.py  # RAG engine
│   └── utils/
│       └── persona.py     # System prompts
└── requirements.txt        # Python dependencies

source docs/
└── netherlands/           # All documents should be here
    ├── *.docx
    ├── *.txt
    └── *.html
```

---

## Quick Reference Commands

```bash
# 1. Navigate to backend
cd backend

# 2. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Ingest documents
python ingest_data.py

# 4. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Test API
# Open browser: http://localhost:8000/docs
```

---

## Next Steps

- Read `API_DOCUMENTATION.md` for detailed API documentation
- Check `FIELD_MAPPING_V2.md` for field mappings
- Review server logs for debugging information

---

## Support

If you encounter issues:
1. Check server logs in the terminal
2. Verify all environment variables are set correctly
3. Ensure Qdrant is running and accessible
4. Check OpenAI API key is valid

