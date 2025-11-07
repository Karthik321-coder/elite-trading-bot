@echo off
chcp 65001 >nul
title Elite Trading Bot - Deploy to Railway

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🚂 RAILWAY.APP DEPLOYMENT - AUTOMATED GUIDE
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Your bot is ready to deploy to Railway.app (FREE)!
echo    Just follow these simple steps:
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.

echo 📋 STEP 1: Create GitHub Repository
echo ─────────────────────────────────────
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: elite-trading-bot
echo 3. Make it PRIVATE (important for .env security)
echo 4. Do NOT initialize with README
echo 5. Click "Create repository"
echo.
pause

echo.
echo 📤 STEP 2: Push Code to GitHub
echo ─────────────────────────────────────
echo.
echo Your repository: https://github.com/Karthik321-coder/elite-trading-bot
echo.
echo Pushing code to GitHub...
echo.

git remote add origin https://github.com/Karthik321-coder/elite-trading-bot.git 2>nul
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  Push failed! Please:
    echo    1. Make sure you're logged into GitHub
    echo    2. Complete authentication in the browser window
    echo    3. Then run: git push -u origin main
    echo.
) else (
    echo.
    echo ✅ Code pushed to GitHub successfully!
    echo.
)

pause

echo.
echo 🚂 STEP 3: Deploy on Railway.app
echo ─────────────────────────────────────
echo.
echo Opening Railway.app...
start https://railway.app/
echo.
echo Follow these steps:
echo.
echo 1. Sign up / Login with GitHub account
echo 2. Click "New Project"
echo 3. Select "Deploy from GitHub repo"
echo 4. Choose: elite-trading-bot
echo 5. Railway will auto-detect Dockerfile
echo.
pause

echo.
echo ⚙️  STEP 4: Add Environment Variables
echo ─────────────────────────────────────
echo.
echo In Railway dashboard:
echo.
echo 1. Go to your project
echo 2. Click "Variables" tab
echo 3. Add these variables (copy from your .env file):
echo.
echo    DHAN_CLIENT_ID=1108804283
echo    DHAN_ACCESS_TOKEN=your_token_here
echo    USERNAME=admin
echo    PASSWORD=Elite@Bot2025
echo    PAPER_TRADING=1
echo    USE_MOCK_DATA=0
echo    PORT=5000
echo.
echo 4. Add email settings if you want alerts:
echo    EMAIL_ENABLED=true
echo    SMTP_SERVER=smtp.gmail.com
echo    SMTP_PORT=587
echo    SENDER_EMAIL=your@gmail.com
echo    SENDER_PASSWORD=your_app_password
echo    RECIPIENT_EMAILS=alerts@email.com
echo.
pause

echo.
echo 🚀 STEP 5: Deploy!
echo ─────────────────────────────────────
echo.
echo 1. Railway will automatically build and deploy
echo 2. Wait 3-5 minutes for build to complete
echo 3. Railway will give you a public URL
echo.
pause

echo.
echo ✅ STEP 6: Access Your Bot
echo ─────────────────────────────────────
echo.
echo 1. Get your URL from Railway dashboard
echo    Example: https://your-app.railway.app
echo.
echo 2. Open URL in browser
echo 3. Login with your credentials
echo 4. Control bot from ANYWHERE!
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🎉 SUCCESS! Your bot is now running 24/7 in the cloud!
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo Access from:
echo   📱 Your phone (anywhere with internet)
echo   💻 Any computer
echo   🌍 Anywhere in the world
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.
pause
