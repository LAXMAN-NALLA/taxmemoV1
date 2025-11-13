# Content Flow Diagram: From Prompt to Final Output

## 🎯 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER REQUEST (JSON)                                │
│  {                                                                           │
│    "companyName": "European Holdings BV",                                   │
│    "industry": "Financial Services",                                         │
│    "companyType": "Holding Company",                                         │
│    "entryGoals": ["Tax optimization"],                                      │
│    "taxConsiderations": ["Participation exemption"]                          │
│  }                                                                           │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: REQUEST VALIDATION                               │
│                         (FastAPI + Pydantic)                                │
│                                                                              │
│  Purpose: Validate JSON structure, field names, data types                  │
│  Location: backend/app/models/request.py                                    │
│                                                                              │
│  ✓ Validates: companyName (required), optional fields                       │
│  ✓ Converts: camelCase ↔ snake_case automatically                          │
│  ✓ Returns: TaxMemoRequest object or 422 error                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 2: TASK ORCHESTRATION                              │
│                    (Mutually Exclusive Paths)                               │
│                         backend/app/core/orchestrator.py                     │
│                                                                              │
│  Purpose: Analyze request and plan research tasks based on company type     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  DETECTION LOGIC                                                    │    │
│  │  • Is holding company? (companyType contains "holding")            │    │
│  │  • Participation exemption query? (in taxConsiderations)           │    │
│  │  • Software & Technology? (industry match)                        │    │
│  │  • Hiring employees? (in entryGoals)                               │    │
│  └───────────────────────────────┬────────────────────────────────────┘    │
│                                  │                                           │
│                    ┌─────────────┴─────────────┐                            │
│                    │                           │                            │
│                    ▼                           ▼                            │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐          │
│  │  PATH A: HOLDING COMPANY    │  │  PATH B: GENERIC COMPANY   │          │
│  │  (Mutually Exclusive)       │  │  (Default Path)             │          │
│  │                             │  │                             │          │
│  │  Task 1: Executive Summary  │  │  Task 1: Executive Summary  │          │
│  │    for Holding Company      │  │    (Generic)               │          │
│  │                             │  │                             │          │
│  │  Task 2: BV Structure for   │  │  Task 2: Market Entry      │          │
│  │    Participation Exemption  │  │    Options (Branch/BV)     │          │
│  │                             │  │                             │          │
│  │  Task 3: Participation      │  │  Task 3: Tax Overview      │          │
│  │    Exemption Deep Dive      │  │    (General)               │          │
│  │                             │  │                             │          │
│  │  Task 4: Corporate Tax for  │  │  Task 4: Implementation    │          │
│  │    Holding Companies        │  │    Timeline                │          │
│  │                             │  │                             │          │
│  │  Task 5: BV Setup Timeline  │  │  + Conditional Tasks:       │          │
│  │                             │  │    • WBSO (if Tech)        │          │
│  │  NO Branch Office tasks     │  │    • Employment (if hiring) │          │
│  │  NO Innovation Box tasks    │  │                             │          │
│  └─────────────┬───────────────┘  └─────────────┬───────────────┘          │
│                │                                 │                          │
│                └─────────────┬───────────────────┘                          │
│                              │                                               │
│                              ▼                                               │
│                    List[TaskPlan] objects                                    │
│                    Each contains:                                           │
│                    • task_name                                              │
│                    • search_query                                            │
│                    • section_name                                            │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 3: RAG ENGINE                                       │
│                    backend/app/services/rag_engine.py                       │
│                                                                              │
│  Purpose: For each task, retrieve relevant context and generate content     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  FOR EACH TASK IN TASK LIST:                                       │    │
│  │                                                                     │    │
│  │  Step 3.1: CONTEXT RETRIEVAL                                       │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │  Query: "Netherlands participation exemption..."            │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  OpenAI Embeddings API                                       │  │    │
│  │  │  (text-embedding-3-small)                                    │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  Vector: [0.123, -0.456, ..., 0.789] (1536 dimensions)     │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  Qdrant Vector Search                                       │  │    │
│  │  │  Collection: "netherlands_pilot"                             │  │    │
│  │  │  Top 5 similar chunks                                       │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  Retrieved Documents:                                        │  │    │
│  │  │  • Context 1: "Participation exemption requires BV..."     │  │    │
│  │  │  • Context 2: "Minimum 5% ownership required..."           │  │    │
│  │  │  • Context 3: "Motive test must be passed..."               │  │    │
│  │  │  • Context 4: "Dividends and capital gains exempt..."      │  │    │
│  │  │  • Context 5: "BV structure is mandatory..."                │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  Step 3.2: PROMPT CONSTRUCTION                                      │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │  Components:                                                 │  │    │
│  │  │  1. MASTER_SYSTEM_PROMPT (Street Rules persona)             │  │    │
│  │  │  2. Retrieved context from Qdrant                           │  │    │
│  │  │  3. User context (company name, industry, goals)            │  │    │
│  │  │  4. Expected JSON schema example                            │  │    │
│  │  │  5. Specific instructions for section generation            │  │    │
│  │  │                                                              │  │    │
│  │  │  Full Prompt Structure:                                      │  │    │
│  │  │  ┌──────────────────────────────────────────────────────┐  │    │
│  │  │  │ [MASTER_SYSTEM_PROMPT]                                │  │    │
│  │  │  │ "You are an experienced, direct, entrepreneurial..."  │  │    │
│  │  │  │                                                        │  │    │
│  │  │  │ TASK: Generate "tax_considerations" section           │  │    │
│  │  │  │                                                        │  │    │
│  │  │  │ CONTEXT FROM KNOWLEDGE BASE:                          │  │    │
│  │  │  │ [Retrieved document chunks]                            │  │    │
│  │  │  │                                                        │  │    │
│  │  │  │ USER CONTEXT:                                          │  │    │
│  │  │  │ Company: European Holdings BV                          │  │    │
│  │  │  │ Industry: Financial Services                           │  │    │
│  │  │  │ Entry Goals: Tax optimization                          │  │    │
│  │  │  │                                                        │  │    │
│  │  │  │ EXPECTED JSON STRUCTURE:                              │  │    │
│  │  │  │ {                                                      │  │    │
│  │  │  │   "corporate_tax_rate": "...",                         │  │    │
│  │  │  │   "special_regimes": ["Participation Exemption..."]    │  │    │
│  │  │  │ }                                                      │  │    │
│  │  │  │                                                        │  │    │
│  │  │  │ INSTRUCTIONS:                                          │  │    │
│  │  │  │ 1. Extract relevant information                       │  │    │
│  │  │  │ 2. Return ONLY valid JSON                              │  │    │
│  │  │  │ 3. Include Participation Exemption in special_regimes  │  │    │
│  │  │  └──────────────────────────────────────────────────────┘  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  Step 3.3: LLM GENERATION                                          │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │  OpenAI GPT-4o API Call                                      │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  Response: JSON string (may have markdown formatting)      │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  JSON Cleaning:                                             │  │    │
│  │  │  • Remove ```json markers                                   │  │    │
│  │  │  • Extract JSON object from text                            │  │    │
│  │  │         ↓                                                    │  │    │
│  │  │  Parsed JSON:                                               │  │    │
│  │  │  {                                                           │  │    │
│  │  │    "corporate_tax_rate": "25.8% for 2025",                 │  │    │
│  │  │    "tax_obligations": [...],                                │  │    │
│  │  │    "tax_optimization_strategies": [...],                    │  │    │
│  │  │    "special_regimes": [                                     │  │    │
│  │  │      "Participation Exemption (deelnemingsvrijstelling)"   │  │    │
│  │  │    ]                                                         │  │    │
│  │  │  }                                                           │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Result: Dictionary mapping section_name → generated content                │
│  Example: {                                                                  │
│    "executive_summary": {...},                                               │
│    "tax_considerations": {...},                                              │
│    "business_structure": {...}                                              │
│  }                                                                           │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 4: RESPONSE MAPPING                                 │
│                    backend/app/main.py (map_sections_to_response)            │
│                                                                              │
│  Purpose: Transform raw generated sections into structured response model    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  For each section in generated sections:                           │    │
│  │                                                                     │    │
│  │  1. UNWRAP NESTED STRUCTURES                                        │    │
│  │     • Check if section name appears as key                         │    │
│  │     • Extract inner content if nested                              │    │
│  │                                                                     │    │
│  │  2. FLEXIBLE KEY MAPPING                                           │    │
│  │     • Try multiple key name variations                             │    │
│  │     • Handle snake_case and camelCase                              │    │
│  │     • Fallback to "content" key                                    │    │
│  │                                                                     │    │
│  │  3. TYPE TRANSFORMATIONS                                           │    │
│  │     • pros_and_cons: {option: {pros: [], cons: []}}               │    │
│  │       → {option: [combined list]}                                  │    │
│  │     • Ensure lists are lists, dicts are dicts                      │    │
│  │                                                                     │    │
│  │  4. MAP TO RESPONSE MODEL                                          │    │
│  │     • ExecutiveSummary(...)                                        │    │
│  │     • TaxSection(...)                                              │    │
│  │     • EntryOptionsSection(...)                                     │    │
│  │     • etc.                                                         │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Result: MemoResponse object with 13 optional sections                      │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 5: FINAL OUTPUT (JSON)                              │
│                                                                              │
│  {                                                                           │
│    "executiveSummary": {                                                     │
│      "overview": null,                                                       │
│      "keyRecommendations": [                                                 │
│        "Leverage the Participation Exemption...",                          │
│        "Set up a BV structure (required for exemption)..."                   │
│      ],                                                                      │
│      "criticalConsiderations": [...]                                         │
│    },                                                                        │
│    "taxConsiderations": {                                                    │
│      "corporateTaxRate": "25.8% for 2025",                                   │
│      "taxObligations": [...],                                                │
│      "taxOptimizationStrategies": [                                          │
│        "Utilize Participation Exemption..."                                 │
│      ],                                                                      │
│      "specialRegimes": [                                                     │
│        "Participation Exemption (deelnemingsvrijstelling)"                  │
│      ]                                                                       │
│    },                                                                        │
│    "businessStructure": {                                                    │
│      "recommendedStructure": "BV (required for participation exemption)",    │
│      ...                                                                     │
│    },                                                                        │
│    ... (other sections)                                                      │
│  }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Layer-by-Layer Breakdown

### **Layer 1: Request Validation**
**File:** `backend/app/models/request.py`  
**Purpose:** 
- Validate JSON structure
- Convert camelCase ↔ snake_case
- Ensure required fields present
- Type checking

**Key Features:**
- Pydantic model validation
- Automatic alias conversion
- Error messages for invalid fields

---

### **Layer 2: Task Orchestration**
**File:** `backend/app/core/orchestrator.py`  
**Purpose:**
- Analyze company type and goals
- Plan research tasks
- Prevent context bleed-over with mutually exclusive paths

**Key Features:**
- **Holding Company Path:** Only BV/participation exemption tasks
- **Generic Path:** Standard market entry tasks
- Conditional task addition (WBSO for tech, employment for hiring)

**Critical Logic:**
```python
if is_holding_company:
    # ONLY holding-specific tasks
    # NO branch office tasks
    # NO innovation box tasks
