# 🚀 Deploy Now - 3 Simple Steps

## Step 1: Deploy Backend (If Not Already Deployed)

### Quick Test - Is Your Backend Running?
```bash
# In backend folder
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or if already deployed:**
- Note your backend URL (e.g., `https://your-api.railway.app` or `http://localhost:8000`)

---

## Step 2: Deploy Streamlit UI

### Option A: Streamlit Cloud (Recommended - 2 Minutes)

1. **Push to GitHub:**
   ```bash
   git add streamlit_app.py requirements_streamlit.txt
   git commit -m "V1 ready for testing"
   git push
   ```

2. **Deploy:**
   - Go to: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Repository: Your repo
   - Main file: `streamlit_app.py`
   - Click "Deploy"

3. **Get Your Link:**
   - Streamlit gives you: `https://your-app.streamlit.app`
   - Copy this link

### Option B: Local Testing (For Internal Use)

```bash
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

---

## Step 3: Share with Tester

**Send them:**
1. Streamlit app URL
2. Backend API URL (if different from default)
3. `TEST_SCENARIOS.md` file
4. Brief instructions (see email template below)

---

## ✅ Quick Verification

Before sharing, test once:
1. Open Streamlit app
2. Fill out form with Test Scenario 1
3. Generate memo
4. Verify output looks correct

**If it works → Ready to share!**

---

## 📧 Email Template for Tester

```
Subject: Tax Memo Generator V1 - Ready for Testing

Hi [Name],

The Tax Memo Generator V1 is ready for testing.

🔗 Access Link: [Your Streamlit URL]

📋 Test Scenarios: See attached TEST_SCENARIOS.md

This is V1 with core features:
- Netherlands market entry focus
- 12 working input fields
- Smart task planning (no contradictions)
- All dropdown options work

Please test the 6 scenarios in TEST_SCENARIOS.md and report:
- Any contradictions in recommendations
- Missing information
- Wrong recommendations

Thanks!
```

---

## 🎯 That's It!

Once deployed, share the link and test scenarios. The system is ready for testing!

