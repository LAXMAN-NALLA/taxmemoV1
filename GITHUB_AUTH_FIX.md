# Fix GitHub Authentication Error

## Problem
```
remote: Permission to HOCEBRANCHAI/taxmemoV1.git denied to LAXMAN-NALLA.
error: 403
```

## Solution Options

### Option 1: Use Personal Access Token (Recommended)

1. **Create Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "Tax Memo Deployment"
   - Select scopes: `repo` (full control)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Push with Token:**
   ```bash
   git push -u origin main
   ```
   - When prompted for username: Enter `HOCEBRANCHAI`
   - When prompted for password: **Paste the token** (not your password!)

### Option 2: Update Git Credentials

**Clear cached credentials:**
```bash
git config --global --unset credential.helper
```

Then try pushing again - it will prompt for new credentials.

### Option 3: Use SSH Instead

1. **Change remote to SSH:**
   ```bash
   git remote set-url origin git@github.com:HOCEBRANCHAI/taxmemoV1.git
   ```

2. **Set up SSH key** (if not already):
   - Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Option 4: Check Repository Access

Make sure:
- Repository `HOCEBRANCHAI/taxmemoV1` exists
- You have write access to it
- You're logged into the correct GitHub account

---

## Quick Fix (Try This First)

1. **Clear Windows Credential Manager:**
   - Press `Win + R`
   - Type: `control /name Microsoft.CredentialManager`
   - Go to "Windows Credentials"
   - Find `git:https://github.com`
   - Delete it

2. **Try pushing again:**
   ```bash
   git push -u origin main
   ```
   - Enter username: `HOCEBRANCHAI`
   - Enter password: Use Personal Access Token (see Option 1)

---

## Recommended: Use Personal Access Token

This is the most reliable method for HTTPS authentication.

