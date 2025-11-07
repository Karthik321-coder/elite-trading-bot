"""
🔒 SECURITY STATUS DASHBOARD
Real-time security monitoring and health check
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    """Print section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def check_security_files():
    """Check if security files exist"""
    print_header("📁 SECURITY FILES STATUS")
    
    files = {
        'ULTIMATE_SECURITY_SYSTEM.py': 'Main security system',
        'SECURITY_SETUP_GUIDE.md': 'Setup documentation',
        'SETUP_SECURITY.py': 'Setup wizard',
        'security_requirements.txt': 'Security dependencies',
        'secure_vault/': 'Encrypted credential vault',
        'secure_keys/': 'RSA key storage',
        'security_audit_trail.jsonl': 'Security event log',
        'file_integrity.json': 'File integrity database',
    }
    
    for file, description in files.items():
        path = Path(file)
        if path.exists():
            if path.is_dir():
                count = len(list(path.glob('*')))
                print(f"  ✅ {file:<40} {description} ({count} files)")
            else:
                size = path.stat().st_size / 1024
                print(f"  ✅ {file:<40} {description} ({size:.1f} KB)")
        else:
            print(f"  ❌ {file:<40} {description} (NOT FOUND)")

def check_env_security():
    """Check .env security configuration"""
    print_header("⚙️  ENVIRONMENT SECURITY CONFIG")
    
    configs = {
        'SECURITY_MASTER_PASSWORD': 'Vault master password',
        'JWT_SECRET_KEY': 'JWT token secret',
        'IP_WHITELIST_ENABLED': 'IP whitelist mode',
        'RATE_LIMIT_ENABLED': 'Rate limiting',
        'TWO_FACTOR_ENABLED': 'Two-Factor Auth (2FA)',
        'FILE_INTEGRITY_CHECK': 'File integrity monitoring',
        'SECURITY_AUDIT_ENABLED': 'Security audit trail',
        'AUTO_LOCKDOWN_ENABLED': 'Auto-lockdown protection',
    }
    
    for key, description in configs.items():
        value = os.getenv(key, 'NOT SET')
        
        if value == 'NOT SET':
            status = '❌'
        elif key in ['SECURITY_MASTER_PASSWORD', 'JWT_SECRET_KEY']:
            status = '🔒' if len(value) >= 32 else '⚠️'
            value = f"{'*' * 40} (length: {len(value)})"
        else:
            status = '✅' if value.lower() in ('true', '1', 'yes') else '⚠️'
        
        print(f"  {status} {key:<35} {value:<30} {description}")

def check_protected_credentials():
    """Check if sensitive credentials are set"""
    print_header("🔐 CREDENTIAL PROTECTION STATUS")
    
    credentials = {
        'DHAN_CLIENT_ID': 'Dhan Client ID',
        'DHAN_ACCESS_TOKEN': 'Dhan Access Token',
        'OPENAI_API_KEY': 'OpenAI API Key',
        'SENDER_PASSWORD': 'Email Password',
        'NGROK_AUTH_TOKEN': 'Ngrok Auth Token',
    }
    
    vault_exists = Path('secure_vault').exists()
    
    for key, description in credentials.items():
        value = os.getenv(key)
        
        if not value or value.startswith('your_'):
            print(f"  ⚠️  {key:<25} {description:<30} NOT SET")
        else:
            # Check if in vault
            if vault_exists:
                vault_file = Path(f'secure_vault/{key}.enc')
                if vault_file.exists():
                    print(f"  🔒 {key:<25} {description:<30} ENCRYPTED IN VAULT ✅")
                else:
                    print(f"  ⚠️  {key:<25} {description:<30} IN .ENV (move to vault!)")
            else:
                print(f"  ⚠️  {key:<25} {description:<30} IN .ENV (vault not created)")

def check_password_strength():
    """Check password strength"""
    print_header("🔑 PASSWORD STRENGTH ANALYSIS")
    
    passwords = {
        'PASSWORD': 'Login Password',
        'SECURITY_MASTER_PASSWORD': 'Vault Master Password',
    }
    
    for key, description in passwords.items():
        password = os.getenv(key, '')
        
        if not password:
            print(f"  ❌ {description:<30} NOT SET")
            continue
        
        # Check strength
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        score = sum([
            length >= 12,
            length >= 20,
            has_upper,
            has_lower,
            has_digit,
            has_special,
        ])
        
        if score >= 5:
            status = '✅ STRONG'
        elif score >= 3:
            status = '⚠️  MEDIUM'
        else:
            status = '❌ WEAK'
        
        print(f"  {status:<20} {description:<30} Length: {length}")
        print(f"                         Uppercase: {'✅' if has_upper else '❌'}  "
              f"Lowercase: {'✅' if has_lower else '❌'}  "
              f"Digits: {'✅' if has_digit else '❌'}  "
              f"Special: {'✅' if has_special else '❌'}")