else:
    # Generic tasks
    # + conditional additions
```

---

### **Layer 3: RAG Engine**
**File:** `backend/app/services/rag_engine.py`  
**Purpose:**
- Retrieve relevant documents from knowledge base
- Generate section content using LLM
- Clean and parse JSON responses

**Sub-layers:**

#### 3.1 Context Retrieval
- Query → Embedding (OpenAI)
- Vector Search (Qdrant)
- Top 5 relevant chunks
- Format context string

#### 3.2 Prompt Construction
- Master System Prompt (persona)
- Retrieved context
- User context
- JSON schema example
- Specific instructions

#### 3.3 LLM Generation
- GPT-4o API call
- JSON cleaning (remove markdown)
- JSON parsing
- Error handling

---

### **Layer 4: Response Mapping**
**File:** `backend/app/main.py`  
**Purpose:**
- Transform raw LLM output to structured response
- Handle various JSON formats
- Type conversions
- Map to Pydantic models

**Key Features:**
- Unwrap nested structures
- Flexible key mapping
- Type transformations (pros_and_cons)
- Default values for missing fields

---

### **Layer 5: Final Output**
**Purpose:**
- Structured JSON response
- 13 optional sections
- camelCase field names (for frontend)
- Validated by Pydantic

---

## 🔄 Complete Data Flow

```
User JSON Request
    ↓
