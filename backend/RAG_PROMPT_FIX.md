# RAG Prompt Fix: "Stay in Your Lane" Constraints

## 🎯 The Problem

Even though the Orchestrator was creating the correct tasks, the LLM was still overriding them with user context preferences.

**Example:**
- Task: "Research BV structure"
- User Context: "Urgent timeline"
- LLM Thought: "User wants speed → Recommend Branch Office"
- **Result:** Wrong recommendation despite correct task

## ✅ The Solution

Added **task-specific constraints** to the RAG prompt that tell the LLM: **"The task is the source of truth, not user preferences."**

---

## 🔧 What Was Changed

### 1. Added Task Name Parameter
- `generate_section()` now accepts `task_name` parameter
- Task name is passed from `TaskPlan` to the RAG engine

### 2. Created `_build_task_constraints()` Method
This method analyzes the task and adds specific constraints:

**For BV Tasks:**
```
- You MUST recommend a BV structure
- Do NOT recommend Branch Office, even if user mentions urgency
- If user mentions 'urgent', explain fast-track BV setup, but still recommend BV
```

**For Branch Office Tasks:**
```
- You MUST recommend Branch Office
- Do NOT mention notary requirements
- Focus on speed and simplicity
```

**For Holding Company Tasks:**
```
- You MUST recommend BV (required for participation exemption)
- Do NOT recommend Branch Office
- Do NOT include Innovation Box or WBSO
```

**For Tech/R&D Tasks:**
```
- Only include WBSO/Innovation Box for Software & Technology
- Do NOT include for Financial Services or Holdings
```

### 3. Added to Prompt
The constraints are inserted **right after** the task description and **before** the context, ensuring the LLM sees them first.

---

## 📝 How It Works

### Before (The Problem):
```
Prompt:
"User wants urgent entry. Here is info about BVs. Write recommendation."

LLM thinks: "Urgent = Branch Office" → Recommends Branch
```

### After (The Fix):
```
Prompt:
"CRITICAL RULE: Your task is 'Research BV Structure'
- You MUST recommend BV
- Do NOT recommend Branch Office, even if user mentions urgency
- If user mentions 'urgent', explain fast-track BV setup, but still recommend BV

User wants urgent entry. Here is info about BVs. Write recommendation."

LLM thinks: "Task says BV → Must recommend BV" → Recommends BV (with fast-track option)
```

---

## 🧪 Expected Results

### Test 1: "Speedy Traders B.V."
**Before:** Recommended Branch Office (wrong)  
**After:** ✅ Recommends BV (explains fast-track setup, but still BV)

### Test 2: "Global Assets Group" (Holding)
**Before:** Recommended Branch Office + Innovation Box (wrong)  
**After:** ✅ Recommends BV only, Participation Exemption only

### Test 3: "SaaS Startups Inc" (Tech)
**Before:** ✅ Already working  
**After:** ✅ Still working (no change needed)

---

## 🔍 Key Features

1. **Task-Specific Rules:** Different constraints for BV, Branch, Holding, Tech tasks
2. **Explicit Instructions:** "MUST recommend X" and "Do NOT recommend Y"
3. **Context Priority:** Task > User Context (when they conflict)
4. **Personalization Allowed:** User context can personalize (e.g., "fast-track BV") but not change structure

---

## 📊 Constraint Detection Logic

The system automatically detects task type from:
- Task name (e.g., "BV Incorporation Process")
- Search query (e.g., "Netherlands BV incorporation...")

Then applies the appropriate constraints:
- `"bv"` in task/query → BV constraints
- `"branch"` in task/query → Branch constraints
- `"holding"` in task/query → Holding constraints
- `"wbso"` or `"innovation box"` in task/query → Tech constraints

---

## ✅ Summary

**The Fix:**
- Added task-specific constraints to RAG prompts
- LLM now follows task instructions, not user preferences
- Prevents "thinking" that overrides the orchestrator's plan

**Result:**
- ✅ BV tasks → Always recommend BV
- ✅ Branch tasks → Always recommend Branch
- ✅ Holding tasks → Always recommend BV + Participation Exemption
- ✅ No more context bleed-over

This fix works **together** with the orchestrator logic to ensure end-to-end correctness.

