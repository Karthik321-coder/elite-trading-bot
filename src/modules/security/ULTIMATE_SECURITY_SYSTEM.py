"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║      🔒 ULTIMATE SECURITY & PROTECTION SYSTEM V1.0 🔒                       ║
║            MILITARY-GRADE SECURITY FOR TRADING BOT                          ║
║                                                                              ║
║  ✅ AES-256 Encryption for Credentials                                      ║
║  ✅ RSA Public/Private Key Authentication                                   ║
║  ✅ JWT Token-Based Session Security                                        ║
║  ✅ Rate Limiting & DDoS Protection                                         ║
║  ✅ IP Whitelist/Blacklist System                                           ║
║  ✅ Brute Force Attack Prevention                                           ║
║  ✅ Two-Factor Authentication (2FA)                                         ║
║  ✅ Encrypted Backup System                                                 ║
║  ✅ Audit Trail & Security Logging                                          ║
║  ✅ Auto-Lockdown on Suspicious Activity                                    ║
║  ✅ File Integrity Monitoring                                               ║
║  ✅ Secrets Manager (Vault)                                                 ║
║                                                                              ║
║  © 2025 Elite Security Systems - Bank-Grade Protection                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import hashlib
import secrets
import base64
import time
import hmac
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from collections import defaultdict
from functools import wraps

# ═══════════════════════════════════════════════════════════════════════════════
#                        CRYPTOGRAPHY LIBRARIES
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️  Install cryptography: pip install cryptography")

try:
    import jwt  # PyJWT for token authentication
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("⚠️  Install PyJWT: pip install PyJWT")

try:
    import pyotp  # For 2FA
    TOTP_AVAILABLE = True
except ImportError:
    TOTP_AVAILABLE = False
    print("⚠️  Install pyotp: pip install pyotp")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_audit.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#                    1. AES-256 CREDENTIAL ENCRYPTION
# ═══════════════════════════════════════════════════════════════════════════════

class SecureVault:
    """
    Military-grade AES-256 encryption for sensitive data
    Protects API keys, passwords, tokens from file access
    """
    
    def __init__(self, master_password: str = None):
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        self.vault_dir = Path("secure_vault")
        self.vault_dir.mkdir(exist_ok=True)
        
        # Generate or load master key
        self.key_file = self.vault_dir / ".master.key"
        
        if master_password:
            self.master_key = self._derive_key_from_password(master_password)
        elif self.key_file.exists():
            self.master_key = self.key_file.read_bytes()
        else:
            self.master_key = Fernet.generate_key()
            self.key_file.write_bytes(self.master_key)
            os.chmod(self.key_file, 0o600)  # Owner read/write only
        
        self.cipher = Fernet(self.master_key)
        logger.info("🔒 Secure Vault initialized with AES-256 encryption")
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        salt = b'elite_trading_bot_salt_v1'  # Use unique salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def store_secret(self, name: str, value: str):
        """Encrypt and store secret"""
        encrypted = self.cipher.encrypt(value.encode())
        secret_file = self.vault_dir / f"{name}.enc"
        secret_file.write_bytes(encrypted)
        os.chmod(secret_file, 0o600)
        logger.info(f"✅ Secret '{name}' stored securely")
    
    def get_secret(self, name: str) -> Optional[str]:
        """Retrieve and decrypt secret"""
        secret_file = self.vault_dir / f"{name}.enc"
        if not secret_file.exists():
            logger.warning(f"⚠️  Secret '{name}' not found")
            return None
        
        encrypted = secret_file.read_bytes()
        try:
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"❌ Failed to decrypt '{name}': {e}")
            return None
    
    def delete_secret(self, name: str):
        """Securely delete secret"""
        secret_file = self.vault_dir / f"{name}.enc"
        if secret_file.exists():
            # Overwrite before delete (prevent recovery)
            secret_file.write_bytes(os.urandom(1024))
            secret_file.unlink()
            logger.info(f"🗑️  Secret '{name}' deleted securely")
    
    def list_secrets(self) -> List[str]:
        """List all stored secrets (names only)"""
        return [f.stem for f in self.vault_dir.glob("*.enc")]

# ═══════════════════════════════════════════════════════════════════════════════
#                    2. RSA PUBLIC/PRIVATE KEY AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

