"""
📊 MONITORING DASHBOARD MODULE
Elite Trading Bot V5.0 - Real-Time Monitoring
Author: Elite Trading Systems
Date: November 7, 2025

FEATURES:
- Performance Dashboard
- Alert System
- Auto-Restart Mechanism
- Health Monitoring
"""

import logging
import time
import psutil
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class PerformanceDashboard:
    """Real-time performance monitoring dashboard"""
    
    def __init__(self):
        self.metrics = {
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'pnl': 0.0,
            'runtime': 0
        }
        self.start_time = time.time()
        logger.info("✅ Performance Dashboard initialized")
    
    def update_trade(self, profit: float):
        """Update trade metrics"""
        self.metrics['trades'] += 1
        self.metrics['pnl'] += profit
        
        if profit > 0:
            self.metrics['wins'] += 1
        else:
            self.metrics['losses'] += 1
    
    def get_dashboard(self) -> Dict:
        """Get dashboard data"""
        runtime = time.time() - self.start_time
        win_rate = (self.metrics['wins'] / self.metrics['trades'] * 100) if self.metrics['trades'] > 0 else 0
        
        return {
            'total_trades': self.metrics['trades'],
            'win_rate': win_rate,
            'total_pnl': self.metrics['pnl'],
            'runtime_hours': runtime / 3600,
            'trades_per_hour': self.metrics['trades'] / (runtime / 3600) if runtime > 0 else 0
        }
    
    def print_dashboard(self):
        """Print dashboard to console"""
        data = self.get_dashboard()
        logger.info("=" * 60)
        logger.info("📊 PERFORMANCE DASHBOARD")
        logger.info("=" * 60)
        logger.info(f"Total Trades: {data['total_trades']}")
        logger.info(f"Win Rate: {data['win_rate']:.1f}%")
        logger.info(f"Total P&L: Rs.{data['total_pnl']:.2f}")
        logger.info(f"Runtime: {data['runtime_hours']:.2f} hours")
        logger.info(f"Trades/Hour: {data['trades_per_hour']:.2f}")
        logger.info("=" * 60)


class AlertSystem:
    """Alert system for critical events"""
    
    def __init__(self):
        self.alerts = deque(maxlen=100)
        self.alert_levels = ['INFO', 'WARNING', 'CRITICAL']
        logger.info("✅ Alert System initialized")
    
    def send_alert(self, level: str, message: str):
        """Send alert"""
        alert = {
            'time': datetime.now(),
            'level': level,
            'message': message
        }
        self.alerts.append(alert)
        
        # Log based on severity
        if level == 'CRITICAL':
            logger.critical(f"🚨 ALERT: {message}")
        elif level == 'WARNING':
            logger.warning(f"⚠️ ALERT: {message}")
        else:
            logger.info(f"ℹ️ ALERT: {message}")
    
    def get_recent_alerts(self, count: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return list(self.alerts)[-count:]
    
    def check_thresholds(self, metrics: Dict):
        """Check if metrics exceed thresholds"""
        # Check drawdown
        if metrics.get('drawdown', 0) > 0.08:
            self.send_alert('CRITICAL', f"Drawdown exceeded 8%: {metrics['drawdown']:.1%}")
        
        # Check win rate
        if metrics.get('win_rate', 100) < 40:
            self.send_alert('WARNING', f"Win rate below 40%: {metrics['win_rate']:.1f}%")


class AutoRestart:
    """Auto-restart mechanism for error recovery"""
    
    def __init__(self, max_restarts: int = 3, restart_window: int = 3600):
        self.max_restarts = max_restarts
        self.restart_window = restart_window
        self.restarts = deque()
        logger.info(f"✅ Auto-Restart initialized (max={max_restarts} per hour)")
    
    def can_restart(self) -> bool:
        """Check if restart is allowed"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.restart_window)
        
        # Clean old restarts
        while self.restarts and self.restarts[0] < window_start:
            self.restarts.popleft()
        
        return len(self.restarts) < self.max_restarts
    
    def record_restart(self):
        """Record a restart"""
        self.restarts.append(datetime.now())
        logger.info(f"🔄 Restart recorded ({len(self.restarts)}/{self.max_restarts})")
    
    def attempt_restart(self, error: Exception) -> bool:
        """Attempt to restart after error"""
        if self.can_restart():
            logger.error(f"💥 Error: {error}")
            logger.info("🔄 Attempting auto-restart...")
            self.record_restart()
            time.sleep(5)  # Cooldown
            return True
        else:
            logger.critical("🚨 Max restarts exceeded - manual intervention required")
            return False


class HealthMonitor:
    """Monitor system health"""
    
    def __init__(self):
        self.last_check = datetime.now()
        self.check_interval = 60  # seconds
        logger.info("✅ Health Monitor initialized")
    
    def check_health(self) -> Dict:
        """Check system health"""
        health = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'status': 'healthy'
        }
        
        # Determine overall health
        if health['cpu_percent'] > 90 or health['memory_percent'] > 90:
            health['status'] = 'warning'
        if health['cpu_percent'] > 95 or health['memory_percent'] > 95:
            health['status'] = 'critical'
        
        self.last_check = datetime.now()
        return health
    
    def print_health(self):
        """Print health status"""
        health = self.check_health()
        logger.info(f"💚 System Health: {health['status'].upper()}")
        logger.info(f"   CPU: {health['cpu_percent']:.1f}%")
        logger.info(f"   Memory: {health['memory_percent']:.1f}%")
        logger.info(f"   Disk: {health['disk_percent']:.1f}%")


# Singleton instances
performance_dashboard = PerformanceDashboard()
alert_system = AlertSystem()
auto_restart = AutoRestart()
health_monitor = HealthMonitor()


def get_monitoring_systems():
    """Get all monitoring systems"""
    return {
        'dashboard': performance_dashboard,
        'alerts': alert_system,
        'auto_restart': auto_restart,
        'health': health_monitor
    }
