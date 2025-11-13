# System Architecture Flow

## Quick Reference Diagram

```
┌─────────────┐
│ User Input  │ JSON Request
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Layer 1:        │ Validate & Convert
│ Validation      │ (Pydantic)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Layer 2:        │ Plan Tasks
│ Orchestrator    │ (Mutually Exclusive Paths)
└──────┬──────────┘
       │
       ├──→ Holding Company Path
       └──→ Generic Company Path
       │
       ▼
┌─────────────────┐
│ Layer 3:        │ For Each Task:
│ RAG Engine      │ 1. Retrieve Context
│                 │ 2. Generate Content
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Layer 4:        │ Map to Response Model
│ Response Mapper │ (Handle Variations)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Final Output    │ JSON Response
└─────────────────┘
```

## Detailed Component Flow

### Component 1: Request Handler
**Location:** `backend/app/main.py`  
**Input:** HTTP POST request with JSON  
**Output:** Validated `TaxMemoRequest` object

### Component 2: Orchestrator
**Location:** `backend/app/core/orchestrator.py`  
**Input:** `TaxMemoRequest`  
**Output:** `List[TaskPlan]`  
**Logic:** Mutually exclusive paths based on company type

### Component 3: RAG Engine
**Location:** `backend/app/services/rag_engine.py`  
**Input:** `List[TaskPlan]` + User Context  
**Output:** Dictionary of generated sections  
**Process:** Retrieval → Prompt → Generation → Parsing

### Component 4: Response Mapper
**Location:** `backend/app/main.py`  
**Input:** Raw generated sections  
**Output:** `MemoResponse` object  
**Process:** Unwrap → Map → Transform → Validate

### Component 5: JSON Serializer
**Location:** FastAPI (automatic)  
**Input:** `MemoResponse` object  
**Output:** JSON string  
**Process:** Pydantic serialization with camelCase aliases

---

## Data Transformation at Each Layer

| Layer | Input Type | Output Type | Transformation |
|-------|-----------|-------------|----------------|
| 1. Validation | JSON string | Pydantic model | Parse, validate, convert |
| 2. Orchestration | Request model | Task list | Analyze, plan, route |
| 3. RAG | Task list | Section dict | Retrieve, generate, parse |
| 4. Mapping | Section dict | Response model | Unwrap, map, transform |
| 5. Serialization | Response model | JSON string | Serialize, alias |

---

## Error Handling Flow

```
Request
  ↓
[Validation Error?] → 422 Unprocessable Entity
  ↓
[Orchestration Error?] → 500 Internal Server Error
  ↓
[RAG Error?] → Log error, return None for section
  ↓
[Mapping Error?] → Use defaults, log warning
  ↓
[Serialization Error?] → 500 Internal Server Error
  ↓
Success Response
```

---

## Context Flow (RAG Process)

```
User Query: "Participation exemption"
    ↓
Search Query: "Netherlands participation exemption..."
    ↓
Embedding: [0.123, -0.456, ...] (1536 dims)
    ↓
Qdrant Search: Top 5 chunks
    ↓
Context String:
  "Context 1: Participation exemption requires BV...
   Context 2: Minimum 5% ownership...
   ..."
    ↓
Full Prompt:
  [System Prompt]
  [Context]
  [User Context]
  [Schema Example]
  [Instructions]
    ↓
GPT-4o Generation
    ↓
JSON Response
    ↓
Cleaned & Parsed
    ↓
Section Content
```

---

This architecture ensures clean separation of concerns, proper error handling, and maintainable code structure.

