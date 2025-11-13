# Streamlit UI Deployment Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_streamlit.txt
```

### 2. Run Locally

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## Deployment Options

### Option 1: Streamlit Cloud (Easiest - Free)

1. **Push to GitHub:**
   ```bash
   git init
   git add streamlit_app.py requirements_streamlit.txt
   git commit -m "Add Streamlit UI"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Environment Variables:**
   - In Streamlit Cloud settings, add:
     - `API_URL` = Your backend API URL (e.g., `https://your-api.herokuapp.com`)

**Free tier includes:**
- Public apps
- Unlimited apps
- Automatic updates on git push

---

### Option 2: Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

### Option 3: Docker

1. **Create `Dockerfile`:**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   COPY requirements_streamlit.txt .
   RUN pip install -r requirements_streamlit.txt
   
   COPY streamlit_app.py .
   
   EXPOSE 8501
   
   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
   
   ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t tax-memo-ui .
   docker run -p 8501:8501 tax-memo-ui
   ```

---

### Option 4: AWS/Azure/GCP

**For AWS (EC2 or ECS):**
- Use Docker container
- Deploy to ECS or EC2 instance
- Configure security groups for port 8501

**For Azure:**
- Use Azure Container Instances
- Or deploy to Azure App Service

**For GCP:**
- Use Cloud Run
- Or deploy to Compute Engine

---

## Configuration

### Backend API URL

The app uses the API URL from the sidebar. For production:

1. **Set default in code:**
   ```python
   API_URL = st.sidebar.text_input(
       "Backend API URL",
       value="https://your-production-api.com",  # Change this
       help="Enter your backend API URL"
   )
   ```

2. **Or use environment variable:**
   ```python
   import os
   API_URL = os.getenv("API_URL", "http://localhost:8000")
   ```

---

## Testing Before Deployment

1. **Test locally:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Test with your backend:**
   - Make sure backend is running
   - Fill out the form
   - Click "Generate Memo"
   - Verify response

3. **Check all steps:**
   - Navigate through all 7 steps
   - Verify data is saved correctly
   - Test memo generation

---

## Troubleshooting

### Issue: Can't connect to backend
**Solution:** 
- Check API URL in sidebar
- Verify backend is running
- Check CORS settings on backend

### Issue: Timeout errors
**Solution:**
- Increase timeout in `generate_memo()` function
- Check backend response time
- Consider async processing

### Issue: Field mapping errors
**Solution:**
- Check `map_frontend_to_backend()` function
- Verify backend accepts the field names
- Check backend API documentation

---

## Security Considerations

1. **API Key Protection:**
   - Don't hardcode API keys
   - Use environment variables
   - Use Streamlit secrets for sensitive data

2. **Input Validation:**
   - Validate all user inputs
   - Sanitize data before sending to API

3. **Error Handling:**
   - Don't expose internal errors to users
   - Log errors server-side

---

## Customization

### Change Colors/Theme

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Add Logo

```python
st.sidebar.image("logo.png", use_container_width=True)
```

### Custom CSS

```python
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)
```

---

## Performance Tips

1. **Cache API calls:**
   ```python
   @st.cache_data
   def generate_memo_cached(request_data):
       return requests.post(...)
   ```

2. **Lazy load sections:**
   - Only load data when needed
   - Use expanders for optional sections

3. **Optimize images:**
   - Compress images
   - Use appropriate formats

---

## Support

For issues:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Check backend API is working
3. Review error messages in Streamlit logs

---

## Quick Deploy Checklist

- [ ] Test locally
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Configure API URL
- [ ] Test memo generation
- [ ] Share link with CEO
- [ ] Monitor for errors

---

**Recommended:** Use Streamlit Cloud for fastest deployment. It's free, automatic, and perfect for sharing with stakeholders.

