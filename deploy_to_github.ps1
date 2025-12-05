# ============================================
# Streamlit Cloud Deployment Script (PowerShell)
# Creates a private GitHub repository and pushes code
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Streamlit Cloud Deployment Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $null = Get-Command git -ErrorAction Stop
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if GitHub CLI is installed
$ghInstalled = $false
try {
    $null = Get-Command gh -ErrorAction Stop
    $ghInstalled = $true
} catch {
    Write-Host ""
    Write-Host "WARNING: GitHub CLI (gh) is not installed." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You have two options:" -ForegroundColor Yellow
    Write-Host "  1. Install GitHub CLI: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host "  2. Manually create the repo on GitHub and use the alternative script" -ForegroundColor Yellow
    Write-Host ""
}

# Get repository name
$repoName = Read-Host "Enter GitHub repository name (e.g., lynx-apartment-dashboard)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "ERROR: Repository name cannot be empty" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize Git repository
Write-Host ""
Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Green
if (Test-Path .git) {
    Write-Host "Git repository already exists. Skipping initialization." -ForegroundColor Yellow
} else {
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to initialize Git repository" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Add all files
Write-Host ""
Write-Host "[2/5] Adding files to Git..." -ForegroundColor Green
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create initial commit
Write-Host ""
Write-Host "[3/5] Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Lynx Apartment Dashboard"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: If you see 'nothing to commit', files may already be committed" -ForegroundColor Yellow
}

# Create repository and push
if ($ghInstalled) {
    Write-Host ""
    Write-Host "[4/5] Checking GitHub CLI authentication..." -ForegroundColor Green
    
    # Check if user is logged in
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "You need to authenticate with GitHub CLI first." -ForegroundColor Yellow
        Write-Host "Running: gh auth login" -ForegroundColor Yellow
        Write-Host "Please follow the prompts to authenticate." -ForegroundColor Yellow
        gh auth login
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: GitHub authentication failed" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host "[5/5] Creating private GitHub repository and pushing..." -ForegroundColor Green
    gh repo create $repoName --private --source=. --remote=origin --push
    
    if ($LASTEXITCODE -eq 0) {
        $username = (gh api user -q .login)
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Green
        Write-Host "SUCCESS! Repository created and pushed." -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository URL: https://github.com/$username/$repoName" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Go to https://share.streamlit.io/" -ForegroundColor White
        Write-Host "2. Click 'New app'" -ForegroundColor White
        Write-Host "3. Connect your GitHub account (if not already connected)" -ForegroundColor White
        Write-Host "4. Select repository: $repoName" -ForegroundColor White
        Write-Host "5. Set main file: lynx_app.py" -ForegroundColor White
        Write-Host "6. Click 'Deploy'" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "ERROR: Failed to create repository via GitHub CLI" -ForegroundColor Red
        Write-Host ""
        Show-ManualSteps -RepoName $repoName
    }
} else {
    Write-Host ""
    Write-Host "[4/5] GitHub CLI not available - Manual setup required" -ForegroundColor Yellow
    Write-Host ""
    Show-ManualSteps -RepoName $repoName
    
    $repoUrl = Read-Host "Enter the repository URL"
    if (-not [string]::IsNullOrWhiteSpace($repoUrl)) {
        Write-Host ""
        Write-Host "[5/5] Adding remote and pushing..." -ForegroundColor Green
        git remote add origin $repoUrl
        git branch -M main
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "============================================" -ForegroundColor Green
            Write-Host "SUCCESS! Code pushed to GitHub." -ForegroundColor Green
            Write-Host "============================================" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
            Write-Host "Please check your repository URL and try again." -ForegroundColor Yellow
        }
    }
}

function Show-ManualSteps {
    param([string]$RepoName)
    
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "MANUAL STEPS REQUIRED:" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "2. Create a new PRIVATE repository named: $RepoName" -ForegroundColor White
    Write-Host "3. Do NOT initialize with README, .gitignore, or license" -ForegroundColor White
    Write-Host "4. Copy the repository URL (e.g., https://github.com/YOUR_USERNAME/$RepoName.git)" -ForegroundColor White
    Write-Host ""
}

Read-Host "Press Enter to exit"

