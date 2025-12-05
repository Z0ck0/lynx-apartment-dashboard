@echo off
REM ============================================
REM Streamlit Cloud Deployment Script
REM Creates a private GitHub repository and pushes code
REM ============================================

echo.
echo ============================================
echo Streamlit Cloud Deployment Setup
echo ============================================
echo.

REM Check if Git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Check if GitHub CLI is installed
where gh >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: GitHub CLI (gh) is not installed.
    echo.
    echo You have two options:
    echo   1. Install GitHub CLI: https://cli.github.com/
    echo   2. Manually create the repo on GitHub and use the alternative script
    echo.
    echo For now, we'll initialize Git and prepare for manual repo creation.
    echo.
    pause
)

REM Get repository name
set /p REPO_NAME="Enter GitHub repository name (e.g., lynx-apartment-dashboard): "
if "%REPO_NAME%"=="" (
    echo ERROR: Repository name cannot be empty
    pause
    exit /b 1
)

REM Initialize Git repository
echo.
echo [1/5] Initializing Git repository...
if exist .git (
    echo Git repository already exists. Skipping initialization.
) else (
    git init
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to initialize Git repository
        pause
        exit /b 1
    )
)

REM Add all files
echo.
echo [2/5] Adding files to Git...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

REM Create initial commit
echo.
echo [3/5] Creating initial commit...
git commit -m "Initial commit: Lynx Apartment Dashboard"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create commit
    echo Note: If you see "nothing to commit", files may already be committed
)

REM Check if GitHub CLI is available
where gh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [4/5] Creating private GitHub repository...
    
    REM Check if user is logged in to GitHub CLI
    gh auth status >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo You need to authenticate with GitHub CLI first.
        echo Running: gh auth login
        echo Please follow the prompts to authenticate.
        gh auth login
        if %ERRORLEVEL% NEQ 0 (
            echo ERROR: GitHub authentication failed
            pause
            exit /b 1
        )
    )
    
    REM Create private repository
    gh repo create %REPO_NAME% --private --source=. --remote=origin --push
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ============================================
        echo SUCCESS! Repository created and pushed.
        echo ============================================
        echo.
        echo Repository URL: https://github.com/%USERNAME%/%REPO_NAME%
        echo.
        echo Next steps:
        echo 1. Go to https://share.streamlit.io/
        echo 2. Click "New app"
        echo 3. Connect your GitHub account (if not already connected)
        echo 4. Select repository: %REPO_NAME%
        echo 5. Set main file: lynx_app.py
        echo 6. Click "Deploy"
        echo.
    ) else (
        echo.
        echo ERROR: Failed to create repository via GitHub CLI
        echo.
        echo Manual steps:
        echo 1. Go to https://github.com/new
        echo 2. Create a new PRIVATE repository named: %REPO_NAME%
        echo 3. Do NOT initialize with README, .gitignore, or license
        echo 4. Then run these commands:
        echo    git remote add origin https://github.com/YOUR_USERNAME/%REPO_NAME%.git
        echo    git branch -M main
        echo    git push -u origin main
        echo.
    )
) else (
    echo.
    echo [4/5] GitHub CLI not available - Manual setup required
    echo.
    echo ============================================
    echo MANUAL STEPS REQUIRED:
    echo ============================================
    echo.
    echo 1. Go to https://github.com/new
    echo 2. Create a new PRIVATE repository named: %REPO_NAME%
    echo 3. Do NOT initialize with README, .gitignore, or license
    echo 4. Copy the repository URL (e.g., https://github.com/YOUR_USERNAME/%REPO_NAME%.git)
    echo.
    set /p REPO_URL="Enter the repository URL: "
    if not "%REPO_URL%"=="" (
        echo.
        echo [5/5] Adding remote and pushing...
        git remote add origin %REPO_URL%
        git branch -M main
        git push -u origin main
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo ============================================
            echo SUCCESS! Code pushed to GitHub.
            echo ============================================
        ) else (
            echo.
            echo ERROR: Failed to push to GitHub
            echo Please check your repository URL and try again.
        )
    )
)

echo.
pause

