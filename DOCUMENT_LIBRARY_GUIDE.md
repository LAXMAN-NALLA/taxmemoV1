# Document Library Guide

## 📁 Document Storage Structure

### Current Location
```
1CountryTaxmemo/
├── source docs/
│   ├── netherlands/          # Netherlands documents (currently active)
│   │   ├── *.docx
│   │   ├── *.txt
│   │   ├── *.html
│   │   └── *.pdf
│   └── metadata_sources.json # Metadata file (optional)
│
└── backend/
    └── ingest_data.py        # Script to ingest documents into Qdrant
```

### Future Multi-Country Structure (Recommended)
```
1CountryTaxmemo/
├── source docs/
│   ├── netherlands/          # Netherlands documents
│   │   ├── *.docx
│   │   ├── *.txt
│   │   └── *.html
│   ├── belgium/             # Belgium documents (future)
│   │   ├── *.docx
│   │   └── *.txt
│   ├── germany/              # Germany documents (future)
│   │   ├── *.docx
│   │   └── *.txt
│   └── metadata_sources.json
│
└── backend/
    └── ingest_data.py
```

---

## 🔍 How to Access Documents

### Option 1: Direct File System Access
**Location:** `C:\Users\laxma\Desktop\1CountryTaxmemo\source docs\netherlands\`

**To Access:**
1. Navigate to the project folder
2. Open `source docs` folder
3. Open `netherlands` folder (or other country folder)
4. All documents are stored here as regular files

**Supported File Types:**
- `.docx` - Microsoft Word documents
- `.txt` - Plain text files
- `.html` - HTML files
- `.pdf` - PDF files (if added in future)

---

### Option 2: Through Version Control (Git)
If the project is in a Git repository:

```bash
# Clone the repository
git clone <repository-url>

# Navigate to documents
cd 1CountryTaxmemo/source docs/netherlands/

# View files
ls  # or dir on Windows
```

**Benefits:**
- Version history
- Collaboration
- Backup
- Change tracking

---

### Option 3: Network/Shared Drive Access
If documents are on a shared drive or network location:

**Windows:**
```
\\server-name\shared-folder\1CountryTaxmemo\source docs\netherlands\
```

**Benefits:**
- Multiple users can access
- Centralized storage
- Easy backup

---

## ✏️ How to Modify Documents

### Adding New Documents

**Step 1: Place Document in Correct Folder**
```bash
# For Netherlands
source docs/netherlands/your_new_document.docx

# For future countries
source docs/belgium/your_new_document.docx
```

**Step 2: Re-run Ingestion**
```bash
cd backend
python ingest_data.py
```

**Important:** The ingestion script automatically:
- Deletes old collection (prevents duplicates)
- Scans all files in `source docs/` and subfolders
- Creates fresh chunks
- Uploads to Qdrant

---

### Modifying Existing Documents

**Step 1: Edit the Document**
- Open the file directly (e.g., `source docs/netherlands/tax_guide.docx`)
- Make your changes
- Save the file

**Step 2: Re-run Ingestion**
```bash
cd backend
python ingest_data.py
```

**Note:** The system will automatically:
- Delete old version
- Process updated document
- Create new chunks with updated content

---

### Removing Documents

**Step 1: Delete the File**
```bash
# Delete from file system
rm source docs/netherlands/old_document.docx  # Linux/Mac
del source docs\netherlands\old_document.docx  # Windows
```

**Step 2: Re-run Ingestion**
```bash
cd backend
python ingest_data.py
```

The deleted document will be removed from the knowledge base.

---

## 👥 Collaboration Guide

### For Team Members

**1. Access Documents:**
- Documents are stored in: `source docs/[country]/`
- Anyone with file system access can view/edit

**2. Document Naming Convention:**
```
[country_code]_[topic]_[year].[extension]

Examples:
- nl_tax_rates_2025.txt
- nl_holding_company_guide_2025.docx
- nl_gdpr_compliance_2025.txt
```

**3. Adding Documents:**
1. Add file to appropriate country folder
2. Notify team to re-run ingestion
3. Or set up automated ingestion (see below)

**4. Document Standards:**
- Use clear, descriptive filenames
- Include year in filename (e.g., `_2025`)
- Keep documents organized by topic
- Update `metadata_sources.json` if using metadata

---

## 🔄 Automated Workflow (Recommended)

### Option 1: Git Hooks (Automatic Ingestion)
Create a Git hook that runs ingestion when documents are committed:

**File:** `.git/hooks/post-commit`
```bash
#!/bin/bash
cd backend
python ingest_data.py
```

**Benefits:**
- Automatic updates
- Version control
- Team collaboration

---

### Option 2: File Watcher (Real-time Updates)
Use a file watcher to automatically re-ingest when files change:

**Python Script Example:**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class DocumentHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.docx', '.txt', '.html')):
            print(f"Document changed: {event.src_path}")
            subprocess.run(["python", "backend/ingest_data.py"])

observer = Observer()
observer.schedule(DocumentHandler(), "source docs/", recursive=True)
observer.start()
```

