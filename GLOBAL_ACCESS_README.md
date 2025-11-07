# 🌍 Elite Trading Bot - Global Access Guide

**Access your trading bot from anywhere in the world - college, home, mobile data, anywhere!**

---

## 🚀 Quick Start (30 Seconds)

### Method 1: One-Click Start (Windows)
1. **Double-click**: `START_GLOBAL_BOT.bat`
2. **Wait** for URLs to appear (30 seconds)
3. **Open** the global URL on your phone
4. **Login** with credentials
5. **Start trading** from anywhere! 🎉

### Method 2: Python Start
```bash
python start_global_bot.py
```

---

## 📱 How It Works

### Local Access (Same WiFi Only)
- URL: `http://192.168.x.x:5000`
- Works only when phone is on same WiFi network
- **Limited to local network**

### Global Access (From Anywhere) ⭐
- URL: `https://abc123.ngrok.io` (unique for each session)
- Works from **any WiFi**, **mobile data**, **anywhere in world**
- **Requires ngrok (FREE)**

---

## 🔧 Setup Ngrok (For Global Access)

### Step 1: Get Free Ngrok Token
1. Go to: **https://ngrok.com/**
2. Click **"Sign up"** (100% FREE)
3. Login to dashboard
4. Copy your **Auth Token** (looks like: `2a1b2c3d4e5f6g7h8i9j0k`)

### Step 2: Configure Token
1. Open **`.env`** file in your bot folder
2. Find line: `NGROK_AUTH_TOKEN=`
3. Paste your token: `NGROK_AUTH_TOKEN=2a1b2c3d4e5f6g7h8i9j0k`
4. Save the file

### Step 3: Start Bot
Run `START_GLOBAL_BOT.bat` - You'll see:

```
========================================
🌍 GLOBAL ACCESS ENABLED
========================================
Public URL: https://abc123.ngrok.io
Local URL:  http://192.168.1.100:5000

✅ Access from ANYWHERE in the world!
========================================
```

