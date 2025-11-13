# 🚀 Simple Deployment Guide

## Quick Answer

**Yes, you deploy them separately** because they are 2 different applications.

But you have **3 options** - choose what's easiest for you:

---

## Option 1: Both on Cloud (Production) ⭐

```
Backend (FastAPI) → Railway/Heroku → https://api.example.com
Frontend (Streamlit) → Streamlit Cloud → https://app.streamlit.app
```

**Best for:** Production, multiple users, 24/7 availability

---

## Option 2: Backend Local + Frontend Cloud (Easiest for Testing) ⭐⭐⭐

```
Backend (FastAPI) → Your Computer → ngrok → https://abc.ngrok.io
Frontend (Streamlit) → Streamlit Cloud → https://app.streamlit.app
```

**Best for:** Quick testing, CEO demo, no backend deployment needed

**Steps:**
1. Run backend: `uvicorn app.main:app --reload`
2. Expose with ngrok: `ngrok http 8000`
3. Deploy Streamlit to Streamlit Cloud
4. Tester enters ngrok URL in Streamlit sidebar

---

## Option 3: Both Local (Development Only)

```
Backend (FastAPI) → Your Computer → localhost:8000
Frontend (Streamlit) → Your Computer → localhost:8501
```

**Best for:** Development, testing on your machine only

---

## 🎯 For Your CEO Testing: Choose Option 2

**Why?**
- ✅ Fastest (5 minutes)
- ✅ No backend deployment
- ✅ Free (Streamlit Cloud)
- ✅ Easy to update

**What to do:**
1. Start backend on your computer
2. Run `ngrok http 8000` (get public URL)
3. Deploy Streamlit to Streamlit Cloud
4. Share Streamlit URL
5. Tester enters ngrok URL in sidebar

---

## 📋 Quick Checklist

**Option 2 (Recommended for Testing):**
- [ ] Backend running locally
- [ ] ngrok installed and running
- [ ] Streamlit deployed to Streamlit Cloud
- [ ] Share Streamlit URL with tester
- [ ] Tester enters ngrok URL in sidebar

**Option 1 (Production):**
- [ ] Backend deployed to Railway/Heroku
- [ ] Streamlit deployed to Streamlit Cloud
- [ ] API URL configured in Streamlit
- [ ] Share Streamlit URL

---

## 💡 How They Connect

The Streamlit app has a sidebar where users can enter the backend URL:

```python
API_URL = st.sidebar.text_input("Backend API URL", value="http://localhost:8000")
```

So:
- **Local testing:** Use `http://localhost:8000`
- **With ngrok:** Use `https://abc123.ngrok.io`
- **Production:** Use `https://your-api.railway.app`

---

## ✅ That's It!

**For CEO testing:** Use Option 2 (Backend Local + Frontend Cloud)

See `DEPLOYMENT_ARCHITECTURE.md` for detailed steps.

