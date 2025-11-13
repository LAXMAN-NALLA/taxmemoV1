# Field Name Mapping Guide

## Your Input → API Expected Field Names

| Your Field Name | API Expected Field | Notes |
|----------------|-------------------|-------|
| `businessName` | `company_name` | **REQUIRED** - Name of the company |
| `industry` | `industry` | ✅ Same - Industry sector |
| `companySize` | `employee_count` | Use integer number, or `planned_employees` |
| `currentMarkets` | `target_markets` | Array of target market strings |
| `entryGoals` | `entry_goals` | Array of entry goal strings |
| `timeline` | `timeline_preference` | Timeline preference string |
| `primaryJurisdiction` | `primary_jurisdiction` | Primary jurisdiction (defaults to Netherlands) |
| `taxQueries` | `tax_considerations` | Array of tax consideration strings |
| `memoName` | ❌ Not used | This field doesn't exist in the API |

## Your Original Request (WRONG):
```json
{
  "businessName": "Simple Trading LLC",
  "industry": "E-commerce & Retail",
  "companySize": "Small (11-50 employees)",
  "currentMarkets": ["United States"],
  "entryGoals": ["Sell products/services", "Establish physical presence"],
  "timeline": "Medium-term (3-6 months)",
  "primaryJurisdiction": "Netherlands",
  "taxQueries": [
    "Corporate income tax implications",
    "Value-added tax (VAT) registration and compliance"
  ],
  "memoName": "Baseline Test - NL Entry"
}
```

## Corrected Request (CORRECT):
```json
{
  "company_name": "Simple Trading LLC",
  "industry": "E-commerce & Retail",
  "entry_goals": [
    "Sell products/services",
    "Establish physical presence"
  ],
  "timeline_preference": "Medium-term (3-6 months)",
  "primary_jurisdiction": "Netherlands",
  "tax_considerations": [
    "Corporate income tax implications",
    "Value-added tax (VAT) registration and compliance"
  ]
}
```

## All Available Fields (23 total)

### Required:
- `company_name` (string) - **MUST be provided**

### Optional (22 fields):
- `industry` (string)
- `company_type` (string)
- `founding_year` (integer)
- `headquarters_location` (string)
- `primary_jurisdiction` (string)
- `target_markets` (array of strings)
- `entry_goals` (array of strings)
- `selected_legal_topics` (array of strings)
- `current_revenue` (float)
- `projected_revenue` (float)
- `budget_range` (string)
- `funding_status` (string)
- `employee_count` (integer)
- `planned_employees` (integer)
- `current_operations` (array of strings)
- `key_products_services` (array of strings)
- `timeline_preference` (string)
- `urgency_level` (string)
- `preferred_structure` (string)
- `tax_considerations` (array of strings)
- `compliance_priorities` (array of strings)
- `additional_context` (string)

