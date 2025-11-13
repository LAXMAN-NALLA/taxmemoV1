# Deployment Checklist: Tax Memo Generator V1

## ✅ Pre-Deployment Checklist

### 1. Backend Setup
- [ ] Backend server is running and accessible
- [ ] Environment variables configured (`.env` file):
  - [ ] `OPENAI_API_KEY` is set
  - [ ] `QDRANT_URL` is set
  - [ ] `QDRANT_API_KEY` is set
- [ ] Qdrant collection `netherlands_pilot` exists and has documents
- [ ] API is accessible at the deployment URL
- [ ] Health check endpoint works: `GET /health`

### 2. Streamlit UI Setup
- [ ] Streamlit app is ready (`streamlit_app.py`)
- [ ] Dependencies installed (`requirements_streamlit.txt`)
- [ ] API URL configured (default: `http://localhost:8000`)

### 3. Code Verification
- [ ] Orchestrator logic updated (mutually exclusive paths)
- [ ] RAG engine has task constraints
- [ ] All fixes applied:
  - [ ] Early return for holding companies
  - [ ] `must_be_bv` check before `prioritizes_speed`
  - [ ] Generic foreign terms removed from `must_be_bv`
  - [ ] Task-specific constraints in prompts

### 4. Testing
- [ ] Tested locally with sample inputs
- [ ] Verified holding company path works
- [ ] Verified BV name constraint works
- [ ] Verified speed preference works for generic terms

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Easiest)

**Steps:**
1. Push code to GitHub repository
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select repository and branch
6. Main file: `streamlit_app.py`
7. Click "Deploy"

**Configuration:**
- No environment variables needed (user enters API URL in sidebar)
- Free tier available
- Automatic updates on git push

**Share Link:**
- Streamlit Cloud provides a public URL
- Share this URL with your tester

---

### Option 2: Local Deployment (For Internal Testing)

**Steps:**
1. Start backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start Streamlit app:
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

3. Access at: `http://localhost:8501`

**For Remote Access:**
- Use ngrok or similar tool to expose local server
- Or deploy backend to cloud (Heroku, Railway, etc.)

---

### Option 3: Full Cloud Deployment

**Backend (FastAPI):**
- Deploy to: Heroku, Railway, Render, or AWS
- Set environment variables in platform
- Get backend URL

**Frontend (Streamlit):**
- Deploy to: Streamlit Cloud
- Configure API URL in sidebar or as environment variable

---

## 📋 Testing Guide for Tester

### Quick Start
1. Open the Streamlit app URL
2. Enter backend API URL (if not default)
3. Fill out the form (5 steps)
4. Click "Generate Memo"
5. Review the output

### Test Scenarios

#### Scenario 1: Software Company (Speed Priority)
**Input:**
- Name: "Tech Startup Inc"
- Industry: Software & Technology
- Type: LLC
- Timeline: ASAP (within 1 month)
- Goals: Hire employees

**Expected:**
- ✅ Recommends Branch Office
- ✅ Includes WBSO and Innovation Box
- ✅ No notary in timeline

---

#### Scenario 2: Company with "B.V." in Name
**Input:**
- Name: "Dutch Solutions B.V."
- Industry: E-commerce & Retail
- Timeline: ASAP

**Expected:**
- ✅ Recommends BV (name constraint wins)
- ✅ Mentions notary in timeline

---

#### Scenario 3: Holding Company
**Input:**
- Name: "European Holdings"
- Industry: Financial Services
- Type: Holding Company
- Tax Considerations: Participation exemption

**Expected:**
- ✅ Recommends BV
- ✅ Includes Participation Exemption
- ✅ NO Innovation Box or WBSO
- ✅ NO Branch Office recommendation

---

#### Scenario 4: Tech Company (No Urgency)
**Input:**
- Name: "SaaS Corp"
- Industry: Software & Technology
- Type: Corporation
- Timeline: Medium-term (3-6 months)

**Expected:**
- ✅ Recommends BV vs Branch comparison
- ✅ Includes WBSO and Innovation Box

---

## 🔍 What to Check

### Output Quality
- [ ] Recommendations match company type
- [ ] No contradictory advice (e.g., Branch + Participation Exemption)
- [ ] Timeline matches recommended structure
- [ ] Special regimes are relevant to industry

### Edge Cases
- [ ] "B.V." in name → Forces BV
- [ ] Holding company → Only holding-specific advice
- [ ] Financial Services → No R&D credits
- [ ] Software & Technology → Includes R&D credits

### UI/UX
- [ ] All steps work correctly
- [ ] Form data persists between steps
- [ ] Memo displays properly
- [ ] Download JSON works

---

## 🐛 Troubleshooting

### Issue: "Could not connect to API"
**Solution:**
- Check backend server is running
- Verify API URL in Streamlit sidebar
- Check firewall/network settings

### Issue: "Empty memo response"
**Solution:**
- Check backend logs for errors
- Verify Qdrant connection
- Check OpenAI API key

### Issue: "Wrong recommendations"
**Solution:**
- Check orchestrator logs (detection values)
- Verify task list is correct
- Check RAG prompt constraints

---

## 📧 Information to Share with Tester

**Share these files:**
1. Streamlit app URL (or deployment instructions)
2. Backend API URL (if separate)
3. `TEST_SCENARIOS.md` (test cases)
4. `CEO_SIMPLE_SUMMARY.md` (what works in V1)

**Tell them:**
- This is V1 - core features only
- Additional fields coming in V2
- Focus on Netherlands market entry
- All dropdown options work
- Report any contradictions or errors

---

## ✅ Ready for Testing

Once all checkboxes are complete, the system is ready for deployment and testing!

