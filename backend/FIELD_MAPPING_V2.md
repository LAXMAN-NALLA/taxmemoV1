# Complete Field Mapping Guide - Your Request to API

## Your Request Fields → API Expected Fields

| Your Field | API Field | Status | Notes |
|------------|-----------|--------|-------|
| `businessName` | `company_name` | ✅ **REQUIRED** | Must be provided |
| `industry` | `industry` | ✅ Same | No change needed |
| `companySize` | `employee_count` | ⚠️ Convert | You have "Small (11-50 employees)" - use integer like `25` |
| `currentMarkets` | `target_markets` | ✅ Map | Array of strings |
| `entryGoals` | `entry_goals` | ✅ Map | Array of strings |
| `timeline` | `timeline_preference` | ✅ Map | String |
| `primaryJurisdiction` | `primary_jurisdiction` | ✅ Map | String |
| `secondaryJurisdictions` | ❌ Not used | - | Not in API model |
| `taxTreaties` | ❌ Not used | - | Not in API model |
| `businessStructure` | `preferred_structure` | ✅ Map | String (e.g., "BV", "Branch") |
| `companies` | ❌ Not used | - | Not in API model |
| `relationships` | ❌ Not used | - | Not in API model |
| `taxQueries` | `tax_considerations` | ✅ Map | Array of strings |
| `transactionTypes` | `current_operations` | ✅ Map | Array of strings |
| `specificConcerns` | `additional_context` | ✅ Map | String |
| `selectedLegalTopics` | `selected_legal_topics` | ✅ Map | Array of strings |
| `legalTopicData` | ❌ Not used | - | Not in API model |
| `targetMarkets` | `target_markets` | ✅ Map | Array of strings |
| `activities` | `current_operations` | ✅ Map | Array of strings (merge with transactionTypes) |
| `expectedRevenue` | `projected_revenue` | ✅ Map | Float (you have empty string "") |
| `entryOption` | ❌ Not used | - | Not in API model |
| `compliancePriorities` | `compliance_priorities` | ✅ Map | Array of strings |
| `memoName` | ❌ Not used | - | Not in API model |

## Your Original Request (WRONG - camelCase):
```json
{
  "businessName": "General Trading LLC",
  "industry": "E-commerce & Retail",
  "companySize": "Small (11-50 employees)",
  "currentMarkets": ["United States"],
  "entryGoals": ["Sell products/services", "Establish physical presence"],
  "timeline": "Medium-term (3-6 months)",
  "primaryJurisdiction": "Netherlands",
  "taxQueries": ["Corporate income tax implications", "Value-added tax (VAT) registration and compliance"],
  "transactionTypes": ["Sale of goods", "E-commerce"],
  "specificConcerns": "We need to know the exact 2025 corporate tax rates for a small business.",
  "businessStructure": "simple"
}
```

## Corrected Request (CORRECT - snake_case):
```json
{
  "company_name": "General Trading LLC",
  "industry": "E-commerce & Retail",
  "employee_count": 25,
  "target_markets": ["Netherlands"],
  "entry_goals": [
    "Sell products/services",
    "Establish physical presence"
  ],
  "timeline_preference": "Medium-term (3-6 months)",
  "primary_jurisdiction": "Netherlands",
  "preferred_structure": "BV",
  "tax_considerations": [
    "Corporate income tax implications",
    "Value-added tax (VAT) registration and compliance"
  ],
  "current_operations": [
    "Sale of goods",
    "E-commerce"
  ],
  "additional_context": "We need to know the exact 2025 corporate tax rates for a small business."
}
```

## Key Issues in Your Request:

1. **camelCase vs snake_case**: All field names must use snake_case (underscores)
2. **companySize**: You have a string "Small (11-50 employees)" but API expects integer `employee_count`
3. **Unused fields**: Many fields like `companies`, `relationships`, `memoName` are not in the API model
4. **Empty strings**: `expectedRevenue: ""` should be omitted or use a number

## All 23 API Fields (for reference):

### Required:
- `company_name` (string) - **MUST be provided**

### Optional:
- `industry`, `company_type`, `founding_year`, `headquarters_location`
- `primary_jurisdiction`, `target_markets`, `entry_goals`, `selected_legal_topics`
- `current_revenue`, `projected_revenue`, `budget_range`, `funding_status`
- `employee_count`, `planned_employees`, `current_operations`, `key_products_services`
- `timeline_preference`, `urgency_level`, `preferred_structure`
- `tax_considerations`, `compliance_priorities`, `additional_context`

