# Code Flow Explanation - Document to Memo Generation

## Overview

This document explains the complete code flow with a concrete example: **How a single document is ingested, stored, and retrieved to generate a memo section**.

---

## Example Scenario

Let's trace through the system with this example:
- **Document**: `source docs/wbso_2025.txt` (WBSO tax credit information)
- **User Query**: "What are the WBSO R&D tax credit rates for 2025?"
- **Generated Section**: `tax_considerations` section of the memo

---

## Part 1: Document Ingestion (Storage)

### File: `backend/ingest_data.py`

### Step 1: Load the Document

```python
# Line 40: Define loader for TXT files
txt_loader = DirectoryLoader(
    SOURCE_DIR,                    # "../source docs"
    glob="**/*.txt",               # Find all .txt files
    loader_cls=TextLoader,         # Use TextLoader class
    loader_kwargs={"encoding": "utf-8"}
)

# Line 56: Load the document
txt_docs = txt_loader.load()
```

**What happens:**
- LangChain's `TextLoader` reads `source docs/wbso_2025.txt`
- File content: `"De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) is een Nederlandse fiscale stimuleringsregeling..."`
- Creates a `Document` object:
  ```python
  Document(
      page_content="De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk)...",
      metadata={"source": "../source docs/wbso_2025.txt"}
  )
  ```

### Step 2: Split into Chunks

```python
# Line 69-73: Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Max 1000 characters per chunk
    chunk_overlap=200,      # 200 characters overlap between chunks
    separators=["\n\n", "\n", " ", ""]  # Split on paragraphs, lines, spaces
)

# Line 75: Split the document
chunks = text_splitter.split_documents(all_docs)
```

