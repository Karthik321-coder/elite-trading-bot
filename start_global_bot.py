"""
Elite Trading Bot - Global Access Launcher
Starts the bot with worldwide internet access via ngrok
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Display startup banner"""
    print("\n" + "="*70)
    print("🌍 ELITE TRADING BOT - GLOBAL ACCESS LAUNCHER")
    print("="*70 + "\n")

def check_python():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} detected\n")
        return True
    else:
        print(f"   ❌ Python 3.8+ required (you have {version.major}.{version.minor})\n")
        return False

def check_dependencies():
    """Check and install dependencies"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask-socketio', 
        'flask-cors',
        'psutil',
        'pyngrok',
        'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   ⚠️  Missing packages: {', '.join(missing)}")
        print("   📥 Installing missing dependencies...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--upgrade'
            ] + missing, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("   ✅ All dependencies installed\n")
            return True
        except:
            print("   ❌ Failed to install dependencies")
            print("   💡 Try manually: pip install " + " ".join(missing) + "\n")
            return False
    else:
        print("   ✅ All dependencies satisfied\n")
        return True

def check_env_file():
    """Check and setup .env file"""
    print("⚙️  Checking configuration...")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ⚠️  .env file not found")
        print("   📝 Creating .env file...")
        
        env_content = """# Elite Trading Bot - Global Access Configuration

# Server Settings
PORT=5000
SECRET_KEY=elite_bot_secret_key_change_this_in_production

# Ngrok Settings (for global internet access)
ENABLE_NGROK=true
NGROK_AUTH_TOKEN=

# Login Credentials
USERNAME=admin
PASSWORD=elite123

# Bot Configuration
BOT_SCRIPT=Untitled-1.py
LOG_FILE=elite_bot.log

# Session Settings
SESSION_TIMEOUT=28800
"""
        
        env_path.write_text(env_content, encoding='utf-8')
        print("   ✅ .env file created\n")
    else:
        print("   ✅ .env file exists\n")
    
    # Check for ngrok token
    from dotenv import load_dotenv
    load_dotenv()
    
    ngrok_token = os.getenv('NGROK_AUTH_TOKEN', '')
    enable_ngrok = os.getenv('ENABLE_NGROK', 'true').lower() == 'true'
    
    if enable_ngrok and not ngrok_token:
        print("⚠️  NGROK SETUP REQUIRED FOR GLOBAL ACCESS")
        print("-" * 70)
        print("📌 To access your bot from anywhere in the world:")
        print("   1. Go to: https://ngrok.com/")
        print("   2. Sign up for FREE account")
        print("   3. Copy your auth token from dashboard")
        print("   4. Open .env file and set: NGROK_AUTH_TOKEN=your_token_here")
        print()
        print("💡 Without ngrok token, bot will work only on local WiFi network")
        print("-" * 70)
        
        choice = input("\n➡️  Continue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            print("\n❌ Setup cancelled. Please configure ngrok token first.\n")
            return False
        
        print()
    
    return True

def start_global_server():
    """Start the global mobile server"""
    print("🚀 Starting Elite Trading Bot with Global Access...")
    print("-" * 70)
    
    # Start the server
    try:
        server_script = Path('global_mobile_server.py')
        
        if not server_script.exists():
            print("❌ global_mobile_server.py not found!")
            print("💡 Make sure you're in the correct directory\n")
            return False
        
        print("📡 Initializing server...")
        print("🌐 Creating secure tunnel...")
        print()
        
        # Run the server
        subprocess.run([sys.executable, str(server_script)])
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Server stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False

def main():
    """Main launcher"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("\nPress Enter to exit...")
        return
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    # Check .env
    if not check_env_file():
        input("\nPress Enter to exit...")
        return
    
    # Start server
    print("=" * 70)
    start_global_server()
    print("\n" + "=" * 70)
    print("👋 Thank you for using Elite Trading Bot!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Launcher interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}\n")
        input("Press Enter to exit...")
