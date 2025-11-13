# Quick Deployment Guide

## 🚀 Fastest Way to Deploy (5 Minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "V1 ready for testing"
git push origin main
```

### Step 2: Deploy Streamlit App
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `streamlit_app.py`
6. Click "Deploy"

### Step 3: Get Your Link
- Streamlit Cloud provides: `https://your-app-name.streamlit.app`
- Share this link with your tester

---

## ⚙️ Backend Deployment (If Needed)

### Option A: Keep Backend Local
- Run backend on your machine
- Use ngrok to expose it: `ngrok http 8000`
- Share ngrok URL with tester (for API URL in Streamlit)

### Option B: Deploy Backend to Cloud

**Heroku:**
```bash
cd backend
heroku create your-app-name
git push heroku main
```

**Railway:**
- Connect GitHub repo
- Select backend folder
- Add environment variables
- Deploy

---

## 📋 Pre-Deployment Checklist

- [ ] Backend running and accessible
- [ ] Qdrant collection has documents
- [ ] Environment variables set
- [ ] Tested locally with sample input
- [ ] Code pushed to GitHub

---

## 🔗 Share with Tester

**Send them:**
1. Streamlit app URL
2. Backend API URL (if separate from Streamlit)
3. `TEST_SCENARIOS.md` file
4. Brief note: "This is V1 - core features only. Test the 6 scenarios in TEST_SCENARIOS.md"

---

## ✅ That's It!

Once deployed, share the link and test scenarios. The system is ready!

