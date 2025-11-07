"""
Elite Trading Bot - Cloud Deployment Manager
Runs bot 24/7 on cloud servers with auto-restart and monitoring
"""
import os
import sys
import time
import signal
import threading
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cloud_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CloudBotManager:
    """Manages bot execution in cloud environment"""
    
    def __init__(self):
        self.bot_process = None
        self.server_process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 100  # Unlimited restarts for 24/7 operation
        
    def start_bot(self):
        """Start the trading bot"""
        try:
            logger.info("🚀 Starting Elite Trading Bot...")
            
            bot_script = os.getenv('BOT_SCRIPT', 'Untitled-1.py')
            
            self.bot_process = subprocess.Popen(
                [sys.executable, bot_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"✅ Bot started (PID: {self.bot_process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            return False
    
    def start_server(self):
        """Start the global mobile server"""
        try:
            logger.info("🌍 Starting Global Mobile Server...")
            
            self.server_process = subprocess.Popen(
                [sys.executable, 'global_mobile_server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"✅ Server started (PID: {self.server_process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False
    
    def monitor_bot(self):
        """Monitor bot process and restart if crashed"""
        while self.running:
            try:
                if self.bot_process and self.bot_process.poll() is not None:
                    # Bot crashed
                    exit_code = self.bot_process.returncode
                    logger.warning(f"⚠️ Bot process exited with code {exit_code}")
                    
                    if self.restart_count < self.max_restarts:
                        self.restart_count += 1
                        logger.info(f"🔄 Restarting bot (attempt {self.restart_count}/{self.max_restarts})...")
                        time.sleep(5)  # Wait before restart
                        self.start_bot()
                    else:
                        logger.error("❌ Max restart attempts reached. Stopping.")
                        self.running = False
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"❌ Monitor error: {e}")
                time.sleep(10)
    
    def monitor_server(self):
        """Monitor server process and restart if crashed"""
        while self.running:
            try:
                if self.server_process and self.server_process.poll() is not None:
                    # Server crashed
                    exit_code = self.server_process.returncode
                    logger.warning(f"⚠️ Server process exited with code {exit_code}")
                    
                    logger.info("🔄 Restarting server...")
                    time.sleep(5)
                    self.start_server()
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"❌ Monitor error: {e}")
                time.sleep(10)
    
    def cleanup(self):
        """Clean shutdown"""
        logger.info("🛑 Shutting down...")
        self.running = False
        
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
                logger.info("✅ Bot process stopped")
            except:
                self.bot_process.kill()
        
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
                logger.info("✅ Server process stopped")
            except:
                self.server_process.kill()
    
    def run(self):
        """Main run loop"""
        logger.info("="*80)
        logger.info("🌍 ELITE TRADING BOT - CLOUD DEPLOYMENT")
        logger.info("="*80)
        logger.info(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"☁️  Environment: {'Docker' if os.path.exists('/.dockerenv') else 'Cloud VM'}")
        logger.info(f"🐍 Python: {sys.version.split()[0]}")
        logger.info(f"📁 Working Dir: {os.getcwd()}")
        logger.info("="*80)
        
        # Start both processes
        if not self.start_server():
            logger.error("❌ Failed to start server. Exiting.")
            return
        
        time.sleep(5)  # Let server initialize
        
        if not self.start_bot():
            logger.error("❌ Failed to start bot. Exiting.")
            self.cleanup()
            return
        
        # Start monitoring threads
        bot_monitor = threading.Thread(target=self.monitor_bot, daemon=True)
        server_monitor = threading.Thread(target=self.monitor_server, daemon=True)
        
        bot_monitor.start()
        server_monitor.start()
        
        logger.info("✅ All systems operational!")
        logger.info("🌍 Bot running 24/7 in cloud")
        logger.info("📱 Access from anywhere via mobile dashboard")
        logger.info("="*80)
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(60)
                
                # Periodic status
                if int(time.time()) % 3600 == 0:  # Every hour
                    logger.info(f"💚 Status: Bot running for {time.time() - start_time:.0f}s, Restarts: {self.restart_count}")
        
        except KeyboardInterrupt:
            logger.info("\n⏸️  Shutdown requested")
        
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"\n📡 Received signal {signum}")
    sys.exit(0)

def main():
    """Main entry point"""
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check critical files
    if not os.path.exists('Untitled-1.py'):
        logger.error("❌ Bot script (Untitled-1.py) not found!")
        return
    
    if not os.path.exists('global_mobile_server.py'):
        logger.error("❌ Server script (global_mobile_server.py) not found!")
        return
    
    if not os.path.exists('.env'):
        logger.warning("⚠️ .env file not found - using defaults")
    
    # Run cloud bot manager
    global start_time
    start_time = time.time()
    
    manager = CloudBotManager()
    manager.run()
    
    logger.info("👋 Cloud deployment stopped")

if __name__ == "__main__":
    main()
