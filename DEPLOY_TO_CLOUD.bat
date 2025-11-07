@echo off
chcp 65001 >nul
title Elite Trading Bot - Cloud Deployment

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    ☁️  ELITE TRADING BOT - CLOUD DEPLOYMENT WIZARD
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    This will help you deploy your bot to cloud for 24/7 operation!
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.

echo 📋 PRE-DEPLOYMENT CHECKLIST:
echo.
echo    ✓ Bot tested locally and working
echo    ✓ .env file configured with correct API keys
echo    ✓ Default password changed
echo    ✓ Email alerts working
echo.

set /p CONTINUE="Continue with cloud deployment? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo.
    echo ❌ Deployment cancelled
    pause
    exit /b
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    CHOOSE DEPLOYMENT PLATFORM
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    1. Railway.app       (Recommended - Easiest, FREE)
echo    2. Render.com        (Easy, FREE tier)
echo    3. Google Cloud Run  (Scalable, $300 credit)
echo    4. AWS EC2           (Professional, 12 months free)
echo    5. DigitalOcean      (Best performance, $200 credit)
echo    6. Local Docker Test (Test before cloud deploy)
echo.

set /p PLATFORM="Select platform (1-6): "

if "%PLATFORM%"=="1" goto railway
if "%PLATFORM%"=="2" goto render
if "%PLATFORM%"=="3" goto gcloud
if "%PLATFORM%"=="4" goto aws
if "%PLATFORM%"=="5" goto digitalocean
if "%PLATFORM%"=="6" goto docker_test
goto invalid

:railway
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🚂 RAILWAY.APP DEPLOYMENT
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Step 1: Push to GitHub
echo    ─────────────────────────
echo.
echo    Run these commands:
echo.
echo    git init
echo    git add .
echo    git commit -m "Elite Trading Bot - Cloud Ready"
echo    git branch -M main
echo    git remote add origin https://github.com/YOUR_USERNAME/elite-trading-bot.git
echo    git push -u origin main
echo.
echo    Step 2: Deploy on Railway
echo    ─────────────────────────
echo.
echo    1. Go to: https://railway.app/
echo    2. Sign up with GitHub (FREE)
echo    3. Click "New Project"
echo    4. Select "Deploy from GitHub repo"
echo    5. Choose your repository
echo    6. Add environment variables from .env file
echo    7. Deploy!
echo.
echo    Step 3: Access Your Bot
echo    ─────────────────────────
echo.
echo    Railway will give you a URL like:
echo    https://your-app.railway.app
echo.
echo    Open that URL and login with your credentials!
echo.
pause
goto end

:render
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🎨 RENDER.COM DEPLOYMENT
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Step 1: Push to GitHub (same as Railway)
echo.
echo    Step 2: Deploy on Render
echo    ────────────────────────
echo.
echo    1. Go to: https://render.com/
echo    2. Sign up with GitHub
echo    3. New → Web Service
echo    4. Connect your repository
echo    5. Configure:
echo       - Environment: Docker
echo       - Name: elite-trading-bot
echo    6. Add environment variables
echo    7. Create Web Service
echo.
echo    Step 3: Access
echo    ──────────────
echo.
echo    URL: https://elite-trading-bot.onrender.com
echo.
pause
goto end

:gcloud
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    ☁️  GOOGLE CLOUD RUN DEPLOYMENT
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Installing Google Cloud SDK...
echo.
start https://cloud.google.com/sdk/docs/install
echo.
echo    After installing, run:
echo.
echo    gcloud init
echo    gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/elite-trading-bot
echo    gcloud run deploy elite-trading-bot --image gcr.io/YOUR_PROJECT_ID/elite-trading-bot --platform managed --allow-unauthenticated
echo.
pause
goto end

:aws
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🚀 AWS EC2 DEPLOYMENT
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Opening AWS EC2 Console...
echo.
start https://console.aws.amazon.com/ec2/
echo.
echo    Follow the guide in CLOUD_DEPLOYMENT_GUIDE.md
echo    for detailed AWS setup instructions.
echo.
pause
goto end

:digitalocean
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🌊 DIGITALOCEAN DEPLOYMENT
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Opening DigitalOcean...
echo.
start https://www.digitalocean.com/
echo.
echo    1. Create account (get $200 credit!)
echo    2. Create Droplet:
echo       - Image: Docker on Ubuntu 22.04
echo       - Plan: $4/month
echo       - Region: Bangalore
echo    3. SSH and run:
echo.
echo       git clone https://github.com/YOUR_USERNAME/elite-trading-bot.git
echo       cd elite-trading-bot
echo       nano .env  # Add your variables
echo       docker-compose up -d
echo.
pause
goto end

:docker_test
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    🐳 LOCAL DOCKER TEST
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo    Testing bot with Docker locally...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not installed!
    echo.
    echo Please install Docker Desktop:
    start https://www.docker.com/products/docker-desktop
    pause
    goto end
)

echo ✓ Docker is installed
echo.
echo Building Docker image...
docker build -t elite-trading-bot .

if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check errors above.
    pause
    goto end
)

echo.
echo ✓ Image built successfully!
echo.
echo Starting container...
docker-compose up -d

if errorlevel 1 (
    echo.
    echo ❌ Failed to start! Check errors above.
    pause
    goto end
)

echo.
echo ✅ Bot is running in Docker!
echo.
echo Access at: http://localhost:5000
echo Login: admin / Elite@Bot2025
echo.
echo View logs: docker-compose logs -f
echo Stop bot: docker-compose down
echo.
pause
goto end

:invalid
echo.
echo ❌ Invalid selection!
pause
goto end

:end
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo    📚 For detailed instructions, see:
echo    CLOUD_DEPLOYMENT_GUIDE.md
echo ═══════════════════════════════════════════════════════════════════════════
echo.
pause