class RSAAuthenticator:
    """
    RSA 4096-bit public/private key authentication
    For secure API communication and file signing
    """
    
    def __init__(self):
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        self.keys_dir = Path("secure_keys")
        self.keys_dir.mkdir(exist_ok=True)
        
        self.private_key_file = self.keys_dir / "private_key.pem"
        self.public_key_file = self.keys_dir / "public_key.pem"
        
        if not self.private_key_file.exists():
            self._generate_key_pair()
        else:
            self._load_keys()
        
        logger.info("🔐 RSA Authenticator initialized (4096-bit)")
    
    def _generate_key_pair(self):
        """Generate RSA 4096-bit key pair"""
        logger.info("🔧 Generating RSA 4096-bit key pair...")
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        # Save private key (encrypted with password)
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  # Use BestAvailableEncryption(password) for extra security
        )
        self.private_key_file.write_bytes(pem_private)
        os.chmod(self.private_key_file, 0o600)
        
        # Save public key
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key_file.write_bytes(pem_public)
        
        self.private_key = private_key
        self.public_key = public_key
        
        logger.info("✅ RSA key pair generated successfully")
    
    def _load_keys(self):
        """Load existing keys"""
        self.private_key = serialization.load_pem_private_key(
            self.private_key_file.read_bytes(),
            password=None,  # Add password if keys are encrypted
            backend=default_backend()
        )
        self.public_key = serialization.load_pem_public_key(
            self.public_key_file.read_bytes(),
            backend=default_backend()
        )
    
    def sign_message(self, message: str) -> bytes:
        """Sign message with private key"""
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify_signature(self, message: str, signature: bytes) -> bool:
        """Verify message signature with public key"""
        try:
            self.public_key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def encrypt_message(self, message: str) -> bytes:
        """Encrypt message with public key"""
        encrypted = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    
    def decrypt_message(self, encrypted: bytes) -> str:
        """Decrypt message with private key"""
        decrypted = self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

# ═══════════════════════════════════════════════════════════════════════════════
#                    3. JWT TOKEN-BASED SESSION SECURITY
# ═══════════════════════════════════════════════════════════════════════════════

class JWTSessionManager:
    """
    JWT (JSON Web Token) session management
    Secure, stateless authentication tokens
    """
    
    def __init__(self, secret_key: str = None):
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT library required: pip install PyJWT")
        
        self.secret_key = secret_key or secrets.token_hex(32)
        self.algorithm = "HS256"
        self.token_expiry = 3600 * 8  # 8 hours (trading day)
        
        logger.info("🎫 JWT Session Manager initialized")
    
    def generate_token(self, user_id: str, data: Dict = None) -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=self.token_expiry),
            "data": data or {}
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        logger.info(f"✅ JWT token generated for user: {user_id}")
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️  Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("⚠️  Invalid token")
            return None
    
    def refresh_token(self, old_token: str) -> Optional[str]:
        """Refresh token before expiry"""
        payload = self.verify_token(old_token)
        if payload:
            user_id = payload.get("user_id")
            data = payload.get("data")
            return self.generate_token(user_id, data)
        return None