### Step 4: Access from Phone
1. Open browser on your phone
2. Go to the **Public URL** (https://abc123.ngrok.io)
3. Works from **any network** - WiFi, 4G, 5G, anywhere!

---

## 🎯 Features

### 📊 Real-Time Dashboard
- **Total P&L** - Live profit/loss tracking
- **Win Rate** - Success percentage
- **Current Capital** - Real-time balance
- **Bot Status** - Running/Stopped with uptime

### 🎮 Bot Control
- **Start Trading** - Launch bot remotely
- **Stop Trading** - Pause bot safely
- **Restart Bot** - Quick restart

### 📈 Performance Charts
- **CPU Usage Graph** - Real-time resource monitoring
- **Trading Statistics** - Sharpe ratio, profit factor, max drawdown
- **System Resources** - CPU, RAM, Disk usage

### 💼 Trading Features
- **Active Positions** - Live position tracking
- **Recent Trades** - Complete trade history
- **Live Logs** - Real-time bot activity
- **Access Info** - URLs and connection details

---

## 🔐 Security

### Default Credentials
- **Username**: `admin`
- **Password**: `elite123`

### Change Password (RECOMMENDED)
1. Open **`.env`** file
2. Modify these lines:
   ```
   USERNAME=your_new_username
   PASSWORD=your_secure_password
   ```
3. Save and restart bot

### Session Timeout
- **8 hours** by default (full trading day)
- Auto-logout after timeout
- Change in `.env`: `SESSION_TIMEOUT=28800`

---

## 📡 Connection Types

### 1️⃣ Global URL (Ngrok) - RECOMMENDED ⭐
```
https://abc123.ngrok.io
```
- ✅ Works from **anywhere** in the world
- ✅ **Mobile data** supported
- ✅ **Different WiFi** networks
- ✅ **Secure HTTPS** encryption
- ⚠️ **Changes** each time you restart server
- 🆓 **FREE** with ngrok account

### 2️⃣ Local Network URL
```
http://192.168.1.100:5000
```
- ✅ Fast and reliable
- ✅ No internet required
- ❌ Works **only** on same WiFi network
- ❌ Can't access from mobile data

### 3️⃣ Localhost
```
http://localhost:5000
```
- ✅ Super fast
- ❌ Works **only** on same computer
- 💻 For testing on PC

---

## 🛠️ Troubleshooting

### Problem: "Ngrok not working"
**Solution**:
1. Check `.env` file has correct token
2. Verify `ENABLE_NGROK=true` in `.env`
3. Restart bot completely
4. Check ngrok.com account is active

### Problem: "Can't access from phone"
**Solution**:
1. Use **global URL** (https://abc123.ngrok.io)
2. Make sure server is running
3. Check phone has internet connection
4. Try refreshing browser page

### Problem: "Login not working"
**Solution**:
1. Check credentials in `.env` file
2. Default: admin / elite123
3. Clear browser cache/cookies
4. Try incognito/private browsing

### Problem: "Bot not starting from dashboard"
**Solution**:
1. Check `Untitled-1.py` exists in folder
2. Verify all dependencies installed
3. Check logs in **Live Logs** tab
4. Restart global server

### Problem: "Server crashes on start"
**Solution**:
```bash
# Install/Update dependencies
pip install -r requirements.txt

# Or install individually
pip install flask flask-socketio flask-cors psutil pyngrok python-dotenv
```

---

## 📂 File Structure

```
tr/
├── START_GLOBAL_BOT.bat          ← One-click launcher (Windows)
├── start_global_bot.py           ← Python launcher
├── global_mobile_server.py       ← Global server with ngrok
├── Untitled-1.py                 ← Main trading bot
├── .env                          ← Configuration file
├── requirements.txt              ← Dependencies
├── templates/
│   ├── login.html               ← Login page
│   └── advanced_dashboard.html  ← Main dashboard
└── GLOBAL_ACCESS_README.md      ← This file
```

---

## 🎓 Usage Examples

### Scenario 1: Access from College
1. Start bot at home using `START_GLOBAL_BOT.bat`
2. Note the **global URL** (https://abc123.ngrok.io)
3. Go to college
4. Open global URL on phone (on college WiFi or mobile data)
5. Control bot, check P&L, view logs
6. Bot keeps running at home!

### Scenario 2: Monitor While Traveling
1. Start bot before leaving home
2. Save global URL to phone
3. Check bot status anytime from anywhere
4. Stop/restart bot remotely if needed
5. View real-time performance and trades

### Scenario 3: Multi-Device Access
1. Access from phone (mobile data)
2. Access from laptop (different WiFi)
3. Access from tablet (anywhere)
4. All devices show same real-time data
5. Control from any device

---

## 💡 Pro Tips

### 📌 Bookmark Global URL
- Save URL to phone home screen
- Quick access like a native app
- Add to browser favorites

### 🔔 Enable Notifications
- Email notifications already integrated
- Get alerts on phone
- Track trades remotely

### ⚡ Keep Server Running
- Run on dedicated PC/laptop
- Use server/VPS for 24/7 access
- Consider cloud hosting for production

### 📊 Monitor Performance
- Check dashboard regularly
- Review trading statistics
- Optimize based on metrics

### 🔒 Security Best Practices
- Change default password immediately
- Don't share global URL publicly
- Use strong credentials
- Monitor access logs

---

## 🆘 Support

### Common Questions

**Q: Does ngrok slow down trading?**
A: No! Ngrok only tunnels the dashboard. Trading happens locally on your PC.

**Q: Is ngrok free forever?**
A: Yes! Free tier includes everything needed for personal use.

**Q: Can multiple people access?**
A: Yes, but only one should control bot to avoid conflicts.

**Q: What if global URL changes?**
A: URL changes each restart. Check server startup for new URL.

**Q: Can I use my own domain?**
A: Yes! Ngrok paid plans support custom domains.

---

## 🎯 Next Steps

1. ✅ **Setup ngrok** (5 minutes) - Get global access
2. ✅ **Change password** - Secure your bot
3. ✅ **Bookmark URLs** - Quick access
4. ✅ **Test from phone** - Verify it works
5. ✅ **Start trading** - Monitor from anywhere!

---

## 📞 Emergency Access

If you lose access:
1. Check server is still running
2. View startup logs for URLs
3. Restart `START_GLOBAL_BOT.bat`
4. Note new global URL
5. Access from phone again

---

## 🌟 Features Summary

| Feature | Local | Global (Ngrok) |
|---------|-------|----------------|
| Same WiFi Access | ✅ | ✅ |
| Different WiFi | ❌ | ✅ |
| Mobile Data | ❌ | ✅ |
| HTTPS Encryption | ❌ | ✅ |
| Worldwide Access | ❌ | ✅ |
| Setup Required | None | 5 min |
| Cost | Free | Free |

---

## 🔥 Why Global Access?

### Before (Local Only)
- ❌ Can't check bot from college
- ❌ Can't access on mobile data
- ❌ Limited to home WiFi
- ❌ Can't control while traveling

### After (Global Access) ⭐
- ✅ Access from **anywhere**
- ✅ Works on **mobile data**
- ✅ Monitor from **college/work**
- ✅ Control while **traveling**
- ✅ **Real-time** updates globally
- ✅ **Professional** trading setup

---

**Made with ❤️ for Elite Traders**

*Access your trading bot from anywhere in the world - trade with confidence, monitor with ease!*

---

### 🚀 Ready to Go Global?

1. Run `START_GLOBAL_BOT.bat`
2. Setup ngrok token (5 minutes)
3. Access from anywhere
4. Trade like a pro! 📈

**Happy Trading! 🎉**