---

### Option 3: Scheduled Ingestion
Run ingestion on a schedule (daily, weekly):

**Windows Task Scheduler:**
```batch
# Create scheduled task
schtasks /create /tn "IngestDocuments" /tr "python C:\path\to\backend\ingest_data.py" /sc daily /st 02:00
```

**Linux Cron:**
```bash
# Add to crontab
0 2 * * * cd /path/to/backend && python ingest_data.py
```

---

## 📊 Document Management Best Practices

### 1. Organization
```
source docs/
├── netherlands/
│   ├── tax/              # Tax-related documents
│   ├── legal/            # Legal documents
│   ├── compliance/       # Compliance documents
│   └── general/         # General documents
```

### 2. Version Control
- Use Git for document versioning
- Tag releases (e.g., `v1.0`, `v2.0`)
- Keep changelog of document updates

### 3. Metadata Tracking
Maintain `metadata_sources.json`:
```json
{
  "netherlands": {
    "documents": [
      {
        "filename": "nl_tax_rates_2025.txt",
        "topic": "Tax Rates",
        "year": 2025,
        "last_updated": "2025-01-15",
        "author": "Tax Team"
      }
    ]
  }
}
```

### 4. Backup Strategy
- Regular backups of `source docs/` folder
- Version control (Git)
- Cloud storage (OneDrive, Google Drive, etc.)

---

## 🌍 Multi-Country Setup (Future)

### Adding a New Country

**Step 1: Create Country Folder**
```bash
mkdir "source docs/belgium"
```

**Step 2: Add Documents**
```bash
# Copy documents to new folder
cp documents/*.docx "source docs/belgium/"
```

**Step 3: Update Ingestion Script**
Modify `backend/ingest_data.py` to support multiple countries:
```python
# Current (Netherlands only)
SOURCE_DIR = "../source docs"

# Future (Multi-country)
SOURCE_DIRS = {
    "netherlands": "../source docs/netherlands",
    "belgium": "../source docs/belgium",
    "germany": "../source docs/germany"
}
```

**Step 4: Re-run Ingestion**
```bash
python ingest_data.py
```

---

## 🔐 Access Control (For Teams)

### Option 1: File Permissions
**Windows:**
- Right-click folder → Properties → Security
- Set read/write permissions per user

**Linux/Mac:**
```bash
chmod 755 source\ docs/netherlands/  # Read/execute for all, write for owner
chown user:group source\ docs/netherlands/
```

### Option 2: Git Branching
- Main branch: Production documents
- Dev branch: Draft documents
- Review process before merging

### Option 3: Document Management System
- SharePoint
- Google Drive with permissions
- Confluence
- Notion

---

## 📝 Quick Reference

### Current Document Location
```
Windows: C:\Users\laxma\Desktop\1CountryTaxmemo\source docs\netherlands\
```

### To Add Documents
1. Copy file to `source docs/netherlands/`
2. Run: `cd backend && python ingest_data.py`

### To Modify Documents
1. Edit file in `source docs/netherlands/`
2. Run: `cd backend && python ingest_data.py`

### To Remove Documents
1. Delete file from `source docs/netherlands/`
2. Run: `cd backend && python ingest_data.py`

---

## 🆘 Troubleshooting

### Documents Not Appearing in API
**Solution:** Re-run ingestion script
```bash
cd backend
python ingest_data.py
```

### Duplicate Documents
**Solution:** The ingestion script automatically prevents duplicates by deleting the collection first. If you see duplicates, check:
1. File names are unique
2. Ingestion completed successfully
3. No errors in ingestion log

### Access Denied
**Solution:** Check file/folder permissions
```bash
# Windows: Right-click → Properties → Security
# Linux: chmod 755 source\ docs/netherlands/
```

---

## 📞 Support

For questions about document management:
1. Check this guide first
2. Review `backend/ingest_data.py` for ingestion logic
3. Check server logs for errors
4. Verify file paths are correct

---

## Summary

**Document Location:** `source docs/[country]/`
**Access Method:** Direct file system, Git, or shared drive
**Modification:** Edit files, then run `python ingest_data.py`
**Collaboration:** Use Git, shared drive, or document management system
**Future:** Easy to add new countries by creating new folders

