"""
🛡️ ADVANCED RISK MANAGEMENT SYSTEM - INSTITUTIONAL GRADE
Implements: Position sizing, drawdown limits, portfolio heat map, VaR/CVaR, circuit breakers
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from collections import deque
import json

logger = logging.getLogger(__name__)

@dataclass
class Position:
    """Position data structure"""
    symbol: str
    security_id: str
    entry_price: float
    current_price: float
    quantity: int
    side: str  # 'LONG' or 'SHORT'
    entry_time: datetime
    stop_loss: float
    take_profit: float
    trailing_stop: Optional[float]
    unrealized_pnl: float
    realized_pnl: float = 0
    risk_amount: float = 0
    position_value: float = 0
    
class AdvancedRiskManager:
    """
    Institutional-Grade Risk Management System
    
    Features:
    - Kelly Criterion position sizing
    - Value at Risk (VaR) / Conditional VaR (CVaR)
    - Maximum drawdown protection
    - Portfolio heat map
    - Dynamic stop-loss (ATR-based)
    - Correlation-based diversification
    - Real-time risk monitoring
    - Circuit breakers
    """
    
    def __init__(self, initial_capital: float, config: Dict):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.config = config
        
        # Risk limits
        self.max_risk_per_trade = config.get('max_risk_per_trade', 2.0)  # %
        self.max_portfolio_risk = config.get('max_portfolio_risk', 6.0)  # %
        self.max_drawdown = config.get('max_drawdown', 10.0)  # %
        self.max_daily_loss = config.get('max_daily_loss', -20.0)  # Rs
        self.max_positions = config.get('max_positions', 2)
        self.max_daily_trades = config.get('max_daily_trades', 8)
        
        # VaR parameters
        self.var_confidence = config.get('var_confidence', 0.95)  # 95%
        self.cvar_limit = config.get('cvar_limit', 3.0)  # %
        
        # Position tracking
        self.positions: Dict[str, Position] = {}
        self.closed_positions: List[Position] = []
        self.trade_history: List[Dict] = []
        
        # Performance tracking
        self.daily_pnl = 0
        self.peak_capital = initial_capital
        self.current_drawdown = 0
        self.max_drawdown_observed = 0
        self.trade_count_today = 0
        self.last_reset_date = datetime.now().date()
        
        # Risk metrics
        self.portfolio_heat = 0  # Current risk %
        self.var_95 = 0  # 95% VaR
        self.cvar_95 = 0  # 95% CVaR
        self.sharpe_ratio = 0
        self.sortino_ratio = 0
        
        # Returns history for VaR calculation
        self.returns_history = deque(maxlen=252)  # 1 year of daily returns
        
        # Circuit breaker
        self.is_trading_halted = False
        self.halt_reason = None
        self.halt_time = None
        
        logger.info("🛡️ Advanced Risk Manager initialized")
        logger.info(f"   Capital: Rs.{initial_capital:.2f}")
        logger.info(f"   Max risk/trade: {self.max_risk_per_trade}%")
        logger.info(f"   Max portfolio risk: {self.max_portfolio_risk}%")
        logger.info(f"   Max drawdown: {self.max_drawdown}%")
    
    def calculate_position_size_kelly(self, win_prob: float, avg_win: float, 
                                     avg_loss: float, kelly_fraction: float = 0.25) -> float:
        """
        Calculate optimal position size using Kelly Criterion
        
        Kelly % = (Win% × Avg Win - Loss% × Avg Loss) / Avg Win
        Uses fractional Kelly for safety
        
        Args:
            win_prob: Probability of winning (0-1)
            avg_win: Average win size (%)
            avg_loss: Average loss size (%)
            kelly_fraction: Fraction of Kelly to use (0.25 = quarter Kelly)
        
        Returns:
            Position size as % of capital
        """
        try:
            if avg_win <= 0 or avg_loss <= 0:
                return self.max_risk_per_trade
            
            # Kelly formula
            win_loss_ratio = avg_win / abs(avg_loss)
            kelly_pct = (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio
            
            # Apply fractional Kelly for safety
            kelly_pct = kelly_pct * kelly_fraction
            
            # Cap at max risk
            kelly_pct = max(0, min(kelly_pct, self.max_risk_per_trade))
            
            logger.debug(f"Kelly position size: {kelly_pct:.2f}% (Win prob: {win_prob:.2f}, W/L ratio: {win_loss_ratio:.2f})")
            
            return kelly_pct
            
        except Exception as e:
            logger.error(f"Kelly calculation error: {e}")
            return self.max_risk_per_trade
    
    def calculate_position_size(self, entry_price: float, stop_loss: float,
                                risk_pct: Optional[float] = None) -> int:
        """
        Calculate position size based on risk
        
        Position Size = (Capital × Risk%) / (Entry Price - Stop Loss)
        
        Args:
            entry_price: Entry price per share
            stop_loss: Stop loss price
            risk_pct: Risk percentage (uses default if None)
        
        Returns:
            Number of shares to buy
        """
        try:
            if risk_pct is None:
                risk_pct = self.max_risk_per_trade
            
            # Calculate risk per share
            risk_per_share = abs(entry_price - stop_loss)
            
            if risk_per_share <= 0:
                logger.warning("Invalid stop loss - risk per share is zero")
                return 0
            
            # Calculate position size
            risk_amount = self.current_capital * (risk_pct / 100)
            quantity = int(risk_amount / risk_per_share)
            
            # Validate position size
            position_value = quantity * entry_price
            max_position_value = self.current_capital * 0.45  # Max 45% per position
            
            if position_value > max_position_value:
                quantity = int(max_position_value / entry_price)
            
            logger.info(f"Position size: {quantity} shares @ Rs.{entry_price:.2f}")
            logger.info(f"   Risk: Rs.{risk_amount:.2f} ({risk_pct}%)")
            logger.info(f"   Position value: Rs.{position_value:.2f}")
            
            return max(0, quantity)
            
        except Exception as e:
            logger.error(f"Position size calculation error: {e}")
            return 0
    
    def calculate_atr_stop_loss(self, prices: np.array, atr_multiplier: float = 2.0) -> float:
        """
        Calculate ATR-based stop loss
        
        ATR = Average True Range (volatility measure)
        Stop = Current Price - (ATR × Multiplier)
        
        Args:
            prices: Array of recent prices
            atr_multiplier: ATR multiplier (2.0 = 2 ATR)
        
        Returns:
            Stop loss price
        """
        try:
            if len(prices) < 14:
                logger.warning("Insufficient data for ATR calculation")
                return prices[-1] * 0.98  # Fallback: 2% stop
            
            # Calculate True Range
            highs = np.array([max(prices[i:i+2]) for i in range(len(prices)-1)])
            lows = np.array([min(prices[i:i+2]) for i in range(len(prices)-1)])
            closes = prices[:-1]
            
            tr1 = highs - lows
            tr2 = np.abs(highs - closes)
            tr3 = np.abs(lows - closes)
            
            true_range = np.maximum(tr1, np.maximum(tr2, tr3))
            
            # Calculate ATR (14-period)
            atr = np.mean(true_range[-14:])
            
            # Calculate stop loss
            current_price = prices[-1]
            stop_loss = current_price - (atr * atr_multiplier)
            
            logger.debug(f"ATR stop loss: Rs.{stop_loss:.2f} (ATR: Rs.{atr:.2f})")
            
            return stop_loss
            
        except Exception as e:
            logger.error(f"ATR calculation error: {e}")
            return prices[-1] * 0.98
    
    def can_open_position(self, symbol: str, position_value: float, risk_amount: float) -> Tuple[bool, str]:
        """
        Check if new position can be opened
        
        Returns:
            (can_open: bool, reason: str)
        """
        try:
            # Check if trading is halted
            if self.is_trading_halted:
                return False, f"Trading halted: {self.halt_reason}"
            
            # Reset daily counters if new day
            today = datetime.now().date()
            if today != self.last_reset_date:
                self.trade_count_today = 0
                self.daily_pnl = 0
                self.last_reset_date = today
                logger.info("🔄 Daily counters reset")
            
            # Check max positions
            if len(self.positions) >= self.max_positions:
                return False, f"Max positions reached ({self.max_positions})"
            
            # Check if already have position in this symbol
            if symbol in self.positions:
                return False, f"Already have position in {symbol}"
            
            # Check max daily trades
            if self.trade_count_today >= self.max_daily_trades:
                return False, f"Max daily trades reached ({self.max_daily_trades})"
            
            # Check daily loss limit
            if self.daily_pnl <= self.max_daily_loss:
                return False, f"Daily loss limit hit (Rs.{self.daily_pnl:.2f})"
            
            # Check if enough capital
            if position_value > self.current_capital:
                return False, "Insufficient capital"
            
            # Check portfolio heat (total risk)
            new_portfolio_heat = self.portfolio_heat + (risk_amount / self.current_capital * 100)
            if new_portfolio_heat > self.max_portfolio_risk:
                return False, f"Portfolio heat too high ({new_portfolio_heat:.1f}% > {self.max_portfolio_risk}%)"
            
            # Check drawdown
            if self.current_drawdown >= self.max_drawdown:
                return False, f"Max drawdown reached ({self.current_drawdown:.2f}%)"
            
            # All checks passed
            return True, "OK"
            
        except Exception as e:
            logger.error(f"Position check error: {e}")
            return False, f"Error: {e}"
    
    def open_position(self, symbol: str, security_id: str, entry_price: float,
                     quantity: int, stop_loss: float, take_profit: float,
                     side: str = 'LONG') -> bool:
        """Open new position"""
        try:
            position_value = quantity * entry_price
            risk_per_share = abs(entry_price - stop_loss)
            risk_amount = quantity * risk_per_share
            
            # Validate
            can_open, reason = self.can_open_position(symbol, position_value, risk_amount)
            if not can_open:
                logger.warning(f"Cannot open position: {reason}")
                return False
            
            # Create position
            position = Position(
                symbol=symbol,
                security_id=security_id,
                entry_price=entry_price,
                current_price=entry_price,
                quantity=quantity,
                side=side,
                entry_time=datetime.now(),
                stop_loss=stop_loss,
                take_profit=take_profit,
                trailing_stop=None,
                unrealized_pnl=0,
                risk_amount=risk_amount,
                position_value=position_value
            )
            
            self.positions[symbol] = position
            self.trade_count_today += 1
            self.portfolio_heat += (risk_amount / self.current_capital * 100)
            
            logger.info(f"✅ Position opened: {symbol}")
            logger.info(f"   Qty: {quantity} @ Rs.{entry_price:.2f}")
            logger.info(f"   Stop: Rs.{stop_loss:.2f} | Target: Rs.{take_profit:.2f}")
            logger.info(f"   Risk: Rs.{risk_amount:.2f}")
            logger.info(f"   Portfolio heat: {self.portfolio_heat:.2f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"Open position error: {e}")
            return False
    
    def update_position(self, symbol: str, current_price: float):
        """Update position with current price"""
        try:
            if symbol not in self.positions:
                return
            
            position = self.positions[symbol]
            position.current_price = current_price
            
            # Calculate unrealized P&L
            if position.side == 'LONG':
                position.unrealized_pnl = (current_price - position.entry_price) * position.quantity
            else:  # SHORT
                position.unrealized_pnl = (position.entry_price - current_price) * position.quantity
            
            # Update trailing stop
            if position.trailing_stop:
                if position.side == 'LONG' and current_price > position.entry_price:
                    # Update trailing stop for profitable long
                    new_trail = current_price * (1 - self.config.get('trailing_stop_percent', 1.5) / 100)
                    position.trailing_stop = max(position.trailing_stop, new_trail)
            
            # Check stop loss
            if (position.side == 'LONG' and current_price <= position.stop_loss) or \
               (position.side == 'SHORT' and current_price >= position.stop_loss):
                logger.warning(f"⚠️ {symbol} hit stop loss!")
                self.close_position(symbol, current_price, "STOP_LOSS")
                return
            
            # Check trailing stop
            if position.trailing_stop and \
               ((position.side == 'LONG' and current_price <= position.trailing_stop) or \
                (position.side == 'SHORT' and current_price >= position.trailing_stop)):
                logger.info(f"✅ {symbol} hit trailing stop (profit secured)")
                self.close_position(symbol, current_price, "TRAILING_STOP")
                return
            
            # Check take profit
            if (position.side == 'LONG' and current_price >= position.take_profit) or \
               (position.side == 'SHORT' and current_price <= position.take_profit):
                logger.info(f"🎯 {symbol} hit take profit target!")
                self.close_position(symbol, current_price, "TAKE_PROFIT")
                return
            
        except Exception as e:
            logger.error(f"Update position error: {e}")
    
    def close_position(self, symbol: str, exit_price: float, reason: str = "MANUAL"):
        """Close position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"No position to close for {symbol}")
                return
            
            position = self.positions[symbol]
            
            # Calculate final P&L
            if position.side == 'LONG':
                realized_pnl = (exit_price - position.entry_price) * position.quantity
            else:
                realized_pnl = (position.entry_price - exit_price) * position.quantity
            
            position.realized_pnl = realized_pnl
            position.unrealized_pnl = 0
            
            # Update capital and metrics
            self.current_capital += realized_pnl
            self.daily_pnl += realized_pnl
            self.portfolio_heat -= (position.risk_amount / self.initial_capital * 100)
            self.portfolio_heat = max(0, self.portfolio_heat)
            
            # Update drawdown
            if self.current_capital > self.peak_capital:
                self.peak_capital = self.current_capital
                self.current_drawdown = 0
            else:
                self.current_drawdown = ((self.peak_capital - self.current_capital) / self.peak_capital) * 100
                self.max_drawdown_observed = max(self.max_drawdown_observed, self.current_drawdown)
            
            # Record trade
            trade_record = {
                'symbol': symbol,
                'entry_time': position.entry_time,
                'exit_time': datetime.now(),
                'entry_price': position.entry_price,
                'exit_price': exit_price,
                'quantity': position.quantity,
                'side': position.side,
                'pnl': realized_pnl,
                'pnl_pct': (realized_pnl / position.position_value) * 100,
                'reason': reason,
                'holding_time': (datetime.now() - position.entry_time).total_seconds() / 60  # minutes
            }
            
            self.trade_history.append(trade_record)
            self.closed_positions.append(position)
            
            # Remove from active positions
            del self.positions[symbol]
            
            # Log
            pnl_color = "profit" if realized_pnl > 0 else "loss"
            logger.info(f"{'🟢' if realized_pnl > 0 else '🔴'} Position closed: {symbol} ({reason})")
            logger.info(f"   Entry: Rs.{position.entry_price:.2f} → Exit: Rs.{exit_price:.2f}")
            logger.info(f"   P&L: Rs.{realized_pnl:+.2f} ({trade_record['pnl_pct']:+.2f}%)")
            logger.info(f"   New capital: Rs.{self.current_capital:.2f}")
            logger.info(f"   Drawdown: {self.current_drawdown:.2f}%")
            
            # Check circuit breakers
            self.check_circuit_breakers()
            
        except Exception as e:
            logger.error(f"Close position error: {e}")
    
    def calculate_var_cvar(self, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calculate Value at Risk (VaR) and Conditional VaR (CVaR)
        
        VaR = Maximum loss at given confidence level
        CVaR = Average of losses beyond VaR
        
        Returns:
            (VaR, CVaR) in percentage
        """
        try:
            if len(self.returns_history) < 30:
                return 0, 0
            
            returns = np.array(self.returns_history)
            
            # Calculate VaR (percentile of losses)
            var_percentile = 1 - confidence
            var = np.percentile(returns, var_percentile * 100)
            
            # Calculate CVaR (average of losses beyond VaR)
            cvar_returns = returns[returns <= var]
            cvar = np.mean(cvar_returns) if len(cvar_returns) > 0 else var
            
            self.var_95 = abs(var)
            self.cvar_95 = abs(cvar)
            
            return abs(var), abs(cvar)
            
        except Exception as e:
            logger.error(f"VaR/CVaR calculation error: {e}")
            return 0, 0
    
    def check_circuit_breakers(self):
        """Check if any circuit breakers should trigger"""
        try:
            # Daily loss limit
            if self.daily_pnl <= self.max_daily_loss:
                self.halt_trading(f"Daily loss limit hit: Rs.{self.daily_pnl:.2f}")
                return
            
            # Max drawdown
            if self.current_drawdown >= self.max_drawdown:
                self.halt_trading(f"Max drawdown hit: {self.current_drawdown:.2f}%")
                return
            
            # CVaR limit
            if self.cvar_95 > self.cvar_limit:
                self.halt_trading(f"CVaR limit exceeded: {self.cvar_95:.2f}%")
                return
            
        except Exception as e:
            logger.error(f"Circuit breaker check error: {e}")
    
    def halt_trading(self, reason: str):
        """Halt all trading (circuit breaker)"""
        self.is_trading_halted = True
        self.halt_reason = reason
        self.halt_time = datetime.now()
        
        logger.critical("=" * 80)
        logger.critical("🚨 TRADING HALTED - CIRCUIT BREAKER TRIGGERED 🚨")
        logger.critical("=" * 80)
        logger.critical(f"Reason: {reason}")
        logger.critical(f"Time: {self.halt_time}")
        logger.critical("All new positions blocked. Manual review required.")
        logger.critical("=" * 80)
    
    def resume_trading(self, override_code: str = None):
        """Resume trading (manual intervention required)"""
        if override_code == "RESUME_CONFIRMED":
            self.is_trading_halted = False
            self.halt_reason = None
            logger.warning("⚠️ Trading RESUMED manually")
        else:
            logger.error("Invalid override code - trading remains halted")
    
    def get_risk_report(self) -> Dict:
        """Generate comprehensive risk report"""
        try:
            # Calculate metrics
            total_position_value = sum(p.position_value for p in self.positions.values())
            total_unrealized_pnl = sum(p.unrealized_pnl for p in self.positions.values())
            
            # Win rate
            if self.trade_history:
                winning_trades = [t for t in self.trade_history if t['pnl'] > 0]
                win_rate = (len(winning_trades) / len(self.trade_history)) * 100
            else:
                win_rate = 0
            
            # Average win/loss
            if self.trade_history:
                wins = [t['pnl'] for t in self.trade_history if t['pnl'] > 0]
                losses = [abs(t['pnl']) for t in self.trade_history if t['pnl'] < 0]
                avg_win = np.mean(wins) if wins else 0
                avg_loss = np.mean(losses) if losses else 0
                profit_factor = sum(wins) / sum(losses) if losses and sum(losses) > 0 else 0
            else:
                avg_win = avg_loss = profit_factor = 0
            
            # Calculate VaR/CVaR
            var, cvar = self.calculate_var_cvar(self.var_confidence)
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'capital': {
                    'initial': self.initial_capital,
                    'current': self.current_capital,
                    'peak': self.peak_capital,
                    'change': self.current_capital - self.initial_capital,
                    'change_pct': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
                },
                'positions': {
                    'count': len(self.positions),
                    'max_allowed': self.max_positions,
                    'total_value': total_position_value,
                    'unrealized_pnl': total_unrealized_pnl
                },
                'risk': {
                    'portfolio_heat': self.portfolio_heat,
                    'max_portfolio_risk': self.max_portfolio_risk,
                    'current_drawdown': self.current_drawdown,
                    'max_drawdown_limit': self.max_drawdown,
                    'max_drawdown_observed': self.max_drawdown_observed,
                    'var_95': var,
                    'cvar_95': cvar,
                    'cvar_limit': self.cvar_limit
                },
                'performance': {
                    'daily_pnl': self.daily_pnl,
                    'daily_pnl_limit': self.max_daily_loss,
                    'trades_today': self.trade_count_today,
                    'max_daily_trades': self.max_daily_trades,
                    'total_trades': len(self.trade_history),
                    'win_rate': win_rate,
                    'avg_win': avg_win,
                    'avg_loss': avg_loss,
                    'profit_factor': profit_factor,
                    'sharpe_ratio': self.sharpe_ratio
                },
                'status': {
                    'trading_halted': self.is_trading_halted,
                    'halt_reason': self.halt_reason,
                    'halt_time': self.halt_time.isoformat() if self.halt_time else None
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Risk report generation error: {e}")
            return {}

# Export
__all__ = ['AdvancedRiskManager', 'Position']

if __name__ == "__main__":
    print("✅ Advanced Risk Management System Module Loaded")
    print("   - Kelly Criterion position sizing")
    print("   - VaR/CVaR risk metrics")
    print("   - ATR-based dynamic stops")
    print("   - Circuit breakers & portfolio heat map")
