# Test Scenarios for Tax Memo Generator V1

## 🎯 Purpose
This document provides specific test cases to verify the system works correctly.

---

## ✅ Test Scenario 1: Software Company (Speed Priority)

**Purpose:** Verify speed preference works for generic company types

**Input:**
```json
{
  "companyName": "Tech Startup Inc",
  "industry": "Software & Technology",
  "companyType": "LLC",
  "employeeCount": 15,
  "entryGoals": ["Hire employees", "Establish physical presence"],
  "primaryJurisdiction": "Netherlands",
  "timelinePreference": "ASAP (within 1 month)"
}
```

**Expected Output:**
- ✅ Recommends **Branch Office** (speed preference wins)
- ✅ Includes **WBSO** and **Innovation Box** in specialRegimes
- ✅ Timeline mentions **"no notary"** or doesn't mention notary
- ✅ NO Participation Exemption

**Why:** Generic "LLC" doesn't force BV, so speed preference wins.

---

## ✅ Test Scenario 2: Company with "B.V." in Name

**Purpose:** Verify name constraint forces BV even with urgent timeline

**Input:**
```json
{
  "companyName": "Dutch Solutions B.V.",
  "industry": "E-commerce & Retail",
  "companyType": "Corporation",
  "entryGoals": ["Sell products/services"],
  "primaryJurisdiction": "Netherlands",
  "timelinePreference": "ASAP (within 1 month)"
}
```

**Expected Output:**
- ✅ Recommends **BV** (name constraint wins over speed)
- ✅ Timeline mentions **notary** (BV requires notary)
- ✅ Explains fast-track BV setup but still recommends BV
- ✅ NO Branch Office recommendation

**Why:** "B.V." in name = explicit Dutch entity intent, forces BV.

---

## ✅ Test Scenario 3: Holding Company

**Purpose:** Verify holding company isolation (no R&D credits, no Branch)

**Input:**
```json
{
  "companyName": "European Holdings Group",
  "industry": "Financial Services",
  "companyType": "Holding Company",
  "entryGoals": ["Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "taxConsiderations": ["Participation exemption"]
}
```

**Expected Output:**
- ✅ Recommends **BV** (holding companies need BV)
- ✅ Includes **Participation Exemption** in specialRegimes
- ✅ NO Innovation Box
- ✅ NO WBSO
- ✅ NO Branch Office recommendation

**Why:** Holding companies are isolated path - only holding-specific advice.

---

## ✅ Test Scenario 4: Tech Company (No Urgency)

**Purpose:** Verify default comparison path works

**Input:**
```json
{
  "companyName": "SaaS Innovations",
  "industry": "Software & Technology",
  "companyType": "Corporation",
  "entryGoals": ["Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "timelinePreference": "Medium-term (3-6 months)"
}
```

**Expected Output:**
- ✅ Provides **BV vs Branch comparison**
- ✅ Includes **WBSO** and **Innovation Box**
- ✅ NO Participation Exemption

**Why:** No urgency, no name constraint → default comparison path.

---

## ✅ Test Scenario 5: Financial Services (No R&D Credits)

**Purpose:** Verify ghost R&D credits are prevented

**Input:**
```json
{
  "companyName": "Financial Advisors Ltd",
  "industry": "Financial Services",
  "companyType": "Corporation",
  "entryGoals": ["Tax optimization"],
  "primaryJurisdiction": "Netherlands"
}
```

**Expected Output:**
- ✅ NO Innovation Box
- ✅ NO WBSO
- ✅ General tax advice only

**Why:** Financial Services ≠ Tech, so no R&D credits.

---

## ✅ Test Scenario 6: E-commerce Company

**Purpose:** Verify transaction types work

**Input:**
```json
{
  "companyName": "Online Store",
  "industry": "E-commerce & Retail",
  "entryGoals": ["Sell products/services"],
  "primaryJurisdiction": "Netherlands",
  "taxConsiderations": ["VAT registration and compliance"],
  "transactionTypes": ["E-commerce", "Sale of goods"]
}
```

**Expected Output:**
- ✅ Focuses on **VAT obligations**
- ✅ Mentions **e-commerce** considerations
- ✅ Appropriate structure recommendation

**Why:** Transaction types influence recommendations.

---

## ❌ Failure Indicators

**If you see these, report them:**

1. **Contradictions:**
   - Recommends Branch Office but mentions notary
   - Recommends BV for holding but includes Innovation Box
   - Participation Exemption for non-holding companies

2. **Missing Information:**
   - Empty sections (all null)
   - Generic answers without specifics
   - Missing relevant tax regimes

3. **Wrong Recommendations:**
   - Branch Office for "B.V." named companies
   - Innovation Box for Financial Services
   - Branch Office for Holding Companies

---

## 📊 Test Results Template

For each test scenario, record:

```
Test Scenario: [Number]
Input: [Copy input JSON]
Expected: [What should happen]
Actual: [What actually happened]
Status: ✅ PASS / ❌ FAIL
Notes: [Any observations]
```

---

## 🎯 Success Criteria

**System passes if:**
- ✅ All 6 test scenarios produce expected outputs
- ✅ No contradictions in recommendations
- ✅ No irrelevant tax regimes
- ✅ Timeline matches recommended structure
- ✅ All sections are populated (not null)

**System fails if:**
- ❌ Any test scenario produces wrong recommendations
- ❌ Contradictory advice appears
- ❌ Ghost tax credits for wrong industries
- ❌ Name constraints ignored

---

## 📝 Reporting Issues

When reporting issues, include:
1. **Input JSON** (exact values used)
2. **Expected Output** (what should happen)
3. **Actual Output** (what actually happened)
4. **Screenshots** (if possible)
5. **Error Messages** (if any)

This helps identify if the issue is in:
- Orchestrator logic
- RAG retrieval
- LLM generation
- Response mapping

