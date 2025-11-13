# Deployment Architecture Explained

## 🏗️ How It Works

Your system has **2 separate applications** that communicate via HTTP:

1. **Backend (FastAPI)** - Runs on port 8000
   - Handles business logic
   - Connects to Qdrant
   - Calls OpenAI API
   - Provides REST API endpoints

2. **Frontend (Streamlit)** - Runs on port 8501
   - User interface
   - Collects form data
   - Sends HTTP requests to backend
   - Displays results

**They communicate like this:**
```
User → Streamlit UI → HTTP Request → FastAPI Backend → Response → Streamlit UI → User
```

---

## ✅ Deployment Options (3 Choices)

### Option 1: Both Separate (Recommended for Production)

**Backend:** Deploy to cloud (Heroku, Railway, Render, etc.)  
**Frontend:** Deploy to Streamlit Cloud

**Pros:**
- ✅ Most scalable
- ✅ Can update independently
- ✅ Professional setup
- ✅ Free tier available

**Cons:**
- ⚠️ Need to manage 2 deployments
- ⚠️ Need to configure API URL

**Steps:**
1. Deploy backend → Get URL (e.g., `https://your-api.railway.app`)
2. Deploy Streamlit → Set API URL in sidebar or code
3. Share Streamlit URL with tester

---

### Option 2: Backend Local + Frontend Cloud (Easiest for Testing)

**Backend:** Run on your computer  
**Frontend:** Deploy to Streamlit Cloud

**Pros:**
- ✅ Easiest to set up
- ✅ No backend deployment needed
- ✅ Free (Streamlit Cloud is free)

**Cons:**
- ⚠️ Backend must stay running on your computer
- ⚠️ Need ngrok or similar to expose backend publicly
- ⚠️ Not ideal for production

**Steps:**
1. Start backend locally: `uvicorn app.main:app --reload --port 8000`
2. Expose with ngrok: `ngrok http 8000` → Get public URL
3. Deploy Streamlit → User enters ngrok URL in sidebar
4. Share Streamlit URL

**Note:** If tester is on same network, can use your local IP instead of ngrok.

---

### Option 3: Both Local (For Development Only)

**Backend:** Run on your computer  
**Frontend:** Run on your computer

**Pros:**
- ✅ Fastest to test
- ✅ No deployment needed
- ✅ Good for development

**Cons:**
- ❌ Only accessible on your computer
- ❌ Can't share with remote testers
- ❌ Not for production

**Steps:**
1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `streamlit run streamlit_app.py`
3. Access at `http://localhost:8501`

---

## 🎯 Which Option Should You Choose?

### For CEO Testing (Recommended: Option 2)

**Why:**
- Quickest to set up
- No backend deployment complexity
- Streamlit Cloud is free and easy
- Tester just needs the Streamlit URL

**Setup:**
1. Run backend on your machine
2. Use ngrok to expose it (or share local IP if same network)
3. Deploy Streamlit to Streamlit Cloud
4. In Streamlit sidebar, user enters backend URL
5. Share Streamlit URL

---

### For Production (Recommended: Option 1)

**Why:**
- More reliable
- Backend runs 24/7
- Can handle multiple users
- Professional setup

**Setup:**
1. Deploy backend to Railway/Heroku/Render
2. Deploy Streamlit to Streamlit Cloud
3. Configure API URL in Streamlit code or sidebar
4. Share Streamlit URL

---

## 📋 Step-by-Step: Option 2 (Easiest for Testing)

### Step 1: Start Backend Locally
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Expose Backend (Choose One)

**Option A: ngrok (Easiest)**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
# Copy the https URL (e.g., https://abc123.ngrok.io)
```

**Option B: Local Network IP (If Same Network)**
```bash
# Find your IP
ipconfig  # Windows
# Use: http://YOUR_IP:8000
```

### Step 3: Deploy Streamlit
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Deploy `streamlit_app.py`
4. Get public URL

### Step 4: Configure
- Tester opens Streamlit URL
- Enters backend URL in sidebar (ngrok URL or your IP)
- Ready to test!

---

## 📋 Step-by-Step: Option 1 (Production)

### Step 1: Deploy Backend

**Railway (Easiest):**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select `backend` folder
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. Get deployment URL

**Heroku:**
```bash
cd backend
heroku create your-app-name
git push heroku main
```

### Step 2: Deploy Streamlit
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Update API URL in code (or use sidebar)

### Step 3: Configure API URL

**In `streamlit_app.py`, change:**
```python
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://your-backend-url.com",  # Change this
    help="Enter your backend API URL"
)
```

Or use environment variable:
```python
import os
API_URL = os.getenv("API_URL", "https://your-backend-url.com")
```

---

## 🔍 How Frontend Finds Backend

The Streamlit app has this code (line 26-30):
```python
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="http://localhost:8000",  # Default
    help="Enter your backend API URL"
)
```

**This means:**
- User can enter backend URL in sidebar
- Default is `localhost:8000` (for local testing)
- For production, change default or use environment variable

---

## ✅ Quick Decision Tree

**Q: Do you want to deploy backend to cloud?**
- **Yes** → Option 1 (Both Separate)
- **No** → Option 2 (Backend Local + Frontend Cloud)

**Q: Is tester on same network?**
- **Yes** → Use local IP, no ngrok needed
- **No** → Use ngrok to expose backend

**Q: Is this for production?**
- **Yes** → Option 1 (Both Separate)
- **No** → Option 2 (Easiest for testing)

---

## 🎯 Recommendation for Your Situation

**For CEO Testing:** Use **Option 2** (Backend Local + Frontend Cloud)

**Why:**
1. Fastest setup (5 minutes)
2. No backend deployment complexity
3. Streamlit Cloud is free
4. Easy to update

**Steps:**
1. Run backend locally
2. Use ngrok: `ngrok http 8000`
3. Deploy Streamlit to Streamlit Cloud
4. Share Streamlit URL
5. Tester enters ngrok URL in sidebar

---

## 📝 Summary

**Yes, you need to deploy them separately** because they are 2 different applications.

**But you have flexibility:**
- Both can be on cloud (production)
- Backend local + Frontend cloud (testing)
- Both local (development only)

**For your CEO testing, Option 2 is easiest!**

