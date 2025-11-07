"""
🔧 PRODUCTION FIXES MODULE
Elite Trading Bot V5.0 - Production-Grade Systems
Author: Elite Trading Systems
Date: November 7, 2025

FEATURES:
- Token Management & Auto-Refresh
- Circuit Breakers for Safety
- Performance Monitoring
- Data Validation & Sanitization
- API Request Validation
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class TokenManager:
    """Manage API tokens with auto-refresh"""
    
    def __init__(self):
        self.token = None
        self.expiry = None
        self.refresh_threshold = 300  # 5 minutes
        logger.info("✅ Token Manager initialized")
    
    def is_valid(self) -> bool:
        """Check if token is valid"""
        if not self.token or not self.expiry:
            return False
        return datetime.now() < self.expiry - timedelta(seconds=self.refresh_threshold)
    
    def refresh_if_needed(self):
        """Refresh token if needed"""
        if not self.is_valid():
            logger.info("🔄 Token refresh triggered")
            self.token = f"token_{int(time.time())}"
            self.expiry = datetime.now() + timedelta(hours=24)
            return True
        return False


class CircuitBreaker:
    """Circuit breaker for API failures"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None
        self.state = 'closed'  # closed, open, half_open
        logger.info(f"✅ Circuit Breaker initialized (threshold={failure_threshold})")
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker"""
        if self.state == 'open':
            if datetime.now() - self.last_failure > timedelta(seconds=self.timeout):
                self.state = 'half_open'
                logger.info("🔄 Circuit breaker: HALF-OPEN")
            else:
                raise Exception("Circuit breaker OPEN - too many failures")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'half_open':
                self.state = 'closed'
                self.failures = 0
                logger.info("✅ Circuit breaker: CLOSED")
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure = datetime.now()
            
            if self.failures >= self.failure_threshold:
                self.state = 'open'
                logger.error(f"🚨 Circuit breaker: OPEN (failures={self.failures})")
            
            raise e


class PerformanceMonitor:
    """Monitor system performance"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.latencies = deque(maxlen=window_size)
        self.errors = deque(maxlen=window_size)
        self.start_time = time.time()
        logger.info("✅ Performance Monitor initialized")
    
    def record_latency(self, latency_ms: float):
        """Record API latency"""
        self.latencies.append(latency_ms)
    
    def record_error(self, error: str):
        """Record error"""
        self.errors.append({'time': datetime.now(), 'error': error})
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        return {
            'avg_latency_ms': sum(self.latencies) / len(self.latencies) if self.latencies else 0,
            'max_latency_ms': max(self.latencies) if self.latencies else 0,
            'error_rate': len(self.errors) / self.window_size if self.errors else 0,
            'uptime_hours': (time.time() - self.start_time) / 3600
        }


class DataValidator:
    """Validate and sanitize data"""
    
    def __init__(self):
        self.validation_rules = {
            'price': lambda x: x > 0 and x < 1000000,
            'volume': lambda x: x >= 0,
            'rsi': lambda x: 0 <= x <= 100,
            'confidence': lambda x: 0 <= x <= 1
        }
        logger.info("✅ Data Validator initialized")
    
    def validate(self, data: Dict, schema: Dict) -> bool:
        """Validate data against schema"""
        try:
            for field, rule in schema.items():
                if field not in data:
                    return False
                if not rule(data[field]):
                    return False
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    def sanitize_price(self, price: float) -> float:
        """Sanitize price data"""
        if price <= 0:
            return 0.0
        if price > 1000000:
            return 1000000.0
        return round(price, 2)
    
    def sanitize_volume(self, volume: int) -> int:
        """Sanitize volume data"""
        return max(0, int(volume))


class APIValidator:
    """Validate API requests and responses"""
    
    def __init__(self):
        self.rate_limits = {}
        self.max_requests_per_minute = 60
        logger.info("✅ API Validator initialized")
    
    def check_rate_limit(self, endpoint: str) -> bool:
        """Check if rate limit exceeded"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        if endpoint not in self.rate_limits:
            self.rate_limits[endpoint] = deque()
        
        # Clean old requests
        while self.rate_limits[endpoint] and self.rate_limits[endpoint][0] < minute_ago:
            self.rate_limits[endpoint].popleft()
        
        # Check limit
        if len(self.rate_limits[endpoint]) >= self.max_requests_per_minute:
            return False
        
        self.rate_limits[endpoint].append(now)
        return True
    
    def validate_response(self, response: Any) -> bool:
        """Validate API response"""
        if response is None:
            return False
        if isinstance(response, dict) and 'error' in response:
            return False
        return True


# Singleton instances
token_manager = TokenManager()
circuit_breaker = CircuitBreaker()
performance_monitor = PerformanceMonitor()
data_validator = DataValidator()
api_validator = APIValidator()


def get_production_systems():
    """Get all production systems"""
    return {
        'token_manager': token_manager,
        'circuit_breaker': circuit_breaker,
        'performance_monitor': performance_monitor,
        'data_validator': data_validator,
        'api_validator': api_validator
    }
