# Why Certain Fields Are Not in the API

## The Original Specification

The API was built according to the original requirements which specified **exactly 23 fields** for the request model. The fields you're asking about were **not part of the original specification**.

## Fields Not Included (and Why)

### 1. `companies` (Array of Company Objects)
**Why not included:**
- Original spec focused on **single company** market entry
- V1 is designed for one company entering Netherlands
- Multi-entity scenarios weren't in scope

**Should we add it?** 
- ✅ **YES** - Useful for multi-entity structures (parent/subsidiary relationships)
- Would enable analysis of corporate group structures

### 2. `relationships` (Array)
**Why not included:**
- Not specified in original 23-field requirement
- Focus was on single company entry

**Should we add it?**
- ✅ **YES** - Useful for tracking inter-company relationships, ownership structures

### 3. `secondaryJurisdictions` (Array)
**Why not included:**
- Original spec had `primary_jurisdiction` only
- V1 hardcoded to Netherlands only

**Should we add it?**
- ✅ **YES** - Useful for multi-country expansion scenarios
- Would enable cross-border tax analysis

### 4. `taxTreaties` (Array)
**Why not included:**
- Not in original 23-field spec
- Treaty analysis would be inferred from jurisdiction data

**Should we add it?**
- ⚠️ **MAYBE** - Could be useful for explicit treaty selection
- Currently handled via `primary_jurisdiction` and `target_markets`

### 5. `legalTopicData` (Object)
**Why not included:**
- Original spec had `selected_legal_topics` (array of strings)
- Detailed legal data wasn't part of input model

**Should we add it?**
- ⚠️ **MAYBE** - Could store structured legal topic data
- Currently handled via `additional_context` or `selected_legal_topics`

### 6. `entryOption` (String)
**Why not included:**
- Original spec had `preferred_structure` (BV, Branch, etc.)
- Entry option is similar to preferred structure

**Should we add it?**
- ❌ **NO** - Redundant with `preferred_structure`
- Use `preferred_structure` instead

### 7. `memoName` (String)
**Why not included:**
- Not in original specification
- Memo naming is a UI/client concern, not API concern

**Should we add it?**
- ❌ **NO** - This is metadata for your frontend/client
- Store this on your side, not in the API request

## Summary

| Field | Should Add? | Reason |
|-------|-------------|--------|
| `companies` | ✅ **YES** | Multi-entity support |
| `relationships` | ✅ **YES** | Corporate structures |
| `secondaryJurisdictions` | ✅ **YES** | Multi-country expansion |
| `taxTreaties` | ⚠️ **MAYBE** | Could be useful |
| `legalTopicData` | ⚠️ **MAYBE** | Structured legal data |
| `entryOption` | ❌ **NO** | Use `preferred_structure` |
| `memoName` | ❌ **NO** | Client-side metadata |

## Current Workaround

For now, you can:
- Put company details in `additional_context`
- Use `target_markets` for multiple jurisdictions
- Use `preferred_structure` instead of `entryOption`
- Store `memoName` on your client side

## Next Steps

If you need these fields, I can:
1. **Extend the request model** to include them
2. **Update the orchestrator** to use them in task planning
3. **Update the RAG engine** to incorporate them in context

Would you like me to add these fields to the API?

