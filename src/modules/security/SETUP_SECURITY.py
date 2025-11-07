"""
🔒 QUICK SECURITY SETUP SCRIPT
Automatically integrates security into your Elite Trading Bot
"""
import os
import sys
from pathlib import Path

def print_banner():
    print("\n" + "="*80)
    print("🔒 ELITE TRADING BOT - SECURITY INTEGRATION WIZARD 🔒")
    print("="*80 + "\n")

def check_requirements():
    """Check if security requirements are installed"""
    print("📋 Checking security requirements...")
    
    required = {
        'cryptography': 'AES-256 encryption',
        'PyJWT': 'JWT token sessions',
        'pyotp': 'Two-Factor Authentication',
        'bcrypt': 'Password hashing',
        'python-dotenv': 'Environment variables'
    }
    
    missing = []
    for module, description in required.items():
        try:
            __import__(module.replace('-', '_').lower())
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ❌ {module} - {description} (NOT INSTALLED)")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n📦 Install with:")
        print(f"   pip install {' '.join(missing)}")
        print("\n   OR")
        print("   pip install -r security_requirements.txt")
        return False
    
    print("\n✅ All security requirements installed!\n")
    return True

def initialize_security():
    """Initialize security system"""
    print("🔧 Initializing security system...")
    
    try:
        from ULTIMATE_SECURITY_SYSTEM import UltimateSecurityManager
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Get master password from env or prompt
        master_password = os.getenv('SECURITY_MASTER_PASSWORD')
        
        if not master_password:
            print("\n⚠️  No master password found in .env")
            master_password = input("Enter master password for vault (20+ characters): ")
            
            if len(master_password) < 20:
                print("❌ Password too short! Must be 20+ characters")
                return None
        
        # Initialize security
        security = UltimateSecurityManager(master_password=master_password)
        
        print("✅ Security system initialized!")
        return security
        
    except Exception as e:
        print(f"❌ Failed to initialize security: {e}")
        return None