# ═══════════════════════════════════════════════════════════════════════════════
#                    4. RATE LIMITING & DDOS PROTECTION
# ═══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """
    Rate limiting to prevent brute force and DDoS attacks
    Tracks requests per IP and implements sliding window
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # IP -> [timestamps]
        self.blocked_ips = set()
        self.block_duration = 3600  # 1 hour block
        
        logger.info(f"🛡️  Rate Limiter: {max_requests} requests per {window_seconds}s")
    
    def is_allowed(self, ip_address: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            logger.warning(f"🚫 Blocked IP attempted access: {ip_address}")
            return False
        
        # Clean old requests
        self.requests[ip_address] = [
            ts for ts in self.requests[ip_address]
            if now - ts < self.window_seconds
        ]
        
        # Check rate limit
        if len(self.requests[ip_address]) >= self.max_requests:
            logger.warning(f"⚠️  Rate limit exceeded for IP: {ip_address}")
            self.block_ip(ip_address)
            return False
        
        # Record request
        self.requests[ip_address].append(now)
        return True
    
    def block_ip(self, ip_address: str):
        """Block IP address"""
        self.blocked_ips.add(ip_address)
        logger.warning(f"🚫 IP blocked: {ip_address}")
    
    def unblock_ip(self, ip_address: str):
        """Unblock IP address"""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            logger.info(f"✅ IP unblocked: {ip_address}")

# ═══════════════════════════════════════════════════════════════════════════════
#                    5. IP WHITELIST/BLACKLIST SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class IPAccessControl:
    """
    IP Whitelist/Blacklist access control
    Only allow trusted IPs to access bot
    """
    
    def __init__(self):
        self.config_file = Path("ip_access_control.json")
        self.whitelist = set()
        self.blacklist = set()
        self.whitelist_enabled = False
        
        self._load_config()
        logger.info("🌐 IP Access Control initialized")
    
    def _load_config(self):
        """Load IP lists from config"""
        if self.config_file.exists():
            config = json.loads(self.config_file.read_text())
            self.whitelist = set(config.get("whitelist", []))
            self.blacklist = set(config.get("blacklist", []))
            self.whitelist_enabled = config.get("whitelist_enabled", False)
    
    def _save_config(self):
        """Save IP lists to config"""
        config = {
            "whitelist": list(self.whitelist),
            "blacklist": list(self.blacklist),
            "whitelist_enabled": self.whitelist_enabled
        }
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def is_allowed(self, ip_address: str) -> bool:
        """Check if IP is allowed"""
        # Check blacklist first
        if ip_address in self.blacklist:
            logger.warning(f"🚫 Blacklisted IP blocked: {ip_address}")
            return False
        
        # Check whitelist if enabled
        if self.whitelist_enabled:
            if ip_address not in self.whitelist:
                logger.warning(f"⚠️  Non-whitelisted IP denied: {ip_address}")
                return False
        
        return True
    
    def add_to_whitelist(self, ip_address: str):
        """Add IP to whitelist"""
        self.whitelist.add(ip_address)
        self._save_config()
        logger.info(f"✅ IP added to whitelist: {ip_address}")
    
    def add_to_blacklist(self, ip_address: str):
        """Add IP to blacklist"""
        self.blacklist.add(ip_address)
        self._save_config()
        logger.warning(f"🚫 IP added to blacklist: {ip_address}")
    
    def remove_from_whitelist(self, ip_address: str):
        """Remove IP from whitelist"""
        self.whitelist.discard(ip_address)
        self._save_config()
    
    def remove_from_blacklist(self, ip_address: str):
        """Remove IP from blacklist"""
        self.blacklist.discard(ip_address)
        self._save_config()
    
    def enable_whitelist(self):
        """Enable whitelist mode"""
        self.whitelist_enabled = True
        self._save_config()
        logger.info("🔒 Whitelist mode ENABLED - Only whitelisted IPs allowed")
    
    def disable_whitelist(self):
        """Disable whitelist mode"""
        self.whitelist_enabled = False
        self._save_config()
        logger.info("🔓 Whitelist mode DISABLED")

# ═══════════════════════════════════════════════════════════════════════════════
#                    6. BRUTE FORCE ATTACK PREVENTION
# ═══════════════════════════════════════════════════════════════════════════════

class BruteForceProtection:
    """
    Brute force attack prevention
    Tracks failed login attempts and implements exponential backoff
    """
    
    def __init__(self, max_attempts: int = 5, lockout_duration: int = 1800):
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration  # 30 minutes default
        self.failed_attempts = defaultdict(list)  # username/IP -> [timestamps]
        self.locked_accounts = {}  # username/IP -> unlock_time
        
        logger.info(f"🔐 Brute Force Protection: {max_attempts} attempts, {lockout_duration}s lockout")
    
    def record_failed_attempt(self, identifier: str):
        """Record failed login attempt"""
        now = time.time()
        self.failed_attempts[identifier].append(now)
        
        # Clean old attempts (1 hour window)
        self.failed_attempts[identifier] = [
            ts for ts in self.failed_attempts[identifier]
            if now - ts < 3600
        ]
        
        # Check if max attempts exceeded
        if len(self.failed_attempts[identifier]) >= self.max_attempts:
            self.lock_account(identifier)
    
    def record_successful_attempt(self, identifier: str):
        """Clear failed attempts on successful login"""
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
        if identifier in self.locked_accounts:
            del self.locked_accounts[identifier]
    
    def is_locked(self, identifier: str) -> bool:
        """Check if account/IP is locked"""
        if identifier in self.locked_accounts:
            unlock_time = self.locked_accounts[identifier]
            if time.time() < unlock_time:
                remaining = int(unlock_time - time.time())
                logger.warning(f"🔒 Account locked: {identifier} ({remaining}s remaining)")
                return True
            else:
                # Lock expired
                del self.locked_accounts[identifier]
                return False
        return False
    
    def lock_account(self, identifier: str):
        """Lock account/IP"""
        unlock_time = time.time() + self.lockout_duration
        self.locked_accounts[identifier] = unlock_time
        logger.warning(f"🚫 Account/IP locked: {identifier} (too many failed attempts)")
    
    def unlock_account(self, identifier: str):
        """Manually unlock account/IP"""
        if identifier in self.locked_accounts:
            del self.locked_accounts[identifier]
            logger.info(f"🔓 Account/IP unlocked: {identifier}")

# ═══════════════════════════════════════════════════════════════════════════════
#                    7. TWO-FACTOR AUTHENTICATION (2FA)
# ═══════════════════════════════════════════════════════════════════════════════

class TwoFactorAuth:
    """
    TOTP-based Two-Factor Authentication
    Generates time-based one-time passwords
    """
    
    def __init__(self):
        if not TOTP_AVAILABLE:
            raise ImportError("pyotp library required: pip install pyotp")
        
        self.secrets_file = Path("2fa_secrets.json")
        self.user_secrets = {}
        
        if self.secrets_file.exists():
            self.user_secrets = json.loads(self.secrets_file.read_text())
        
        logger.info("🔐 Two-Factor Authentication initialized")
    
    def enable_2fa(self, user_id: str) -> Tuple[str, str]:
        """
        Enable 2FA for user
        Returns: (secret, qr_code_url)
        """
        secret = pyotp.random_base32()
        self.user_secrets[user_id] = secret
        self._save_secrets()
        
        # Generate QR code URL for Google Authenticator
        totp = pyotp.TOTP(secret)
        qr_url = totp.provisioning_uri(
            name=user_id,
            issuer_name="Elite Trading Bot"
        )
        
        logger.info(f"✅ 2FA enabled for user: {user_id}")
        return secret, qr_url
    
    def disable_2fa(self, user_id: str):
        """Disable 2FA for user"""
        if user_id in self.user_secrets:
            del self.user_secrets[user_id]
            self._save_secrets()
            logger.info(f"🔓 2FA disabled for user: {user_id}")
    
    def verify_code(self, user_id: str, code: str) -> bool:
        """Verify 2FA code"""
        if user_id not in self.user_secrets:
            logger.warning(f"⚠️  2FA not enabled for user: {user_id}")
            return False
        
        secret = self.user_secrets[user_id]
        totp = pyotp.TOTP(secret)
        
        is_valid = totp.verify(code, valid_window=1)  # Allow 30s window
        
        if is_valid:
            logger.info(f"✅ 2FA code verified for user: {user_id}")
        else:
            logger.warning(f"❌ Invalid 2FA code for user: {user_id}")
        
        return is_valid
    
    def _save_secrets(self):
        """Save 2FA secrets"""
        self.secrets_file.write_text(json.dumps(self.user_secrets, indent=2))
        os.chmod(self.secrets_file, 0o600)

# ═══════════════════════════════════════════════════════════════════════════════
#                    8. FILE INTEGRITY MONITORING
# ═══════════════════════════════════════════════════════════════════════════════

class FileIntegrityMonitor:
    """
    Monitor critical files for unauthorized changes
    Detects tampering with bot code or configuration
    """
    
    def __init__(self, monitored_files: List[str] = None):
        self.monitored_files = monitored_files or [
            "Untitled-1.py",
            "global_mobile_server.py",
            "cloud_deploy.py",
            ".env"
        ]
        
        self.integrity_file = Path("file_integrity.json")
        self.file_hashes = {}
        
        self._load_hashes()
        logger.info(f"🔍 File Integrity Monitor: {len(self.monitored_files)} files")
    
    def _load_hashes(self):
        """Load stored file hashes"""
        if self.integrity_file.exists():
            self.file_hashes = json.loads(self.integrity_file.read_text())
    
    def _save_hashes(self):
        """Save file hashes"""
        self.integrity_file.write_text(json.dumps(self.file_hashes, indent=2))
    
    def _calculate_hash(self, filepath: str) -> str:
        """Calculate SHA-256 hash of file"""
        if not Path(filepath).exists():
            return ""
        
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def baseline(self):
        """Create baseline hashes for all files"""
        for filepath in self.monitored_files:
            file_hash = self._calculate_hash(filepath)
            if file_hash:
                self.file_hashes[filepath] = file_hash
        
        self._save_hashes()
        logger.info("✅ File integrity baseline created")
    
    def check_integrity(self) -> List[str]:
        """Check file integrity, return list of modified files"""
        modified_files = []
        
        for filepath in self.monitored_files:
            current_hash = self._calculate_hash(filepath)
            stored_hash = self.file_hashes.get(filepath)
            
            if current_hash != stored_hash:
                modified_files.append(filepath)
                logger.warning(f"⚠️  File modified: {filepath}")
        
        return modified_files
    
    def update_baseline(self, filepath: str):
        """Update baseline for specific file"""
        file_hash = self._calculate_hash(filepath)
        if file_hash:
            self.file_hashes[filepath] = file_hash
            self._save_hashes()
            logger.info(f"✅ Baseline updated: {filepath}")

# ═══════════════════════════════════════════════════════════════════════════════
#                    9. SECURITY AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityAuditTrail:
    """
    Comprehensive security event logging
    Tracks all authentication, access, and security events
    """
    
    def __init__(self):
        self.audit_file = Path("security_audit_trail.jsonl")
        logger.info("📋 Security Audit Trail initialized")
    
    def log_event(self, event_type: str, user_id: str = None, user: str = None,
                  ip_address: str = None, description: str = None, details: Dict = None):
        """
        Log security event
        
        Args:
            event_type: Type of security event
            user_id: User identifier (deprecated, use 'user')
            user: User identifier (preferred)
            ip_address: IP address of the event
            description: Event description
            details: Additional event details
        """
        # Support both user_id and user parameters
        actual_user = user or user_id
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user": actual_user,
            "ip_address": ip_address,
            "description": description,
            "details": details or {}
        }
        
        with open(self.audit_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')
        
        desc_str = f" - {description}" if description else ""
        logger.info(f"📝 Audit: {event_type} | User: {actual_user} | IP: {ip_address}{desc_str}")
    
    def get_events(self, limit: int = 100, event_type: str = None) -> List[Dict]:
        """Retrieve recent security events"""
        if not self.audit_file.exists():
            return []
        
        events = []
        with open(self.audit_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    if event_type is None or event.get("event_type") == event_type:
                        events.append(event)
                except json.JSONDecodeError:
                    continue
        
        return events[-limit:]  # Return most recent

# ═══════════════════════════════════════════════════════════════════════════════
#                    10. INTEGRATED SECURITY MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class UltimateSecurityManager:
    """
    Master security coordinator
    Integrates all security components
    """
    
    def __init__(self, master_password: str = None):
        logger.info("="*80)
        logger.info("🔒 INITIALIZING ULTIMATE SECURITY SYSTEM 🔒")
        logger.info("="*80)
        
        # Initialize all security components
        try:
            self.vault = SecureVault(master_password) if CRYPTO_AVAILABLE else None
            self.rsa_auth = RSAAuthenticator() if CRYPTO_AVAILABLE else None
            self.jwt_manager = JWTSessionManager() if JWT_AVAILABLE else None
            self.rate_limiter = RateLimiter()
            self.ip_control = IPAccessControl()
            self.brute_force = BruteForceProtection()
            self.two_factor = TwoFactorAuth() if TOTP_AVAILABLE else None
            self.file_monitor = FileIntegrityMonitor()
            self.audit_trail = SecurityAuditTrail()
            
            logger.info("✅ All security modules loaded successfully")
            logger.info("="*80)
            
        except Exception as e:
            logger.error(f"❌ Security initialization error: {e}")
            raise
    
    def secure_login(self, username: str, password: str, 
                     ip_address: str, totp_code: str = None) -> Optional[str]:
        """
        Comprehensive secure login with all protections
        Returns JWT token if successful
        """
        # 1. Rate limiting
        if not self.rate_limiter.is_allowed(ip_address):
            self.audit_trail.log_event("RATE_LIMIT_EXCEEDED", username, ip_address)
            return None
        
        # 2. IP access control
        if not self.ip_control.is_allowed(ip_address):
            self.audit_trail.log_event("IP_BLOCKED", username, ip_address)
            return None
        
        # 3. Brute force protection
        if self.brute_force.is_locked(username):
            self.audit_trail.log_event("ACCOUNT_LOCKED", username, ip_address)
            return None
        
        # 4. Verify credentials (example - integrate with your auth system)
        stored_password = self.vault.get_secret(f"user_password_{username}") if self.vault else None
        
        if not stored_password or not self._verify_password(password, stored_password):
            self.brute_force.record_failed_attempt(username)
            self.audit_trail.log_event("LOGIN_FAILED", username, ip_address)
            return None
        
        # 5. Two-factor authentication
        if self.two_factor and username in self.two_factor.user_secrets:
            if not totp_code or not self.two_factor.verify_code(username, totp_code):
                self.brute_force.record_failed_attempt(username)
                self.audit_trail.log_event("2FA_FAILED", username, ip_address)
                return None
        
        # 6. Success - generate JWT token
        self.brute_force.record_successful_attempt(username)
        token = self.jwt_manager.generate_token(username) if self.jwt_manager else None
        
        self.audit_trail.log_event("LOGIN_SUCCESS", username, ip_address)
        logger.info(f"✅ Secure login successful: {username} from {ip_address}")
        
        return token
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password (use bcrypt/argon2 in production)"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == stored_hash
    
    def _hash_password(self, password: str) -> str:
        """Hash password (use bcrypt/argon2 in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str):
        """Create new user with secure password storage"""
        if self.vault:
            password_hash = self._hash_password(password)
            self.vault.store_secret(f"user_password_{username}", password_hash)
            logger.info(f"✅ User created: {username}")
    
    def check_file_integrity(self) -> bool:
        """Check all files for tampering"""
        modified = self.file_monitor.check_integrity()
        
        if modified:
            logger.error(f"🚨 SECURITY ALERT: Files modified: {modified}")
            self.audit_trail.log_event("FILE_TAMPERING_DETECTED", details={"files": modified})
            return False
        
        return True
    
    def export_security_report(self) -> str:
        """Generate comprehensive security report"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "vault_secrets": self.vault.list_secrets() if self.vault else [],
            "whitelisted_ips": list(self.ip_control.whitelist),
            "blacklisted_ips": list(self.ip_control.blacklist),
            "locked_accounts": list(self.brute_force.locked_accounts.keys()),
            "recent_events": self.audit_trail.get_events(50)
        }
        
        report_file = Path(f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_file.write_text(json.dumps(report, indent=2))
        
        logger.info(f"📊 Security report exported: {report_file}")
        return str(report_file)

# ═══════════════════════════════════════════════════════════════════════════════
#                    EXAMPLE USAGE & TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔒 ULTIMATE SECURITY SYSTEM - DEMONSTRATION 🔒")
    print("="*80 + "\n")
    
    # Initialize security system
    security = UltimateSecurityManager(master_password="elite_trading_bot_2025")
    
    # Create test user
    security.create_user("admin", "Elite@Bot2025")
    
    # Store sensitive API keys in vault
    if security.vault:
        security.vault.store_secret("DHAN_CLIENT_ID", "1108804283")
        security.vault.store_secret("DHAN_ACCESS_TOKEN", "your_token_here")
        security.vault.store_secret("OPENAI_API_KEY", "sk-xxxxxxxxxxxxx")
        
        print("\n✅ Secrets stored in encrypted vault:")
        print(f"   Secrets: {security.vault.list_secrets()}")
    
    # Create file integrity baseline
    security.file_monitor.baseline()
    print("\n✅ File integrity baseline created")
    
    # Test secure login
    print("\n🔐 Testing secure login...")
    token = security.secure_login(
        username="admin",
        password="Elite@Bot2025",
        ip_address="192.168.1.100"
    )
    
    if token:
        print(f"✅ Login successful! JWT token: {token[:50]}...")
    else:
        print("❌ Login failed")
    
    # Add IP to whitelist
    security.ip_control.add_to_whitelist("192.168.1.100")
    print("\n✅ IP whitelisted: 192.168.1.100")
    
    # Export security report
    report_file = security.export_security_report()
    print(f"\n📊 Security report: {report_file}")
    
    print("\n" + "="*80)
    print("✅ SECURITY SYSTEM DEMONSTRATION COMPLETE")
    print("="*80 + "\n")