def check_file_integrity():
    """Check file integrity"""
    print_header("📋 FILE INTEGRITY STATUS")
    
    integrity_file = Path('file_integrity.json')
    
    if not integrity_file.exists():
        print("  ⚠️  Baseline not created")
        print("     Run: python -c \"from ULTIMATE_SECURITY_SYSTEM import *; UltimateSecurityManager().file_monitor.baseline()\"")
        return
    
    try:
        from ULTIMATE_SECURITY_SYSTEM import UltimateSecurityManager
        
        security = UltimateSecurityManager(master_password=os.getenv('SECURITY_MASTER_PASSWORD'))
        modified = security.file_monitor.check_integrity()
        
        if not modified:
            print("  ✅ All monitored files intact - NO tampering detected")
        else:
            print(f"  ⚠️  {len(modified)} file(s) modified:")
            for file in modified:
                print(f"     - {file}")
    except Exception as e:
        print(f"  ❌ Check failed: {e}")

def check_security_audit():
    """Check security audit trail"""
    print_header("📊 SECURITY AUDIT TRAIL")
    
    audit_file = Path('security_audit_trail.jsonl')
    
    if not audit_file.exists():
        print("  ⚠️  No audit trail yet (will be created on first security event)")
        return
    
    import json
    
    events = []
    with open(audit_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                events.append(json.loads(line.strip()))
            except:
                pass
    
    if not events:
        print("  ⚠️  No events logged yet")
        return
    
    print(f"  📝 Total events: {len(events)}")
    
    # Count event types
    event_types = {}
    for event in events:
        event_type = event.get('event_type', 'UNKNOWN')
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    print("\n  Event breakdown:")
    for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
        print(f"     {event_type:<30} {count} times")
    
    # Show recent events
    print("\n  Recent events (last 5):")
    for event in events[-5:]:
        timestamp = event.get('timestamp', 'N/A')
        event_type = event.get('event_type', 'N/A')
        user = event.get('user_id', 'N/A')
        ip = event.get('ip_address', 'N/A')
        print(f"     {timestamp} | {event_type:<25} | User: {user:<10} | IP: {ip}")

def check_ip_control():
    """Check IP access control"""
    print_header("🌐 IP ACCESS CONTROL")
    
    ip_file = Path('ip_access_control.json')
    
    if not ip_file.exists():
        print("  ⚠️  IP control not configured")
        return
    
    import json
    config = json.loads(ip_file.read_text())
    
    whitelist = config.get('whitelist', [])
    blacklist = config.get('blacklist', [])
    whitelist_enabled = config.get('whitelist_enabled', False)
    
    print(f"  Whitelist Mode: {'🔒 ENABLED' if whitelist_enabled else '🔓 DISABLED'}")
    print(f"  Whitelisted IPs: {len(whitelist)}")
    for ip in whitelist:
        print(f"     ✅ {ip}")
    
    print(f"\n  Blacklisted IPs: {len(blacklist)}")
    for ip in blacklist:
        print(f"     🚫 {ip}")

def check_vault_secrets():
    """Check encrypted vault contents"""
    print_header("🔐 ENCRYPTED VAULT CONTENTS")
    
    vault_dir = Path('secure_vault')
    
    if not vault_dir.exists():
        print("  ⚠️  Vault not created")
        print("     Run: python SETUP_SECURITY.py")
        return
    
    master_key = vault_dir / '.master.key'
    if not master_key.exists():
        print("  ⚠️  Master key not found")
        return
    
    print(f"  🔒 Master Key: {master_key} (AES-256)")
    
    secrets = list(vault_dir.glob('*.enc'))
    print(f"  📦 Stored Secrets: {len(secrets)}")
    
    for secret in secrets:
        name = secret.stem
        size = secret.stat().st_size
        print(f"     🔒 {name:<30} ({size} bytes encrypted)")

def generate_security_score():
    """Calculate overall security score"""
    print_header("🏆 OVERALL SECURITY SCORE")
    
    score = 0
    max_score = 100
    
    checks = []
    
    # Check 1: Security files exist (10 points)
    if Path('ULTIMATE_SECURITY_SYSTEM.py').exists():
        score += 10
        checks.append(('✅', 'Security system installed', 10))
    else:
        checks.append(('❌', 'Security system NOT installed', 0))
    
    # Check 2: Vault exists (10 points)
    if Path('secure_vault').exists() and list(Path('secure_vault').glob('*.enc')):
        score += 10
        checks.append(('✅', 'Encrypted vault active', 10))
    else:
        checks.append(('❌', 'Vault NOT created', 0))
    
    # Check 3: Strong passwords (20 points)
    password = os.getenv('PASSWORD', '')
    master_pwd = os.getenv('SECURITY_MASTER_PASSWORD', '')
    
    pwd_score = 0
    if len(password) >= 12:
        pwd_score += 5
    if len(master_pwd) >= 20:
        pwd_score += 15
    
    score += pwd_score
    if pwd_score >= 15:
        checks.append(('✅', 'Strong passwords configured', pwd_score))
    else:
        checks.append(('⚠️', 'Weak passwords detected', pwd_score))
    
    # Check 4: Rate limiting (10 points)
    if os.getenv('RATE_LIMIT_ENABLED', '').lower() in ('true', '1'):
        score += 10
        checks.append(('✅', 'Rate limiting enabled', 10))
    else:
        checks.append(('⚠️', 'Rate limiting disabled', 0))
    
    # Check 5: File integrity (10 points)
    if Path('file_integrity.json').exists():
        score += 10
        checks.append(('✅', 'File integrity monitoring', 10))
    else:
        checks.append(('⚠️', 'File integrity NOT configured', 0))
    
    # Check 6: 2FA (15 points)
    if os.getenv('TWO_FACTOR_ENABLED', '').lower() in ('true', '1'):
        score += 15
        checks.append(('✅', 'Two-Factor Auth enabled', 15))
    else:
        checks.append(('⚠️', '2FA not enabled', 0))
    
    # Check 7: IP whitelist (10 points)
    if os.getenv('IP_WHITELIST_ENABLED', '').lower() in ('true', '1'):
        score += 10
        checks.append(('✅', 'IP whitelist active', 10))
    else:
        checks.append(('⚠️', 'IP whitelist disabled', 0))
    
    # Check 8: Security audit (10 points)
    if Path('security_audit_trail.jsonl').exists():
        score += 10
        checks.append(('✅', 'Security audit trail', 10))
    else:
        checks.append(('⚠️', 'Audit trail not active', 0))
    
    # Check 9: Credentials in vault (15 points)
    vault_secrets = len(list(Path('secure_vault').glob('*.enc'))) if Path('secure_vault').exists() else 0
    vault_score = min(15, vault_secrets * 3)
    score += vault_score
    if vault_score >= 12:
        checks.append(('✅', f'Credentials in vault ({vault_secrets})', vault_score))
    else:
        checks.append(('⚠️', f'Few credentials in vault ({vault_secrets})', vault_score))
    
    # Print breakdown
    print(f"\n  Security Checks:")
    for status, check, points in checks:
        print(f"     {status} {check:<40} +{points} points")
    
    # Calculate grade
    percentage = (score / max_score) * 100
    
    if percentage >= 90:
        grade = 'A+ EXCELLENT'
        color = '🟢'
    elif percentage >= 80:
        grade = 'A  VERY GOOD'
        color = '🟢'
    elif percentage >= 70:
        grade = 'B  GOOD'
        color = '🟡'
    elif percentage >= 60:
        grade = 'C  FAIR'
        color = '🟡'
    else:
        grade = 'D  NEEDS IMPROVEMENT'
        color = '🔴'
    
    print("\n" + "="*80)
    print(f"  {color} TOTAL SCORE: {score}/{max_score} ({percentage:.1f}%) - Grade: {grade}")
    print("="*80)
    
    # Recommendations
    if percentage < 90:
        print("\n  📋 RECOMMENDATIONS:")
        if not Path('secure_vault').exists():
            print("     1. Run: python SETUP_SECURITY.py")
        if len(password) < 12:
            print("     2. Change to strong password (12+ chars)")
        if os.getenv('TWO_FACTOR_ENABLED') != 'true':
            print("     3. Enable Two-Factor Authentication")
        if os.getenv('IP_WHITELIST_ENABLED') != 'true':
            print("     4. Enable IP whitelist (if from fixed location)")
        if vault_secrets < 5:
            print("     5. Move all credentials to encrypted vault")

def print_quick_actions():
    """Print quick action commands"""
    print_header("⚡ QUICK SECURITY ACTIONS")
    
    print("""
  🔧 SETUP:
     python SETUP_SECURITY.py                           # Run security wizard
     
  🔐 VAULT:
     python -c "from ULTIMATE_SECURITY_SYSTEM import *; \\
         vault = SecureVault(os.getenv('SECURITY_MASTER_PASSWORD')); \\
         vault.store_secret('API_KEY', 'your_key')"     # Store secret
     
  📁 FILE INTEGRITY:
     python -c "from ULTIMATE_SECURITY_SYSTEM import *; \\
         UltimateSecurityManager().file_monitor.baseline()"  # Create baseline
     
  📊 EXPORT REPORT:
     python -c "from ULTIMATE_SECURITY_SYSTEM import *; \\
         UltimateSecurityManager().export_security_report()"  # Export report
     
  🧪 TEST SECURITY:
     python ULTIMATE_SECURITY_SYSTEM.py                 # Run demo
    """)

def main():
    """Main dashboard"""
    print("\n" + "="*80)
    print("🔒 ELITE TRADING BOT - SECURITY STATUS DASHBOARD 🔒")
    print("="*80)
    print(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run all checks
    check_security_files()
    check_env_security()
    check_protected_credentials()
    check_password_strength()
    check_vault_secrets()
    check_file_integrity()
    check_ip_control()
    check_security_audit()
    generate_security_score()
    print_quick_actions()
    
    print("\n" + "="*80)
    print("📚 Documentation: SECURITY_SETUP_GUIDE.md")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Dashboard error: {e}")
        import traceback
        traceback.print_exc()
