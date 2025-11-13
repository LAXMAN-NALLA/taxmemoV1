# Quick Test Examples

Copy and paste these JSON requests into Swagger UI at `http://localhost:8000/docs` or use them with your API client.

---

## 1. Tech Startup - R&D Focus

```json
{
  "companyName": "SaaS Innovators Inc.",
  "industry": "Software & Technology",
  "employeeCount": 5,
  "entryGoals": ["Establish physical presence", "Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "taxConsiderations": ["Corporate income tax implications", "R&D tax credits"],
  "additionalContext": "We develop our own IP and want to know about R&D incentives like WBSO and Innovation Box."
}
```

**Expected:** Should return sections with WBSO tax credit details and Innovation Box information.

---

## 2. E-commerce Company

```json
{
  "companyName": "Global Marketplace Ltd",
  "industry": "E-commerce & Retail",
  "employeeCount": 25,
  "entryGoals": ["Establish physical presence", "Hire employees", "Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 5000000,
  "projectedRevenue": 8000000,
  "taxConsiderations": ["VAT obligations", "Digital services tax"],
  "additionalContext": "We operate an online marketplace and need to understand GDPR compliance and VAT registration requirements."
}
```

**Expected:** Should include GDPR information, VAT obligations, and e-commerce specific regulations.

---

## 3. Holding Company

```json
{
  "companyName": "European Holdings BV",
  "industry": "Financial Services",
  "companyType": "Holding Company",
  "employeeCount": 3,
  "entryGoals": ["Tax optimization", "Establish physical presence"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 10000000,
  "taxConsiderations": ["Participation exemption", "Holding company benefits", "Tax treaties"],
  "additionalContext": "We want to understand the participation exemption (deelnemingsvrijstelling) and how it applies to our holding structure."
}
```

**Expected:** Should include participation exemption details and holding company benefits.

---

## 4. Manufacturing Company

```json
{
  "companyName": "Advanced Manufacturing Corp",
  "industry": "Manufacturing",
  "employeeCount": 50,
  "entryGoals": ["Establish physical presence", "Hire employees", "Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 15000000,
  "plannedEmployees": 75,
  "preferredStructure": "BV",
  "taxConsiderations": ["Corporate income tax", "Employment tax", "VAT"],
  "additionalContext": "We're setting up a manufacturing facility and need to understand employment law, payroll taxes, and corporate structure options."
}
```

**Expected:** Should include employment law, payroll tax information, and BV setup details.

---

## 5. Consulting Firm (Minimal)

```json
{
  "companyName": "Strategic Consulting Group",
  "industry": "Professional Services",
  "employeeCount": 15,
  "entryGoals": ["Establish physical presence", "Hire employees"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 3000000,
  "preferredStructure": "Branch Office",
  "additionalContext": "We provide consulting services and want the fastest way to establish presence."
}
```

**Expected:** Should recommend Branch Office and provide setup timeline.

---

## 6. Biotech Startup

```json
{
  "companyName": "BioTech Innovations BV",
  "industry": "Biotechnology",
  "employeeCount": 12,
  "entryGoals": ["Tax optimization", "Establish physical presence"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 2000000,
  "taxConsiderations": ["Innovation Box regime", "R&D tax credits", "IP tax benefits"],
  "additionalContext": "We have significant IP and want to maximize benefits from Innovation Box (9% tax rate) and WBSO R&D credits."
}
```

**Expected:** Should include detailed Innovation Box and WBSO information.

---

## 7. Small Business (Minimal Fields)

```json
{
  "companyName": "Local Services Co",
  "industry": "Small Business",
  "employeeCount": 2,
  "entryGoals": ["Establish physical presence"],
  "primaryJurisdiction": "Netherlands",
  "additionalContext": "We're a small business looking for the simplest way to establish presence."
}
```

**Expected:** Should provide simple, straightforward entry options.

---

## 8. FinTech Company

```json
{
  "companyName": "FinTech Solutions BV",
  "industry": "Financial Technology",
  "employeeCount": 30,
  "entryGoals": ["Establish physical presence", "Hire employees", "Compliance"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 8000000,
  "compliancePriorities": ["Financial regulations", "GDPR", "AML compliance"],
  "taxConsiderations": ["Corporate income tax", "Financial services tax"],
  "additionalContext": "We need to understand regulatory requirements for fintech companies, including AML, KYC, and financial services licensing."
}
```

**Expected:** Should include regulatory compliance information.

---

## 9. VC-Backed Startup

```json
{
  "companyName": "ScaleUp Ventures Inc",
  "industry": "Software & Technology",
  "employeeCount": 40,
  "entryGoals": ["Establish physical presence", "Hire employees", "Tax optimization"],
  "primaryJurisdiction": "Netherlands",
  "currentRevenue": 12000000,
  "projectedRevenue": 25000000,
  "fundingStatus": "VC-backed",
  "plannedEmployees": 100,
  "preferredStructure": "BV",
  "taxConsiderations": ["Corporate income tax", "Employee stock options", "R&D credits"],
  "additionalContext": "We're VC-backed and planning rapid growth. Need to understand employee stock option plans, R&D credits, and optimal corporate structure for scaling."
}
```

**Expected:** Should include growth-focused advice and R&D credits.

---

## 10. Minimal Test (Only Required Fields)

```json
{
  "companyName": "Test Company Ltd",
  "primaryJurisdiction": "Netherlands"
}
```

**Expected:** Should still generate basic memo sections.

---

## How to Use These Examples

### Option 1: Swagger UI (Easiest)
1. Start server: `uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click on `POST /generate-memo`
4. Click "Try it out"
5. Paste any JSON example above
6. Click "Execute"

### Option 2: cURL
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

### Option 3: Python Script
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-memo",
    json={
        "companyName": "SaaS Innovators Inc.",
        "industry": "Software & Technology",
        "employeeCount": 5,
        "entryGoals": ["Establish physical presence", "Tax optimization"],
        "primaryJurisdiction": "Netherlands",
        "taxConsiderations": ["Corporate income tax implications"],
        "additionalContext": "We develop our own IP and want to know about R&D incentives."
    }
)

print(response.json())
```

### Option 4: Run All Tests Automatically
```bash
cd backend
python test_scenarios.py
```

This will run all scenarios and provide a summary report.

---

## What to Look For

✅ **Success Indicators:**
- Response status: 200
- Non-null sections in response
- Relevant tax information (WBSO, Innovation Box, etc.)
- Actionable recommendations
- Implementation timelines

❌ **Common Issues:**
- 422 Error: Check field names (use camelCase or snake_case)
- 500 Error: Check server logs, verify Qdrant is running
- Empty sections: Check if documents were ingested properly
- Timeout: Normal for complex requests (30-120 seconds)

---

## Field Reference

**Required:**
- `companyName` (or `company_name`)

**Common Optional Fields:**
- `industry`: "Software & Technology", "E-commerce & Retail", etc.
- `employeeCount`: Number (e.g., 5, 25, 50)
- `entryGoals`: Array of strings
- `taxConsiderations`: Array of strings
- `additionalContext`: String with specific questions/concerns

**See `API_DOCUMENTATION.md` for complete field list.**