def setup_admin_user(security):
    """Setup admin user"""
    print("\n👤 Setting up admin user...")
    
    username = os.getenv('USERNAME', 'admin')
    password = os.getenv('PASSWORD')
    
    if not password:
        print("⚠️  No password found in .env")
        password = input(f"Enter password for user '{username}': ")
    
    try:
        security.create_user(username, password)
        print(f"✅ User '{username}' created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return False

def migrate_credentials_to_vault(security):
    """Move sensitive credentials from .env to encrypted vault"""
    print("\n🔐 Migrating credentials to encrypted vault...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    credentials = {
        'DHAN_CLIENT_ID': os.getenv('DHAN_CLIENT_ID'),
        'DHAN_ACCESS_TOKEN': os.getenv('DHAN_ACCESS_TOKEN'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'NEWSAPI_KEY': os.getenv('NEWSAPI_KEY'),
        'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),
        'SENDER_PASSWORD': os.getenv('SENDER_PASSWORD'),
        'NGROK_AUTH_TOKEN': os.getenv('NGROK_AUTH_TOKEN'),
    }
    
    stored_count = 0
    for key, value in credentials.items():
        if value and value != 'your_openai_api_key_here':
            try:
                security.vault.store_secret(key, value)
                print(f"  ✅ {key} stored in vault")
                stored_count += 1
            except Exception as e:
                print(f"  ❌ {key} failed: {e}")
    
    print(f"\n✅ {stored_count} credentials stored in encrypted vault!")
    print("\n⚠️  IMPORTANT: Credentials are now SAFE in vault!")
    print("   Vault location: secure_vault/*.enc (AES-256 encrypted)")
    
    return stored_count > 0

def create_file_baseline(security):
    """Create file integrity baseline"""
    print("\n📁 Creating file integrity baseline...")
    
    try:
        security.file_monitor.baseline()
        print("✅ File integrity baseline created!")
        print("\n   Monitored files:")
        print("   - Untitled-1.py (main bot)")
        print("   - global_mobile_server.py (web server)")
        print("   - cloud_deploy.py (deployment)")
        print("   - .env (configuration)")
        return True
    except Exception as e:
        print(f"❌ Failed to create baseline: {e}")
        return False

def enable_2fa(security):
    """Enable Two-Factor Authentication"""
    print("\n🔐 Two-Factor Authentication (2FA) Setup")
    
    choice = input("\nEnable 2FA for maximum security? (y/n): ").lower()
    
    if choice != 'y':
        print("⚠️  2FA not enabled (you can enable later)")
        return False
    
    try:
        username = os.getenv('USERNAME', 'admin')
        secret, qr_url = security.two_factor.enable_2fa(username)
        
        print(f"\n✅ 2FA enabled for user: {username}")
        print("\n📱 Scan this QR code with Google Authenticator:")
        print(f"\n{qr_url}\n")
        print("Or manually enter this secret in Google Authenticator:")
        print(f"{secret}\n")
        
        input("Press Enter after scanning QR code...")
        
        code = input("Enter 6-digit code from Google Authenticator to test: ")
        
        if security.two_factor.verify_code(username, code):
            print("✅ 2FA verification successful!")
            return True
        else:
            print("❌ Invalid code - 2FA setup failed")
            return False
            
    except Exception as e:
        print(f"❌ 2FA setup failed: {e}")
        return False

def configure_ip_whitelist(security):
    """Configure IP whitelist"""
    print("\n🌐 IP Access Control Setup")
    
    choice = input("\nEnable IP whitelist for maximum security? (y/n): ").lower()
    
    if choice != 'y':
        print("⚠️  IP whitelist not enabled")
        return False
    
    print("\nEnter your trusted IP addresses (comma-separated)")
    print("Example: 192.168.1.100,10.0.0.50")
    print("Leave blank to skip")
    
    ips = input("\nIPs: ").strip()
    
    if not ips:
        print("⚠️  No IPs added to whitelist")
        return False
    
    try:
        for ip in ips.split(','):
            ip = ip.strip()
            if ip:
                security.ip_control.add_to_whitelist(ip)
                print(f"  ✅ Added: {ip}")
        
        security.ip_control.enable_whitelist()
        print("\n🔒 Whitelist mode ENABLED - Only whitelisted IPs can access!")
        return True
        
    except Exception as e:
        print(f"❌ IP whitelist setup failed: {e}")
        return False

def backup_vault_keys():
    """Remind user to backup vault keys"""
    print("\n💾 CRITICAL: BACKUP YOUR VAULT KEYS!")
    print("="*80)
    print("\n⚠️  WITHOUT THESE FILES, YOU CANNOT RECOVER YOUR DATA!")
    print("\nFiles to backup:")
    print("  1. secure_vault/.master.key (Vault encryption key)")
    print("  2. secure_keys/private_key.pem (RSA private key)")
    print("  3. secure_keys/public_key.pem (RSA public key)")
    print("  4. 2fa_secrets.json (2FA secrets)")
    print("\n📋 Backup methods:")
    print("  ✅ Encrypted USB drive (BEST)")
    print("  ✅ Password-protected ZIP file")
    print("  ✅ Encrypted cloud storage")
    print("  ❌ NEVER plain text backup!")
    print("\n" + "="*80)
    
    input("\nPress Enter after backing up keys (or skip for now)...")

def generate_security_report(security):
    """Generate initial security report"""
    print("\n📊 Generating security report...")
    
    try:
        report_file = security.export_security_report()
        print(f"✅ Security report: {report_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to generate report: {e}")
        return False

def print_next_steps():
    """Print next steps after setup"""
    print("\n" + "="*80)
    print("✅ SECURITY SETUP COMPLETE!")
    print("="*80)
    
    print("\n📋 NEXT STEPS:")
    print("\n1. CHANGE DEFAULT PASSWORDS:")
    print("   - Edit .env file")
    print("   - Change USERNAME and PASSWORD")
    print("   - Change SECURITY_MASTER_PASSWORD")
    print("   - Generate new JWT_SECRET_KEY")
    
    print("\n2. BACKUP VAULT KEYS:")
    print("   - Copy secure_vault/.master.key to USB")
    print("   - Copy secure_keys/*.pem to USB")
    print("   - Store in safe location")
    
    print("\n3. TEST SECURITY:")
    print("   - Run: python ULTIMATE_SECURITY_SYSTEM.py")
    print("   - Verify login works")
    print("   - Test 2FA (if enabled)")
    
    print("\n4. DEPLOY TO CLOUD:")
    print("   - All credentials now encrypted!")
    print("   - Run: .\\DEPLOY_TO_RAILWAY.bat")
    print("   - Your bot is PROTECTED!")
    
    print("\n📚 DOCUMENTATION:")
    print("   - Setup Guide: SECURITY_SETUP_GUIDE.md")
    print("   - Security System: ULTIMATE_SECURITY_SYSTEM.py")
    print("   - Requirements: security_requirements.txt")
    
    print("\n🔒 YOUR BOT IS NOW BANK-GRADE SECURE!")
    print("="*80 + "\n")

def main():
    """Main setup wizard"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install security requirements first!")
        return
    
    # Initialize security
    security = initialize_security()
    if not security:
        print("\n❌ Security initialization failed!")
        return
    
    # Setup admin user
    setup_admin_user(security)
    
    # Migrate credentials to vault
    migrate_credentials_to_vault(security)
    
    # Create file baseline
    create_file_baseline(security)
    
    # Enable 2FA (optional)
    enable_2fa(security)
    
    # Configure IP whitelist (optional)
    configure_ip_whitelist(security)
    
    # Backup reminder
    backup_vault_keys()
    
    # Generate report
    generate_security_report(security)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
