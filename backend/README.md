# Tax Memo Orchestrator Backend (V1 - Netherlands Pilot)

A production-ready FastAPI backend that generates comprehensive market entry memos using RAG (Retrieval-Augmented Generation) with Qdrant vector database and OpenAI GPT-4.

## Features

- **13-Section Memo Generation**: Comprehensive market entry analysis covering all aspects from executive summary to appendix
- **Intelligent Task Orchestration**: Automatically plans research tasks based on company profile and entry goals
- **RAG-Powered**: Uses Qdrant vector database for context retrieval and OpenAI GPT-4 for synthesis
- **Netherlands-Focused (V1)**: Hardcoded to support Netherlands market entry analysis
- **Street Rules Persona**: Direct, actionable advice from an entrepreneurial mentor perspective

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entrypoint
│   ├── core/
│   │   ├── config.py            # Environment configuration
│   │   └── orchestrator.py      # Task planning logic
│   ├── models/
│   │   ├── request.py           # Input JSON models
│   │   └── response.py          # 13-section output models
│   ├── services/
│   │   ├── qdrant.py            # Vector DB connection & search
│   │   └── rag_engine.py        # RAG generation engine
│   └── utils/
│       └── system_prompts.py    # LLM system prompts
├── requirements.txt
└── .env.example
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

### 3. Qdrant Setup

Ensure you have a Qdrant instance running with:
- Collection name: `tax_memo_knowledge_base`
- Documents indexed with metadata fields: `country` (value: "netherlands") and `year` (value: "2025")

### 4. Run the Server

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use Python directly:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST `/generate-memo`

Generate a comprehensive market entry memo.

**Request Body:**
```json
{
  "company_name": "TechStart Inc",
  "industry": "Software & Technology",
  "primary_jurisdiction": "Netherlands",
  "entry_goals": ["Hire employees", "Establish office"],
  "current_revenue": 1000000,
  "employee_count": 10,
  "timeline_preference": "3 months",
  "budget_range": "$50k - $100k"
}
```

**Response:**
Returns a `MemoResponse` object with 13 sections:
- `executive_summary`
- `business_profile`
- `jurisdictions_treaties`
- `business_structure`
- `tax_considerations`
- `legal_topics_overview`
- `legal_deep_dive`
- `market_entry_options`
- `implementation_timeline`
- `resource_budget`
- `risk_assessment`
- `next_steps`
- `appendix`

### GET `/health`

Health check endpoint.

### GET `/`

Root endpoint with API information.

## Orchestration Logic

The orchestrator automatically plans research tasks based on:

1. **Always Included**: Executive Summary, Market Entry Options, Implementation Timeline
2. **Conditional Tasks**:
   - If `industry == "Software & Technology"`: Adds Innovation Box tax regime research
   - If `entry_goals` contains "Hire employees": Adds payroll tax and employment research

## V1 Constraints

- **Hardcoded Jurisdiction**: All logic defaults to `primary_jurisdiction="Netherlands"`
- **Fixed Metadata Filters**: Qdrant searches always filter by `country="netherlands"` and `year="2025"`
- **Single Country Support**: Only Netherlands is supported in this pilot version

## Development

### Testing the API

```bash
# Using curl
curl -X POST "http://localhost:8000/generate-memo" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "industry": "Software & Technology",
    "entry_goals": ["Hire employees"]
  }'
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes

- All sections are optional in the response model to prevent UI breakage if a section fails
- The system uses GPT-4o for complex synthesis tasks
- Vector search retrieves top 5 chunks per query
- The "Street Rules" persona ensures direct, actionable advice

