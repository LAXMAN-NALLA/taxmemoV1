# Quick Deployment Steps: Render + Streamlit

## 🎯 Your Setup
- **Backend:** Render.com
- **Frontend:** Streamlit Cloud

---

## Part 1: Deploy Backend to Render (10 minutes)

### Step 1: Prepare Files
✅ `backend/requirements.txt` - Already exists  
✅ `backend/render.yaml` - Created (optional)  
✅ `backend/app/main.py` - Has health endpoint

### Step 2: Deploy on Render

1. **Go to Render:**
   - Visit https://render.com
   - Sign up/Login with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select your repo

3. **Configure Service:**
   ```
   Name: tax-memo-backend
   Region: Choose closest
   Branch: main
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables:**
   Go to "Environment" tab, add:
   ```
   OPENAI_API_KEY = your-openai-key
   QDRANT_URL = your-qdrant-url
   QDRANT_API_KEY = your-qdrant-key
   PORT = 10000
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for "Live" status (green)
   - Copy your URL: `https://your-app-name.onrender.com`

### Step 3: Test Backend
```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Should return: {"status": "healthy"}
```

---

## Part 2: Deploy Frontend to Streamlit (5 minutes)

### Step 1: Update API URL in Code

Edit `streamlit_app.py`, line 26-30:

**Option A: Keep Sidebar (User can change)**
```python
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://your-app-name.onrender.com",  # Your Render URL
    help="Enter your backend API URL"
)
```

**Option B: Hardcode (Production)**
```python
import os
API_URL = os.getenv("API_URL", "https://your-app-name.onrender.com")
```

### Step 2: Push to GitHub
```bash
git add streamlit_app.py
git commit -m "Configure Render backend URL"
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App:**
   - Click "New app"
   - Select your repository
   - Configure:
     ```
     Repository: your-repo
     Branch: main
     Main file path: streamlit_app.py
     App URL: tax-memo-generator (or your choice)
     ```

3. **Add Environment Variable (If using Option B):**
   - Go to "Settings" → "Secrets"
   - Add:
     ```
     API_URL=https://your-app-name.onrender.com
     ```

4. **Deploy:**
   - Click "Deploy"
   - Wait for "Running" status
   - Copy your URL: `https://your-app-name.streamlit.app`

---

## Part 3: Connect & Test

### Test Connection

1. Open Streamlit URL
2. If using sidebar: Enter Render URL
3. Fill out form with test data:
   ```
   Company Name: Test Company
   Industry: Software & Technology
   Primary Jurisdiction: Netherlands
   ```
4. Click "Generate Memo"
5. Verify it works!

---

## ✅ Checklist

**Backend (Render):**
- [ ] Render account created
- [ ] Web service created
- [ ] Environment variables set:
  - [ ] OPENAI_API_KEY
  - [ ] QDRANT_URL
  - [ ] QDRANT_API_KEY
- [ ] Service is "Live"
- [ ] Health check works
- [ ] Backend URL copied

**Frontend (Streamlit):**
- [ ] Streamlit account created
- [ ] API URL updated in code
- [ ] Code pushed to GitHub
- [ ] App deployed
- [ ] App is "Running"
- [ ] Frontend URL copied

**Connection:**
- [ ] Tested connection
- [ ] Memo generation works
- [ ] Ready to share!

---

## 🚨 Important Notes

### Render Free Tier Limitations:
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds
- ⚠️ Consider paid tier for production ($7/month for always-on)

### Streamlit Cloud:
- ✅ Free tier available
- ✅ Auto-updates on git push
- ✅ No spin-down issues

---

## 🔗 Your URLs

**Backend:** `https://your-app-name.onrender.com`  
**Frontend:** `https://your-app-name.streamlit.app`

**Share the Frontend URL with your tester!**

---

## 🎉 Done!

Once both are deployed and tested, you're ready to share with your CEO!