[Layer 1] Request Validation (Pydantic)
    ↓
TaxMemoRequest Object
    ↓
[Layer 2] Task Orchestration
    ↓
    ├─→ Holding Company? → Path A (Holding-specific tasks)
    └─→ Else → Path B (Generic tasks)
    ↓
List[TaskPlan] (5 tasks for holding, 4+ for generic)
    ↓
[Layer 3] RAG Engine (for each task)
    ↓
    ├─→ Query → Embedding (OpenAI)
    ├─→ Vector Search (Qdrant) → Top 5 chunks
    ├─→ Build Prompt (Context + User Context + Schema)
    ├─→ LLM Generation (GPT-4o)
    └─→ JSON Cleaning & Parsing
    ↓
Generated Sections Dictionary
    ↓
[Layer 4] Response Mapping
    ↓
    ├─→ Unwrap nested structures
    ├─→ Flexible key mapping
    ├─→ Type transformations
    └─→ Map to Pydantic models
    ↓
MemoResponse Object
    ↓
[Layer 5] Final JSON Output
    ↓
User receives structured memo
```

---

## 🎯 Key Design Decisions

### 1. **Mutually Exclusive Paths**
**Why:** Prevents context bleed-over (e.g., Branch Office for holding companies)  
**How:** If/else logic in orchestrator

### 2. **RAG Architecture**
**Why:** Combines knowledge base retrieval with LLM generation  
**How:** Vector search → Context → Prompt → Generation

### 3. **Flexible Mapping**
**Why:** LLMs return various JSON formats  
**How:** Multiple key name attempts, type conversions

### 4. **JSON Cleaning**
**Why:** LLMs often wrap JSON in markdown  
**How:** Regex extraction, markdown removal

### 5. **Schema Examples in Prompt**
**Why:** Guide LLM to return correct structure  
**How:** Include expected JSON structure in prompt

---

## 📈 Performance Flow

```
Request Received
    ↓ (0ms)
Validation: ~1ms
    ↓
Orchestration: ~5ms
    ↓
RAG Generation (per task):
    ├─ Embedding: ~200ms
    ├─ Qdrant Search: ~50ms
    ├─ LLM Call: ~2000-5000ms
    └─ JSON Parsing: ~10ms
    ↓
Mapping: ~10ms
    ↓
Response: ~30-120 seconds total
```

---

## 🔍 Quality Assurance Layers

1. **Validation Layer:** Catches invalid requests early
2. **Orchestration Layer:** Ensures correct task selection
3. **Retrieval Layer:** Gets relevant context
4. **Generation Layer:** Produces structured output
5. **Mapping Layer:** Handles format variations
6. **Response Layer:** Validates final structure

---

This architecture ensures:
- ✅ Correct context for each company type
- ✅ No conflicting recommendations
- ✅ Structured, validated output
- ✅ Flexible handling of LLM variations
- ✅ Scalable to multiple countries