**What happens:**
- Original document (500 characters) → **1 chunk** (since it's < 1000 chars)
- If document was 2000 characters → **3 chunks** (with 200 char overlap)
- Each chunk is a separate `Document` object

**Example chunk:**
```python
Document(
    page_content="De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) is een Nederlandse fiscale stimuleringsregeling voor bedrijven die speur- en ontwikkelingswerk (S&O) verrichten. Voor 2025 zijn de tarieven als volgt: Eerste schijf (tot €350.000 S&O-loon): 32% van de S&O-loonkosten...",
    metadata={"source": "../source docs/wbso_2025.txt"}
)
```

### Step 3: Add Metadata

```python
# Line 79-83: Add source filename to metadata
for chunk in chunks:
    source = chunk.metadata.get("source", "unknown")
    filename = os.path.basename(source)  # "wbso_2025.txt"
    chunk.metadata["source_filename"] = filename
```

**Result:**
```python
Document(
    page_content="De WBSO...",
    metadata={
        "source": "../source docs/wbso_2025.txt",
        "source_filename": "wbso_2025.txt"  # Added
    }
)
```

### Step 4: Generate Embeddings and Store in Qdrant

```python
# Line 87: Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Line 106-110: Initialize QdrantVectorStore
qdrant = QdrantVectorStore(
    client=client,
    collection_name="netherlands_pilot",
    embedding=embeddings,
)

# Line 112: Add documents (this does embedding + storage)
qdrant.add_documents(chunks)
```

**What happens internally:**

1. **For each chunk**, LangChain calls OpenAI:
   ```python
   # LangChain internally does:
   embedding_vector = openai.embeddings.create(
       model="text-embedding-3-small",
       input="De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk)..."
   )
   # Returns: [0.123, -0.456, 0.789, ..., 0.234] (1536 numbers)
   ```

2. **Store in Qdrant:**
   ```python
   # LangChain internally does:
   qdrant_client.upsert(
       collection_name="netherlands_pilot",
       points=[
           PointStruct(
               id=uuid4(),  # Random unique ID
               vector=[0.123, -0.456, ..., 0.234],  # 1536-dim embedding
               payload={
                   "page_content": "De WBSO...",
                   "metadata": {
                       "source": "../source docs/wbso_2025.txt",
                       "source_filename": "wbso_2025.txt"
                   }
               }
           )
       ]
   )
   ```

**Result in Qdrant:**
- **Collection**: `netherlands_pilot`
- **Point ID**: `abc-123-def-456` (random UUID)
- **Vector**: `[0.123, -0.456, ..., 0.234]` (1536 dimensions)
- **Payload**: Contains the text and metadata

---

## Part 2: Document Retrieval (Query Time)

### File: `backend/app/services/qdrant.py`

### Step 1: User Makes Request

User sends:
```json
{
  "company_name": "TechStart Inc",
  "industry": "Software & Technology",
  "tax_considerations": ["WBSO R&D tax credit rates"]
}
```

### Step 2: Orchestrator Creates Search Query

**File**: `backend/app/core/orchestrator.py`

```python
# Line 66-71: Conditional task for Software & Technology
if request.industry == "Software & Technology":
    tasks.append(TaskPlan(
        task_name="WBSO and Innovation Box Tax Credits Research",
        search_query="Netherlands WBSO R&D tax credit Innovation Box tax regime software technology 2025",
        section_name="tax_considerations"
    ))
```

**Result**: Search query = `"Netherlands WBSO R&D tax credit Innovation Box tax regime software technology 2025"`

### Step 3: Convert Query to Embedding

**File**: `backend/app/services/qdrant.py`

```python
# Line 47: In search() method
query_vector = self._text_to_embedding(query)

# Line 97-119: _text_to_embedding() method
def _text_to_embedding(self, text: str) -> List[float]:
    response = self.openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text  # "Netherlands WBSO R&D tax credit..."
    )
    return response.data[0].embedding
```

**What happens:**
- OpenAI converts query text to vector
- **Input**: `"Netherlands WBSO R&D tax credit Innovation Box tax regime software technology 2025"`
- **Output**: `[0.234, -0.567, 0.890, ..., 0.123]` (1536 dimensions)

**Why this works:**
- The query embedding is **semantically similar** to the document embedding
- Even though query is in English and document is in Dutch, embeddings capture meaning
- Words like "WBSO", "tax credit", "R&D" match the Dutch content about WBSO

### Step 4: Vector Search in Qdrant

```python
# Line 50-54: Search Qdrant
search_results = self.client.search(
    collection_name=self.collection_name,  # "netherlands_pilot"
    query_vector=query_vector,             # [0.234, -0.567, ...]
    limit=limit                            # 5 (top 5 matches)
)
```

**What happens:**
1. Qdrant calculates **cosine similarity** between query vector and all stored vectors
2. Finds top 5 most similar vectors (highest cosine similarity scores)
3. Returns results with:
   - `score`: Similarity score (0.0 to 1.0, higher = more similar)
   - `payload`: The original document chunk
   - `id`: Point ID

**Example result:**
```python
[
    ScoredPoint(
        id="abc-123-def-456",
        score=0.89,  # 89% similarity - very high!
        payload={
            "page_content": "De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) is een Nederlandse fiscale stimuleringsregeling...",
            "metadata": {
                "source": "../source docs/wbso_2025.txt",
                "source_filename": "wbso_2025.txt"
            }
        }
    ),
    # ... 4 more results
]
```

### Step 5: Format Context

```python
# Line 72-95: format_context() method
def format_context(self, search_results: List[Dict[str, Any]]) -> str:
    context_parts = []
    for i, result in enumerate(search_results, 1):
        payload = result.get("payload", {})
        content = payload.get("page_content", "")  # Extract text
        metadata = payload.get("metadata", {})
        source_filename = metadata.get("source_filename", "Unknown")
        
        context_parts.append(
            f"Context {i} (Source: {source_filename}):\n{content}"
        )
    
    return "\n---\n".join(context_parts)
```

**Result:**
```
Context 1 (Source: wbso_2025.txt):
De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) is een Nederlandse fiscale stimuleringsregeling voor bedrijven die speur- en ontwikkelingswerk (S&O) verrichten. Voor 2025 zijn de tarieven als volgt: Eerste schijf (tot €350.000 S&O-loon): 32% van de S&O-loonkosten en andere S&O-kosten. Tweede schijf (boven €350.000 S&O-loon): 16% van de S&O-loonkosten en andere S&O-kosten...

---
Context 2 (Source: innovation_box.txt):
...
```

---

## Part 3: Memo Generation (RAG)

### File: `backend/app/services/rag_engine.py`

### Step 1: Retrieve Context

```python
# Line 38-39: In generate_section() method
search_results = self.qdrant_service.search(query=search_query)
context = self.qdrant_service.format_context(search_results)
```

**Result**: `context` = formatted string with top 5 document chunks (from Step 5 above)

### Step 2: Build User Context

```python
# Line 42-47: Build user context string
user_context_str = ""
if user_context:
    user_context_str = f"\n\nUSER CONTEXT:\n"
    user_context_str += f"Company: {user_context.get('company_name', 'N/A')}\n"
    user_context_str += f"Industry: {user_context.get('industry', 'N/A')}\n"
    user_context_str += f"Entry Goals: {', '.join(user_context.get('entry_goals', []))}\n"
```

**Result:**
```
USER CONTEXT:
Company: TechStart Inc
Industry: Software & Technology
Entry Goals: Hire employees, Establish office
```

### Step 3: Create Prompt

```python
# Line 49-64: Generate prompt
full_context = context + user_context_str
prompt = f"""{MASTER_SYSTEM_PROMPT}

TASK: Generate the "{section_name}" section of a Market Entry Memo for the Netherlands.

CONTEXT FROM KNOWLEDGE BASE:
{full_context}

INSTRUCTIONS:
1. Extract relevant information from the context above.
2. Write the {section_name} section in a direct, actionable style.
3. If information is missing, state that clearly rather than guessing.
4. Format your response as structured JSON that matches the expected schema.
5. Be practical and focus on what the company can actually do.
"""
```

**Full prompt sent to GPT-4o:**
```
You are an experienced, direct, entrepreneurial mentor, NOT a cautious government bureaucrat.
Your goal is to provide actionable "Street Rules" advice for entering the Netherlands.

TONE RULES:
- Be empowering and direct ("Here is what you can do...", not "It is generally recommended that...").
- Prioritize practical reality over theoretical compliance.
- Challenge dogma: If the user wants a complex Dutch BV but a simple Branch Office is better, argue for the Branch.

DATA RULES:
- You MUST use the provided CONTEXT to answer.
- If the context lacks specific 2025 rates, state "Data for 2025 currently unavailable" DO NOT HALLUCINATE.

TASK: Generate the "tax_considerations" section of a Market Entry Memo for the Netherlands.

CONTEXT FROM KNOWLEDGE BASE:
Context 1 (Source: wbso_2025.txt):
De WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) is een Nederlandse fiscale stimuleringsregeling voor bedrijven die speur- en ontwikkelingswerk (S&O) verrichten. Voor 2025 zijn de tarieven als volgt: Eerste schijf (tot €350.000 S&O-loon): 32% van de S&O-loonkosten en andere S&O-kosten. Tweede schijf (boven €350.000 S&O-loon): 16% van de S&O-loonkosten en andere S&O-kosten...

---
Context 2 (Source: innovation_box.txt):
...

USER CONTEXT:
Company: TechStart Inc
Industry: Software & Technology
Entry Goals: Hire employees, Establish office

INSTRUCTIONS:
1. Extract relevant information from the context above.
2. Write the tax_considerations section in a direct, actionable style.
3. If information is missing, state that clearly rather than guessing.
4. Format your response as structured JSON that matches the expected schema.
5. Be practical and focus on what the company can actually do.
```

### Step 4: Call GPT-4o

```python
# Line 67-75: Call OpenAI
response = self.openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Generate the {section_name} section now."}
    ],
    temperature=0.7,
    max_tokens=2000
)
```

**What happens:**
- GPT-4o reads the prompt
- Understands it needs to generate `tax_considerations` section
- Extracts WBSO information from the Dutch context
- Generates structured JSON response

**GPT-4o Response:**
```json
{
  "corporate_tax_rate": "25.8% for 2025",
  "tax_obligations": [
    "Corporate income tax (VPB)",
    "VAT registration required for B2B sales"
  ],
  "tax_optimization_strategies": [
    "Apply for WBSO R&D tax credits: First bracket (up to €350,000 S&O payroll): 32% credit. Second bracket (above €350,000): 16% credit. For startups: 40% in first bracket.",
    "Consider Innovation Box regime for qualifying IP income (effective rate: 9%)"
  ],
  "special_regimes": [
    "WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) - R&D tax credit",
    "Innovation Box - Reduced tax rate on IP income"
  ]
}
```

### Step 5: Parse and Return

```python
# Line 78-86: Parse response
content = response.choices[0].message.content

try:
    parsed = json.loads(content)  # Parse JSON
    return parsed
except json.JSONDecodeError:
    return {"content": content}  # Fallback to text
```

**Result**: Returns the parsed JSON dictionary

---

## Part 4: Response Mapping

### File: `backend/app/main.py`

### Step 1: Map to Response Model

```python
# Line 100-109: Map tax_considerations section
if "tax_considerations" in sections:
    tax_data = sections["tax_considerations"]
    if isinstance(tax_data, dict):
        response.tax_considerations = TaxSection(
            corporate_tax_rate=tax_data.get("corporate_tax_rate"),
            tax_obligations=tax_data.get("tax_obligations", []),
            tax_optimization_strategies=tax_data.get("tax_optimization_strategies", []),
            special_regimes=tax_data.get("special_regimes", [])
        )
```

**Result**: Structured `TaxSection` object with all fields populated

### Step 2: Return JSON Response

```python
# Line 196: Return response
return response
```

**Final JSON Response:**
```json
{
  "tax_considerations": {
    "corporate_tax_rate": "25.8% for 2025",
    "tax_obligations": [
      "Corporate income tax (VPB)",
      "VAT registration required for B2B sales"
    ],
    "tax_optimization_strategies": [
      "Apply for WBSO R&D tax credits: First bracket (up to €350,000 S&O payroll): 32% credit. Second bracket (above €350,000): 16% credit. For startups: 40% in first bracket.",
      "Consider Innovation Box regime for qualifying IP income (effective rate: 9%)"
    ],
    "special_regimes": [
      "WBSO (Wet Bevordering Speur- en Ontwikkelingswerk) - R&D tax credit",
      "Innovation Box - Reduced tax rate on IP income"
    ]
  },
  "executive_summary": { ... },
  "business_structure": { ... },
  // ... other sections
}
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Load Document (ingest_data.py)                          │
│    wbso_2025.txt → Document object                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Split into Chunks (RecursiveCharacterTextSplitter)      │
│    Document → [Chunk1, Chunk2, ...]                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Generate Embeddings (OpenAI text-embedding-3-small)      │
│    Chunk text → [0.123, -0.456, ..., 0.234] (1536 dims)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Store in Qdrant (QdrantVectorStore)                     │
│    Vector + Payload → Qdrant collection "netherlands_pilot" │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ (Document is now stored)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    QUERY TIME                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. User Request (main.py)                                   │
│    {"industry": "Software & Technology", ...}               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Orchestrator Plans Tasks (orchestrator.py)               │
│    Creates: "Netherlands WBSO R&D tax credit..." query     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Convert Query to Embedding (qdrant.py)                   │
│    Query text → [0.234, -0.567, ..., 0.123] (1536 dims)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Vector Search in Qdrant (qdrant.py)                      │
│    Query vector → Cosine similarity → Top 5 matches        │
│    Returns: wbso_2025.txt chunk (score: 0.89)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Format Context (qdrant.py)                              │
│    Search results → "Context 1 (Source: wbso_2025.txt):..." │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Generate Prompt (rag_engine.py)                         │
│     Context + User context + System prompt → Full prompt    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 11. Call GPT-4o (rag_engine.py)                            │
│     Prompt → GPT-4o → JSON response                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 12. Map to Response Model (main.py)                        │
│     Raw JSON → TaxSection object                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 13. Return JSON Response                                    │
│     {"tax_considerations": {...}, ...}                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Concepts Explained

### 1. Embeddings (Vector Representations)

**What are embeddings?**
- Numbers that represent the "meaning" of text
- Similar texts have similar embeddings
- 1536 numbers for `text-embedding-3-small`

**Example:**
- Document: "WBSO tax credit 32%"
- Embedding: `[0.123, -0.456, 0.789, ..., 0.234]`
- Query: "R&D tax credit rates"
- Embedding: `[0.125, -0.458, 0.791, ..., 0.236]` (very similar!)

### 2. Cosine Similarity

**How Qdrant finds matches:**
- Calculates angle between two vectors
- Closer vectors = higher similarity score (0.0 to 1.0)
- Score 0.89 = 89% similar (very good match!)

### 3. Cross-Lingual Retrieval

**Why English queries find Dutch documents:**
- Embeddings capture **semantic meaning**, not just words
- "WBSO" in Dutch and "R&D tax credit" in English have similar meanings
- Embeddings bridge the language gap

### 4. RAG (Retrieval-Augmented Generation)

**Why RAG?**
- **Without RAG**: GPT-4o uses only training data (may be outdated)
- **With RAG**: GPT-4o uses your specific documents (up-to-date, accurate)
- Combines retrieval (find relevant docs) + generation (create memo)

---

## Code Files Summary

| File | Purpose | Key Functions |
|------|---------|---------------|
| `ingest_data.py` | Document ingestion | Load → Split → Embed → Store |
| `app/services/qdrant.py` | Vector search | Query → Embed → Search → Format |
| `app/services/rag_engine.py` | RAG generation | Retrieve → Prompt → Generate |
| `app/core/orchestrator.py` | Task planning | Analyze input → Create tasks |
| `app/main.py` | API endpoint | Validate → Orchestrate → Map → Return |

---

## Example: Complete Trace

**Input Document:**
```
File: wbso_2025.txt
Content: "De WBSO... Voor 2025 zijn de tarieven als volgt: Eerste schijf (tot €350.000 S&O-loon): 32%..."
```

**User Request:**
```json
{
  "company_name": "TechStart Inc",
  "industry": "Software & Technology"
}
```

**What Happens:**
1. ✅ Orchestrator detects `industry == "Software & Technology"`
2. ✅ Creates task: "WBSO and Innovation Box Tax Credits Research"
3. ✅ Query: "Netherlands WBSO R&D tax credit Innovation Box..."
4. ✅ Query → Embedding: `[0.234, -0.567, ...]`
5. ✅ Search Qdrant → Finds `wbso_2025.txt` chunk (score: 0.89)
6. ✅ Format context: "Context 1 (Source: wbso_2025.txt): De WBSO..."
7. ✅ GPT-4o reads context, extracts WBSO rates
8. ✅ Generates: `{"tax_optimization_strategies": ["Apply for WBSO: 32% first bracket..."]}`
9. ✅ Maps to `TaxSection` object
10. ✅ Returns JSON response

**Result:**
User gets accurate WBSO tax credit information extracted from the Dutch document, even though they queried in English!

---

This is how the entire system works: **Documents → Embeddings → Storage → Retrieval → Generation → Response**

