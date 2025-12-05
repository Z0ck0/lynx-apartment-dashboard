# Streamlit Cloud Deployment Instructions

This guide will help you deploy your Lynx Apartment Dashboard to Streamlit Cloud using a **private GitHub repository**.

## 📋 Prerequisites

1. **Git** installed on your system
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

2. **GitHub Account**
   - Create account: https://github.com/signup

3. **GitHub CLI (Optional but Recommended)**
   - Download: https://cli.github.com/
   - Verify: `gh --version`
   - Authenticate: `gh auth login`

## 🚀 Quick Deployment

### Option 1: Automated Script (Recommended)

#### Windows (Batch Script)
```cmd
deploy_to_github.bat
```

#### Windows (PowerShell)
```powershell
.\deploy_to_github.ps1
```

The script will:
1. Initialize Git repository (if not already done)
2. Add all files to Git
3. Create initial commit
4. Create a private GitHub repository
5. Push code to GitHub

### Option 2: Manual Deployment

If you prefer to do it manually or the script doesn't work:

#### Step 1: Initialize Git Repository

```cmd
git init
git add .
git commit -m "Initial commit: Lynx Apartment Dashboard"
```

#### Step 2: Create Private GitHub Repository

1. Go to https://github.com/new
2. Repository name: `lynx-apartment-dashboard` (or your preferred name)
3. **IMPORTANT**: Select **Private** (not Public)
4. **DO NOT** check:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
5. Click "Create repository"

#### Step 3: Connect and Push

```cmd
git remote add origin https://github.com/YOUR_USERNAME/lynx-apartment-dashboard.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## ☁️ Deploy to Streamlit Cloud

### Step 1: Connect GitHub to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

### Step 2: Grant Access to Private Repositories

**CRITICAL**: Streamlit Cloud needs permission to access private repositories.

1. After signing in, you'll be redirected to GitHub authorization
2. **Make sure to grant the following permissions:**
   - ✅ `repo` scope (Full control of private repositories)
   - ✅ `read:org` scope (if you're in organizations)

3. If you've already authorized but didn't grant private repo access:
   - Go to GitHub Settings → Applications → Authorized OAuth Apps
   - Find "Streamlit Cloud"
   - Click "Grant" next to the required permissions
   - Or revoke and re-authorize with full permissions

### Step 3: Deploy Your App

1. On Streamlit Cloud dashboard, click **"New app"**
2. Fill in the deployment form:
   - **Repository**: Select `lynx-apartment-dashboard` (or your repo name)
   - **Branch**: `main` (or `master`)
   - **Main file path**: `lynx_app.py`
   - **App URL**: Choose a custom subdomain (optional)
3. Click **"Deploy"**

### Step 4: Configure Secrets (If Needed)

If your app uses secrets (email, API keys, etc.):

1. In Streamlit Cloud dashboard, go to your app
2. Click **"Settings"** (⚙️ icon)
3. Go to **"Secrets"** tab
4. Add your secrets in TOML format:

```toml
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"

[sendgrid]
api_key = "your-sendgrid-api-key"
from_email = "your-email@example.com"
```

5. Click **"Save"**
6. The app will automatically redeploy

## 📁 Project Structure

Your project should have this structure:

```
lynx-apartment-dashboard/
├── lynx_app.py                 # Main Streamlit app
├── export_helpers.py           # Export helper functions
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── secrets.toml.example    # Secrets template (not committed)
├── assets/
│   ├── lynx_logo_dark.png
│   └── lynx_logo_light.png
├── Lynx Apartment Tracker.xlsx # Data file (will be in repo)
├── lynx_custom_metrics.json
├── lynx_custom_graphs.json
└── lynx_report_templates.json
```

## 🔐 Security Notes

### Private Repository

- ✅ Your repository is **PRIVATE** - only you (and collaborators) can see it
- ✅ Streamlit Cloud can access it via OAuth authorization
- ✅ Your code and data remain secure

### Sensitive Data

- ❌ **DO NOT** commit `.streamlit/secrets.toml` (already in `.gitignore`)
- ❌ **DO NOT** commit API keys, passwords, or tokens
- ✅ Use Streamlit Cloud Secrets for sensitive configuration
- ✅ The Excel file (`Lynx Apartment Tracker.xlsx`) is included in the repo

### GitHub Permissions

Streamlit Cloud requires these OAuth scopes for private repositories:
- `repo` - Full control of private repositories
- `read:org` - Read org and team membership (if applicable)

## 🐛 Troubleshooting

### "Unable to deploy" Error

**Problem**: Streamlit Cloud can't access your private repository.

**Solution**:
1. Go to GitHub Settings → Applications → Authorized OAuth Apps
2. Find "Streamlit Cloud"
3. Ensure `repo` scope is granted
4. If not, revoke and re-authorize

### "Module not found" Error

**Problem**: Missing dependencies.

**Solution**:
1. Check `requirements.txt` includes all packages
2. Verify versions are compatible
3. Streamlit Cloud will install packages automatically

### "File not found" Error

**Problem**: App can't find `Lynx Apartment Tracker.xlsx`.

**Solution**:
1. Ensure the Excel file is committed to Git
2. Check the file path in `lynx_app.py` matches the actual location
3. The file should be in the root directory

### Deployment Fails

**Common causes**:
- Missing `requirements.txt`
- Wrong main file path (should be `lynx_app.py`)
- Syntax errors in Python code
- Missing dependencies

**Check logs**:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View "Logs" to see error messages

## 📝 Post-Deployment

### Update Your App

1. Make changes locally
2. Commit and push:
   ```cmd
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Streamlit Cloud will automatically redeploy

### Monitor Your App

- View logs in Streamlit Cloud dashboard
- Check app status and resource usage
- Monitor for errors or performance issues

## 🔗 Useful Links

- Streamlit Cloud: https://share.streamlit.io/
- Streamlit Documentation: https://docs.streamlit.io/
- GitHub: https://github.com/
- GitHub CLI: https://cli.github.com/

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] All files committed
- [ ] Private GitHub repository created
- [ ] Code pushed to GitHub
- [ ] GitHub account connected to Streamlit Cloud
- [ ] Private repository access granted
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets configured (if needed)
- [ ] App is running successfully

## 🎉 Success!

Once deployed, your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

You can share this URL with authorized users. Since your repository is private, only you control who can access the deployed app.

---

**Need Help?**
- Check Streamlit Community Forum: https://discuss.streamlit.io/
- Review Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud

