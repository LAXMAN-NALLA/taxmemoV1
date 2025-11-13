# Orchestrator Improvements - V1.1

## 🎯 Overview

The orchestrator has been upgraded with **strict conditional logic** to prevent hallucinations and context bleed-over. This ensures accurate, relevant recommendations based on company profile.

---

## 🐛 Problems Fixed

### 1. ✅ The "B.V." Name Trap
**Problem:** System recommended Branch Office for companies named "Dutch Food Solutions B.V."

**Fix:** 
- Detects "B.V.", "BV", or "B.V." in company name
- Forces BV structure path (Path 2A)
- Skips Branch Office recommendations

**Detection Logic:**
```python
must_be_bv = (
    "b.v" in company_name or 
    "bv" in company_name or 
    "b.v." in company_name or
    "llc" in company_type or
    "corporation" in company_type or
    is_holding
)
```

---

### 2. ✅ The "Holding" Conflict
**Problem:** Holding companies received irrelevant recommendations (Branch Office, Innovation Box)

**Fix:**
- Strict isolation: Holding companies enter Path 1 (isolated block)
- NO Innovation Box or WBSO tasks
- NO Branch Office tasks
- ONLY: Participation Exemption, BV structure, Holding compliance

**Detection Logic:**
```python
is_holding = (
    "holding" in company_type or 
    "holding" in company_name or
    "participation exemption" in all_tax_text or
    "deelnemingsvrijstelling" in all_tax_text or
    "dividend" in all_tax_text and "holding" in all_tax_text
)
```

---

### 3. ✅ The "Notary" Hallucination
**Problem:** Branch Office timeline incorrectly mentioned notary requirements

**Fix:**
- Branch Office queries explicitly include "no notary required"
- Forces RAG to retrieve documents confirming no notary needed

**Query Example:**
```
"Netherlands Branch Office registration Chamber of Commerce KvK no notary required timeline fast setup 2025"
```

---

### 4. ✅ The "Ghost" Tax Credits
**Problem:** Financial Services companies received Innovation Box recommendations

**Fix:**
- Tech detection explicitly excludes Financial Services
- Innovation Box/WBSO tasks ONLY for Tech industries
- Prevents R&D credit recommendations for non-R&D companies

**Detection Logic:**
```python
is_tech = (
    ("software" in industry or "technology" in industry) and
    "financial services" not in industry
) or (
    "biotech" in industry or 
    "engineering" in industry or
    "r&d" in goals
)
```

---

## 🏗️ Architecture: Mutually Exclusive Paths

### Path 1: Holding Company (Strict Isolation)
```
IF is_holding:
    ✅ Executive Summary (Holding-specific)
    ✅ Participation Exemption Deep Dive
    ✅ BV Structure (forced)
    ✅ Corporate Tax (Holding-specific)
    ✅ Compliance (Holding-specific)
    ❌ NO Innovation Box
    ❌ NO WBSO
    ❌ NO Branch Office
```

### Path 2: Operating Company (Sub-paths)

#### Path 2A: Force BV
```
IF must_be_bv (name contains "B.V."):
    ✅ BV Executive Summary
    ✅ BV Incorporation Process
    ✅ BV Tax and Compliance
    ✅ BV Implementation Timeline
    ❌ NO Branch Office
```

#### Path 2B: Speed/Branch
```
IF prioritizes_speed AND NOT must_be_bv:
    ✅ Branch Office Executive Summary
    ✅ Branch Registration (NO NOTARY - explicit in query)
    ✅ Branch Tax and Compliance
    ✅ Branch Implementation Timeline
```

#### Path 2C: Default Comparison
```
ELSE (unclear preference):
    ✅ Market Entry Comparison (BV vs Branch)
    ✅ Executive Summary
    ✅ Tax Overview
    ✅ Implementation Timeline
```

### Conditional Add-ons (Operating Path Only)

#### Tech Incentives (Path 2 only)
```
IF is_tech (and NOT Financial Services):
    ✅ R&D Incentives (WBSO & Innovation Box)
```

#### Employment (All paths)
```
IF "hire" in goals or "employees" in goals:
    ✅ 30% Ruling & Payroll
```

---

## 📊 Decision Tree

