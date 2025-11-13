# Tax Memo Orchestrator API - Complete Documentation (V1)

## Table of Contents
1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Supported Fields (23 Fields)](#supported-fields-23-fields)
4. [Unsupported Fields](#unsupported-fields)
5. [API Endpoints](#api-endpoints)
6. [Request/Response Examples](#requestresponse-examples)
7. [V1 Limitations](#v1-limitations)
8. [Architecture](#architecture)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The **Tax Memo Orchestrator API** is a FastAPI backend that generates comprehensive 13-section market entry memos for companies entering the Netherlands. It uses:

- **RAG (Retrieval-Augmented Generation)**: Queries a Qdrant vector database for relevant Dutch tax/legal documents
- **OpenAI GPT-4o**: Generates structured memo sections based on retrieved context
- **Orchestrator Logic**: Plans research tasks based on input conditions

### Key Features
- ✅ 23-field input model with flexible company data
- ✅ 13-section structured memo output
- ✅ Conditional research task planning
- ✅ RAG-based knowledge retrieval from Dutch documents
- ✅ "Street Rules" persona for practical, actionable advice

---

## How It Works

### Step-by-Step Process

```
1. User sends POST /generate-memo with JSON request
   ↓
2. Orchestrator analyzes input and plans research tasks
   ↓
3. For each task:
   - RAG Engine queries Qdrant vector DB (netherlands_pilot collection)
   - Retrieves top 5 relevant document chunks
   - Formats context for GPT-4o
   ↓
4. GPT-4o generates memo section using:
   - Master System Prompt ("Street Rules" persona)
   - Retrieved context from Qdrant
   - User context from request
   ↓
5. All sections mapped to structured response model
   ↓
6. Returns 13-section memo as JSON
```

### Detailed Flow

#### 1. Request Validation
- FastAPI validates JSON against `TaxMemoRequest` Pydantic model
- Only `company_name` is required (all other 22 fields are optional)
- Invalid fields cause 422 Unprocessable Entity error

#### 2. Orchestrator Task Planning
The orchestrator (`app/core/orchestrator.py`) plans research tasks:

**Always Included (Default Tasks):**
- Executive Summary Research
- Market Entry Options Research
- Tax Overview Research
- Implementation Timeline Research
- Business Structure Research
- Legal Overview Research

**Conditional Tasks (Based on Input):**

| Condition | Additional Task |
|-----------|----------------|
| `industry == "Software & Technology"` | WBSO and Innovation Box Tax Credits Research |
| `selected_legal_topics` contains `"employment-law"` | Dutch Employment Contracts and 30% Ruling Research |
| `entry_goals` contains `"Hire employees"` | Payroll Tax and Employment Research |

#### 3. RAG Engine Retrieval
For each task:
1. **Query Embedding**: Converts search query to vector using `text-embedding-3-small`
2. **Vector Search**: Searches Qdrant collection `netherlands_pilot` for top 5 matches
3. **Context Formatting**: Extracts `page_content` and `source_filename` from results
4. **Context String**: Combines all retrieved chunks into formatted context

#### 4. LLM Generation
- **Model**: OpenAI GPT-4o
- **System Prompt**: Master System Prompt from `app/utils/persona.py`
- **User Context**: Company name, industry, entry goals, etc.
- **Output**: Structured JSON matching section schema

#### 5. Response Mapping
- Raw generated sections mapped to `MemoResponse` model
- All 13 sections are Optional (can be `null` if generation fails)
- Returns structured JSON response

---

## Supported Fields (23 Fields)

### Required Fields (1)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `company_name` | `string` | **REQUIRED** - Name of the company | `"TechStart Inc"` |

### Optional Fields (22)

#### Company Information (4 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `industry` | `string` | Industry sector | `"Software & Technology"` |
| `company_type` | `string` | Type of company | `"LLC"`, `"Corporation"` |
| `founding_year` | `integer` | Year company was founded | `2020` |
| `headquarters_location` | `string` | Current headquarters | `"United States"` |

#### Jurisdiction & Entry (4 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `primary_jurisdiction` | `string` | Primary jurisdiction (V1: defaults to "Netherlands") | `"Netherlands"` |
| `target_markets` | `array[string]` | Target markets for expansion | `["Netherlands", "Belgium"]` |
| `entry_goals` | `array[string]` | List of entry goals | `["Hire employees", "Establish office"]` |
| `selected_legal_topics` | `array[string]` | Selected legal topics | `["employment-law", "tax-compliance"]` |

**Special Behavior:**
- `entry_goals` containing `"Hire employees"` triggers employment research
- `selected_legal_topics` containing `"employment-law"` triggers employment law research

#### Financial Information (4 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `current_revenue` | `float` | Current annual revenue | `1000000.0` |
| `projected_revenue` | `float` | Projected revenue in target market | `2500000.0` |
| `budget_range` | `string` | Budget range for market entry | `"€50,000 - €100,000"` |
| `funding_status` | `string` | Funding status | `"Bootstrapped"`, `"VC-backed"` |

#### Operational Information (4 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `employee_count` | `integer` | Current number of employees | `15` |
| `planned_employees` | `integer` | Planned employees in target market | `25` |
| `current_operations` | `array[string]` | Current operations/activities | `["Software development", "SaaS platform"]` |
| `key_products_services` | `array[string]` | Key products or services | `["Cloud-based CRM", "API integrations"]` |

#### Timeline & Planning (3 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timeline_preference` | `string` | Preferred timeline | `"3 months"`, `"6 months"`, `"Medium-term (3-6 months)"` |
| `urgency_level` | `string` | Urgency level | `"High"`, `"Medium"`, `"Low"` |
| `preferred_structure` | `string` | Preferred business structure | `"BV"`, `"Branch"`, `"Subsidiary"` |

#### Additional Context (3 fields)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tax_considerations` | `array[string]` | Specific tax considerations | `["Corporate income tax", "VAT registration"]` |
| `compliance_priorities` | `array[string]` | Compliance priorities | `["GDPR compliance", "Employment law"]` |
| `additional_context` | `string` | Any additional context | `"We need to hire local developers in Amsterdam."` |

---

## Unsupported Fields

The following fields from your requests are **NOT supported** in V1:

### Fields Not in API Model

| Your Field | Status | Reason | Alternative |
|------------|--------|--------|-------------|
| `businessName` | ❌ Not supported | Use `company_name` (snake_case) | `company_name` |
| `companySize` | ❌ Not supported | Use `employee_count` (integer) | `employee_count: 25` |
| `currentMarkets` | ❌ Not supported | Use `target_markets` | `target_markets` |
| `entryGoals` | ❌ Not supported | Use `entry_goals` (snake_case) | `entry_goals` |
| `timeline` | ❌ Not supported | Use `timeline_preference` | `timeline_preference` |
| `primaryJurisdiction` | ❌ Not supported | Use `primary_jurisdiction` (snake_case) | `primary_jurisdiction` |
| `taxQueries` | ❌ Not supported | Use `tax_considerations` | `tax_considerations` |
| `transactionTypes` | ❌ Not supported | Use `current_operations` | `current_operations` |
| `specificConcerns` | ❌ Not supported | Use `additional_context` | `additional_context` |
| `selectedLegalTopics` | ❌ Not supported | Use `selected_legal_topics` (snake_case) | `selected_legal_topics` |
| `expectedRevenue` | ❌ Not supported | Use `projected_revenue` | `projected_revenue` |
| `compliancePriorities` | ❌ Not supported | Use `compliance_priorities` (snake_case) | `compliance_priorities` |
| `businessStructure` | ❌ Not supported | Use `preferred_structure` | `preferred_structure` |
| `entryOption` | ❌ Not supported | Use `preferred_structure` | `preferred_structure` |
| `memoName` | ❌ Not supported | Client-side metadata | Store on client side |

### Multi-Entity Fields (Not in V1 Scope)

| Field | Status | Reason | Future Support? |
|-------|--------|--------|-----------------|
| `companies` | ❌ Not supported | V1 focuses on single company | ✅ Planned for V2 |
| `relationships` | ❌ Not supported | Not in V1 scope | ✅ Planned for V2 |
| `secondaryJurisdictions` | ❌ Not supported | V1: Netherlands only | ✅ Planned for V2 |
| `taxTreaties` | ❌ Not supported | Inferred from jurisdiction | ⚠️ Maybe V2 |
| `legalTopicData` | ❌ Not supported | Use `selected_legal_topics` | ⚠️ Maybe V2 |

### Field Naming Rules

**CRITICAL:** All field names must be in **snake_case** (underscores), not camelCase.

- ✅ Correct: `company_name`, `entry_goals`, `timeline_preference`
- ❌ Wrong: `businessName`, `entryGoals`, `timeline`

---

## API Endpoints

### POST `/generate-memo`

Generates a comprehensive 13-section market entry memo.

**URL:** `http://localhost:8000/generate-memo`

**Method:** `POST`

**Content-Type:** `application/json`

**Request Body:** `TaxMemoRequest` (see [Supported Fields](#supported-fields-23-fields))

**Response:** `MemoResponse` (13 sections)

**Response Time:** ~30-120 seconds (depends on number of sections)

**Status Codes:**
- `200 OK` - Memo generated successfully
- `422 Unprocessable Entity` - Invalid request (wrong field names/types)
- `500 Internal Server Error` - Server error during generation

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET `/`

Root endpoint with API information.

**Response:**
```json
{
  "message": "Tax Memo Orchestrator API",
  "version": "1.0.0",
  "status": "operational"
}
```

### GET `/docs`

Interactive API documentation (Swagger UI).

**URL:** `http://localhost:8000/docs`

---

## Request/Response Examples

### Minimal Request (Only Required Field)

```json
{
  "company_name": "Simple Trading LLC"
}
```

**Response:** Returns memo with default sections (Executive Summary, Entry Options, Tax Overview, Timeline).

### Full Request Example

```json
{
  "company_name": "TechStart Inc",
  "industry": "Software & Technology",
  "company_type": "LLC",
  "founding_year": 2020,
  "headquarters_location": "United States",
  "primary_jurisdiction": "Netherlands",
  "target_markets": ["Netherlands", "Belgium"],
  "entry_goals": [
    "Hire employees",
    "Establish office",
    "Register for VAT"
  ],
  "selected_legal_topics": [
    "employment-law",
    "tax-compliance"
  ],
  "current_revenue": 1000000.0,
  "projected_revenue": 2500000.0,
  "budget_range": "€50,000 - €100,000",
  "funding_status": "VC-backed",
  "employee_count": 15,
  "planned_employees": 25,
  "current_operations": [
    "Software development",
    "SaaS platform"
  ],
  "key_products_services": [
    "Cloud-based CRM software",
    "API integrations"
  ],
  "timeline_preference": "6 months",
  "urgency_level": "Medium",
  "preferred_structure": "BV",
  "tax_considerations": [
    "Corporate income tax",
    "VAT registration",
    "WBSO tax credits"
  ],
  "compliance_priorities": [
    "GDPR compliance",
    "Employment law compliance"
  ],
  "additional_context": "We are a fast-growing SaaS company looking to expand into the European market."
}
```

**What This Triggers:**
- ✅ Default tasks (Executive Summary, Entry Options, Tax Overview, Timeline)
- ✅ **WBSO/Innovation Box research** (because `industry == "Software & Technology"`)
- ✅ **Employment law research** (because `selected_legal_topics` contains `"employment-law"`)
- ✅ **Payroll research** (because `entry_goals` contains `"Hire employees"`)

### Response Structure

```json
{
  "executive_summary": {
    "overview": "TechStart Inc should consider establishing a BV...",
    "key_recommendations": [
      "Register for VAT within 30 days",
      "Apply for WBSO tax credits"
    ],
    "critical_considerations": [
      "2025 corporate tax rate: 25.8%",
      "VAT registration required for B2B sales"
    ]
  },
  "business_profile": { ... },
  "jurisdictions_treaties": { ... },
  "business_structure": { ... },
  "tax_considerations": { ... },
  "legal_topics_overview": { ... },
  "legal_deep_dive": { ... },
  "market_entry_options": { ... },
  "implementation_timeline": { ... },
  "resource_budget": { ... },
  "risk_assessment": { ... },
  "next_steps": { ... },
  "appendix": { ... }
}
```

**Note:** All sections are Optional. If a section fails to generate, it will be `null`.

---

## V1 Limitations

### Hardcoded Constraints

1. **Primary Jurisdiction**: Always defaults to `"Netherlands"`
   - Even if you provide `primary_jurisdiction: "Germany"`, it will still generate Netherlands-focused memos

2. **Collection Name**: Hardcoded to `"netherlands_pilot"`
   - Cannot query other collections

3. **Embedding Model**: Fixed to `text-embedding-3-small` (1536 dimensions)
   - Cannot use other embedding models

4. **LLM Model**: Fixed to `gpt-4o`
   - Cannot switch to other models

### Functional Limitations

1. **Single Company Only**: Cannot handle multi-entity structures
   - No support for parent/subsidiary relationships
   - No support for `companies` array

2. **No Secondary Jurisdictions**: Only primary jurisdiction supported
   - Cannot analyze cross-border scenarios with multiple countries

3. **No Treaty Selection**: Tax treaties inferred from jurisdiction
   - Cannot explicitly specify which treaties to consider

4. **Limited Conditional Logic**: Only 3 conditional triggers
   - Software & Technology → WBSO research
   - employment-law topic → Employment law research
   - "Hire employees" goal → Payroll research

5. **No Custom Sections**: Fixed 13-section structure
   - Cannot add or remove sections

6. **No Section Ordering**: Sections generated in fixed order
   - Cannot customize section sequence

### Data Limitations

1. **Knowledge Base**: Only searches `netherlands_pilot` collection
   - Limited to documents ingested in that collection
   - No access to other knowledge bases

2. **No Real-Time Data**: Uses static document knowledge
   - Cannot fetch real-time tax rates or regulations
   - Relies on ingested documents (may be outdated)

3. **No External APIs**: No integration with tax authorities or legal databases
   - Pure RAG-based, no live data sources

---

## Architecture

### Component Overview

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
         ├──► Orchestrator (orchestrator.py)
         │    └──► Plans research tasks based on input
         │
         ├──► RAG Engine (rag_engine.py)
         │    ├──► Qdrant Service (qdrant.py)
         │    │    └──► Queries netherlands_pilot collection
         │    └──► OpenAI Client
         │         └──► Generates sections with GPT-4o
         │
         └──► Response Mapper
              └──► Maps generated sections to MemoResponse
```

### File Structure

```
backend/app/
├── main.py                 # FastAPI app, POST /generate-memo endpoint
├── core/
│   ├── config.py           # Environment settings (Pydantic V2)
│   └── orchestrator.py     # Task planning logic
├── models/
│   ├── request.py          # TaxMemoRequest (23 fields)
│   └── response.py         # MemoResponse (13 sections)
├── services/
│   ├── qdrant.py           # Qdrant vector DB service
│   └── rag_engine.py        # RAG engine (retrieval + generation)
└── utils/
    └── persona.py          # Master System Prompt
```

### Data Flow

1. **Request** → `TaxMemoRequest` model validation
2. **Orchestrator** → Generates `TaskPlan` list
3. **RAG Engine** → For each task:
   - Query → Embedding → Qdrant search → Context
   - Context + Prompt → GPT-4o → Section JSON
4. **Mapper** → Raw sections → `MemoResponse` model
5. **Response** → JSON with 13 sections

---

## Troubleshooting

### Common Errors

#### 422 Unprocessable Entity

**Cause:** Invalid field names or types

**Solutions:**
- ✅ Use snake_case: `company_name` not `businessName`
- ✅ Use correct field names: `entry_goals` not `entryGoals`
- ✅ Use correct types: `employee_count: 25` not `"Small (11-50 employees)"`
- ✅ Remove unsupported fields: `companies`, `relationships`, `memoName`

**Check:** View error details in response body for specific field issues

#### 500 Internal Server Error

**Possible Causes:**
- Qdrant connection failure
- OpenAI API key invalid/expired
- Collection `netherlands_pilot` doesn't exist
- Network timeout

**Solutions:**
- Check `.env` file has correct `QDRANT_URL`, `QDRANT_API_KEY`, `OPENAI_API_KEY`
- Verify Qdrant collection exists: Run `ingest_data.py` first
- Check server logs for detailed error

#### Empty Sections in Response

**Cause:** RAG retrieval found no relevant context, or generation failed

**Solutions:**
- Ensure `netherlands_pilot` collection has documents (run `ingest_data.py`)
- Try more specific queries in `tax_considerations` or `additional_context`
- Check OpenAI API quota/limits

#### Slow Response Times

**Normal:** 30-120 seconds (depends on number of sections)

**Optimization:**
- Reduce number of conditional triggers (fewer sections = faster)
- Use minimal request (only `company_name`) for faster response

### Field Name Quick Reference

| ❌ Wrong (camelCase) | ✅ Correct (snake_case) |
|---------------------|------------------------|
| `businessName` | `company_name` |
| `entryGoals` | `entry_goals` |
| `timeline` | `timeline_preference` |
| `primaryJurisdiction` | `primary_jurisdiction` |
| `taxQueries` | `tax_considerations` |
| `selectedLegalTopics` | `selected_legal_topics` |
| `compliancePriorities` | `compliance_priorities` |

---

## Summary

### What Works in V1 ✅

- 23-field input model (1 required, 22 optional)
- 13-section memo output
- Conditional task planning (3 triggers)
- RAG-based knowledge retrieval
- Netherlands-focused memos
- "Street Rules" persona

### What Doesn't Work in V1 ❌

- Multi-entity structures (`companies`, `relationships`)
- Secondary jurisdictions
- Custom sections
- Other countries (hardcoded to Netherlands)
- Real-time data
- camelCase field names

### Quick Start

1. **Start server:** `uvicorn app.main:app --reload`
2. **Test:** `POST http://localhost:8000/generate-memo`
3. **View docs:** `http://localhost:8000/docs`

---

**Version:** 1.0.0 (Netherlands Pilot)  
**Last Updated:** 2025

