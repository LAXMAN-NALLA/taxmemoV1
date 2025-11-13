# Deploy to Render (Backend) + Streamlit Cloud (Frontend)

## 🎯 Deployment Plan

- **Backend:** Render.com (FastAPI)
- **Frontend:** Streamlit Cloud (Streamlit UI)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Backend for Render

**1.1. Create `render.yaml` (Optional but Recommended)**

Create this file in your `backend/` folder:

```yaml
services:
  - type: web
    name: tax-memo-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: QDRANT_URL
        value: your-qdrant-url
      - key: QDRANT_API_KEY
        sync: false
      - key: PORT
        value: 10000
```

**1.2. Check `requirements.txt` exists**

Make sure `backend/requirements.txt` has all dependencies:
- fastapi
- uvicorn
- openai
- langchain-openai
- langchain-qdrant
- qdrant-client
- python-dotenv
- pydantic
- etc.

### Step 2: Deploy on Render

**2.1. Create Account**
- Go to https://render.com
- Sign up with GitHub

**2.2. Create New Web Service**
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository
4. Configure:
   - **Name:** `tax-memo-backend` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main` (or your branch)
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**2.3. Set Environment Variables**
In Render dashboard, go to "Environment" tab and add:

```
OPENAI_API_KEY=your-openai-api-key
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
PORT=10000
```

**2.4. Deploy**
- Click "Create Web Service"
- Render will build and deploy
- Wait for "Live" status (green)

**2.5. Get Your Backend URL**
- Render provides: `https://your-app-name.onrender.com`
- Copy this URL (you'll need it for Streamlit)

**Important:** Render free tier spins down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

---

## Part 2: Deploy Frontend to Streamlit Cloud

### Step 1: Prepare Frontend

**1.1. Update API URL Default (Optional)**

You can set the Render URL as default in `streamlit_app.py`:

```python
# Option A: Keep sidebar input (user can change)
API_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://your-app-name.onrender.com",  # Your Render URL
    help="Enter your backend API URL"
)

# Option B: Use environment variable (more secure)
import os
API_URL = os.getenv("API_URL", "https://your-app-name.onrender.com")
```

**1.2. Push to GitHub**
```bash
git add streamlit_app.py requirements_streamlit.txt
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

**2.1. Create Account**
- Go to https://share.streamlit.io
- Sign in with GitHub

**2.2. Create New App**
1. Click "New app"
2. Select your GitHub repository
3. Configure:
   - **Repository:** Your repo
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose a name (e.g., `tax-memo-generator`)

**2.3. Set Environment Variables (Optional)**
If you used Option B above, go to "Settings" → "Secrets" and add:
```
API_URL=https://your-app-name.onrender.com
```

**2.4. Deploy**
- Click "Deploy"
- Streamlit will build and deploy
- Wait for "Running" status

**2.5. Get Your Frontend URL**
- Streamlit provides: `https://your-app-name.streamlit.app`
- This is your public URL to share!

---

## Part 3: Connect Frontend to Backend

### Option A: Sidebar Input (Easiest)

The Streamlit app already has a sidebar input. Users can:
1. Open Streamlit app
2. See sidebar on left
3. Enter Render backend URL: `https://your-app-name.onrender.com`
4. Click "Generate Memo"

### Option B: Hardcode in Code (For Production)

Edit `streamlit_app.py`:

```python
# Replace line 26-30 with:
import os
API_URL = os.getenv("API_URL", "https://your-app-name.onrender.com")

# Or remove sidebar input and use:
# API_URL = "https://your-app-name.onrender.com"
```

Then push to GitHub (Streamlit auto-updates).

---

## Part 4: Testing

### Test Backend Directly

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Generate memo
curl -X POST https://your-app-name.onrender.com/generate-memo \
  -H "Content-Type: application/json" \
  -d '{"companyName": "Test Company", "primaryJurisdiction": "Netherlands"}'
```

### Test Frontend

1. Open Streamlit URL
2. Enter Render backend URL in sidebar
3. Fill out form
4. Click "Generate Memo"
5. Verify it works

---

## 🔧 Troubleshooting

### Issue: Backend returns 404

**Solution:**
- Check Render logs
- Verify start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Check if app is "Live" (not "Stopped")

### Issue: Backend times out

**Solution:**
- Render free tier spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading to paid tier for always-on

### Issue: Frontend can't connect to backend

**Solution:**
- Verify backend URL is correct
- Check CORS settings in FastAPI (should allow Streamlit domain)
- Check Render logs for errors

### Issue: Environment variables not working

**Solution:**
- Verify variables are set in Render dashboard
- Check variable names match code
- Restart service after adding variables

---

## 📋 Pre-Deployment Checklist

**Backend (Render):**
- [ ] `requirements.txt` exists in `backend/` folder
- [ ] `render.yaml` created (optional)
- [ ] Environment variables ready:
  - [ ] `OPENAI_API_KEY`
  - [ ] `QDRANT_URL`
  - [ ] `QDRANT_API_KEY`
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Backend URL copied

**Frontend (Streamlit):**
- [ ] `streamlit_app.py` ready
- [ ] `requirements_streamlit.txt` exists
- [ ] API URL configured (sidebar or hardcoded)
- [ ] Code pushed to GitHub
- [ ] Streamlit app deployed
- [ ] Frontend URL copied

**Connection:**
- [ ] Backend URL added to Streamlit (sidebar or code)
- [ ] Tested connection
- [ ] Verified memo generation works

---

## 🎯 Quick Reference

**Backend URL:** `https://your-app-name.onrender.com`  
**Frontend URL:** `https://your-app-name.streamlit.app`

**Backend Health Check:** `https://your-app-name.onrender.com/health`  
**Backend API Endpoint:** `https://your-app-name.onrender.com/generate-memo`

---

## ✅ You're Ready!

Once both are deployed:
1. Share Streamlit URL with tester
2. Tester enters Render URL in sidebar (or it's already configured)
3. Test and verify!

---

## 💡 Pro Tips

1. **Render Free Tier:** Spins down after 15 min. First request is slow (~30s). Consider paid tier for production.

2. **Streamlit Auto-Updates:** Every git push to main branch auto-updates Streamlit app.

3. **Backend Logs:** Check Render dashboard → Logs tab for debugging.

4. **Frontend Logs:** Check Streamlit dashboard → Logs for errors.

5. **CORS:** FastAPI should allow Streamlit domain. Check `app/main.py` for CORS settings.

---

## 🚀 Next Steps

1. Deploy backend to Render
2. Deploy frontend to Streamlit Cloud
3. Connect them (configure API URL)
4. Test with sample input
5. Share Streamlit URL with tester!

Good luck! 🎉