```
User Input
    ↓
┌─────────────────────────────────┐
│ 1. Analyze & Classify           │
│    - is_holding?                │
│    - must_be_bv?                │
│    - is_tech?                    │
│    - prioritizes_speed?          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ 2. Select Path                  │
│    IF is_holding → Path 1       │
│    ELSE → Path 2                 │
│      IF must_be_bv → 2A         │
│      ELIF speed → 2B             │
│      ELSE → 2C                   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ 3. Add Conditionals             │
│    IF is_tech → Add R&D task    │
│    IF hiring → Add employment   │
└─────────────────────────────────┘
    ↓
Return Task List (sorted by priority)
```

---

## 🧪 Test Cases

### Test Case 1: "B.V." Name Trap
**Input:**
```json
{
  "companyName": "Dutch Food Solutions B.V.",
  "industry": "E-commerce & Retail",
  "entryGoals": ["Sell products/services"]
}
```

**Expected:**
- ✅ Path 2A (Force BV)
- ✅ BV tasks only
- ❌ NO Branch Office tasks

---

### Test Case 2: Holding Company
**Input:**
```json
{
  "companyName": "European Holdings BV",
  "companyType": "Holding Company",
  "taxConsiderations": ["Participation exemption"]
}
```

**Expected:**
- ✅ Path 1 (Holding isolation)
- ✅ Participation Exemption tasks
- ✅ BV structure tasks
- ❌ NO Innovation Box
- ❌ NO WBSO
- ❌ NO Branch Office

---

### Test Case 3: Financial Services (Ghost Credits)
**Input:**
```json
{
  "companyName": "Financial Services Corp",
  "industry": "Financial Services",
  "entryGoals": ["Tax optimization"]
}
```

**Expected:**
- ✅ Path 2C (Default)
- ✅ General tax tasks
- ❌ NO Innovation Box
- ❌ NO WBSO

---

### Test Case 4: Tech Company (R&D Credits)
**Input:**
```json
{
  "companyName": "Tech Startup Inc",
  "industry": "Software & Technology",
  "entryGoals": ["Tax optimization"]
}
```

**Expected:**
- ✅ Path 2C (Default)
- ✅ Innovation Box task
- ✅ WBSO task

---

### Test Case 5: Speed Preference
**Input:**
```json
{
  "companyName": "Quick Entry Corp",
  "timelinePreference": "Short-term (1-3 months)",
  "entryGoals": ["Establish physical presence"]
}
```

**Expected:**
- ✅ Path 2B (Speed/Branch)
- ✅ Branch Office tasks
- ✅ "No notary" in queries

---

## 🔍 Key Improvements

### 1. Strict Isolation
- Holding companies cannot access operating company tasks
- Prevents context bleed-over

### 2. Name-Based Detection
- Company name analysis prevents incorrect recommendations
- "B.V." in name = forced BV path

### 3. Industry-Specific Logic
- Tech detection excludes Financial Services
- Prevents ghost R&D credits

### 4. Explicit Query Design
- Branch Office queries include "no notary"
- Forces correct document retrieval

### 5. Priority System
- Tasks sorted by priority
- Ensures logical flow

---

## 📝 Code Structure

### TaskPlan Class
```python
class TaskPlan:
    task_name: str
    search_query: str
    section_name: str
    priority: int  # NEW: Priority for sorting
```

### Detection Functions
- `is_holding`: Detects holding company intent
- `must_be_bv`: Detects BV requirement
- `is_tech`: Detects tech/R&D intent (excludes Financial)
- `prioritizes_speed`: Detects speed preference

### Path Selection
- Path 1: Holding (strict isolation)
- Path 2A: Force BV
- Path 2B: Speed/Branch
- Path 2C: Default comparison

---

## ✅ Verification Checklist

- [x] "B.V." in name → Forces BV path
- [x] Holding company → Isolated path, no R&D/Branch
- [x] Branch Office → Explicit "no notary" in queries
- [x] Financial Services → No Innovation Box/WBSO
- [x] Tech industry → Innovation Box/WBSO included
- [x] Speed preference → Branch Office path
- [x] Mutually exclusive paths → No context bleed

---

## 🚀 Result

The orchestrator now provides:
- ✅ Accurate entity recommendations
- ✅ No conflicting information
- ✅ Industry-appropriate tax credits
- ✅ Correct timeline information
- ✅ Context isolation

**No more hallucinations. No more context bleed-over.**

