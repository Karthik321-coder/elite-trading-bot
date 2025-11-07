"""
🚀 ELITE TRADING BOT - ULTIMATE REAL-TIME INTEGRATION MODULE

This module provides WORLD-CLASS features:
1. Real-time bot data extraction
2. Live P&L tick-by-tick monitoring
3. Position tracking with risk metrics
4. Trade execution analysis
5. AI model performance tracking
6. News sentiment live feed
7. Order flow analytics
8. Risk management system
9. Performance attribution
10. Alert management system
"""

import re
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import deque, defaultdict
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class UltimateDataExtractor:
    """
    Extracts real-time data from bot logs and provides ultimate analytics
    """
    
    def __init__(self):
        # Real-time tracking
        self.positions = {}  # symbol -> position data
        self.trades = deque(maxlen=500)  # Last 500 trades
        self.pnl_history = deque(maxlen=1000)  # 1000 P&L snapshots
        self.capital_history = deque(maxlen=1000)
        
        # AI Model tracking
        self.model_predictions = defaultdict(list)
        self.model_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
        
        # News sentiment tracking
        self.news_sentiment = defaultdict(list)
        
        # Order flow
        self.order_flow = deque(maxlen=200)
        
        # Risk metrics
        self.drawdown_peak = 0
        self.current_drawdown = 0
        self.max_drawdown = 0
        
        # Performance metrics
        self.daily_returns = []
        self.sharpe_ratio = 0.0
        self.sortino_ratio = 0.0
        self.profit_factor = 0.0
        
        # Trading stats
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.gross_profit = 0.0
        self.gross_loss = 0.0
        
        # Capital tracking
        self.starting_capital = 11.18
        self.current_capital = 11.18
        self.peak_capital = 11.18
        
        # Lock for thread safety
        self.lock = threading.Lock()
    
    def parse_log_line(self, log_line: str) -> Optional[Dict]:
        """
        Parse a single log line and extract all relevant data
        Returns dict with extracted data or None
        """
        with self.lock:
            extracted_data = {}
            
            try:
                # ═══════ 1. CAPITAL UPDATES ═══════
                capital_match = re.search(r'Current:\s*Rs\.(\d+\.?\d*)', log_line)
                if capital_match:
                    self.current_capital = float(capital_match.group(1))
                    self.capital_history.append({
                        'time': datetime.now().isoformat(),
                        'value': self.current_capital
                    })
                    
                    # Update peak for drawdown
                    if self.current_capital > self.peak_capital:
                        self.peak_capital = self.current_capital
                    
                    # Calculate drawdown
                    self.current_drawdown = ((self.peak_capital - self.current_capital) / self.peak_capital) * 100
                    if self.current_drawdown > self.max_drawdown:
                        self.max_drawdown = self.current_drawdown
                    
                    extracted_data['capital'] = self.current_capital
                    extracted_data['drawdown'] = self.current_drawdown
                
                # ═══════ 2. STARTING CAPITAL ═══════
                starting_match = re.search(r'Starting Capital:\s*Rs\.(\d+\.?\d*)', log_line)
                if starting_match:
                    self.starting_capital = float(starting_match.group(1))
                    extracted_data['starting_capital'] = self.starting_capital
                
                # ═══════ 3. TRADE EXECUTION ═══════
                if '📈 BUY' in log_line or '📉 SELL' in log_line:
                    trade_data = self._extract_trade(log_line)
                    if trade_data:
                        self.trades.append(trade_data)
                        extracted_data['trade'] = trade_data
                        
                        # Update trade stats
                        self.total_trades += 1
                        if trade_data.get('pnl', 0) > 0:
                            self.winning_trades += 1
                            self.gross_profit += trade_data['pnl']
                        elif trade_data.get('pnl', 0) < 0:
                            self.losing_trades += 1
                            self.gross_loss += abs(trade_data['pnl'])
                
                # ═══════ 4. POSITION UPDATES ═══════
                if 'Position' in log_line or 'Holdings' in log_line:
                    position_data = self._extract_position(log_line)
                    if position_data:
                        symbol = position_data['symbol']
                        self.positions[symbol] = position_data
                        extracted_data['position'] = position_data
                
                # ═══════ 5. P&L UPDATES ═══════
                pnl_match = re.search(r'P&L:\s*Rs\.([+-]?\d+\.?\d*)', log_line)
                if pnl_match:
                    pnl = float(pnl_match.group(1))
                    self.pnl_history.append({
                        'time': datetime.now().isoformat(),
                        'value': pnl
                    })
                    self.total_pnl = pnl
                    extracted_data['pnl'] = pnl
                
                # ═══════ 6. AI MODEL PREDICTIONS ═══════
                if 'Model:' in log_line or 'Prediction:' in log_line:
                    model_data = self._extract_model_prediction(log_line)
                    if model_data:
                        model_name = model_data['model']
                        self.model_predictions[model_name].append(model_data)
                        extracted_data['model_prediction'] = model_data
                
                # ═══════ 7. NEWS SENTIMENT ═══════
                if 'Sentiment:' in log_line or 'News:' in log_line:
                    sentiment_data = self._extract_news_sentiment(log_line)
                    if sentiment_data:
                        symbol = sentiment_data.get('symbol', 'MARKET')
                        self.news_sentiment[symbol].append(sentiment_data)
                        extracted_data['news_sentiment'] = sentiment_data
                
                # ═══════ 8. ORDER FLOW ═══════
                if 'Order' in log_line or 'Quantity' in log_line:
                    order_data = self._extract_order_flow(log_line)
                    if order_data:
                        self.order_flow.append(order_data)
                        extracted_data['order_flow'] = order_data
                
                # ═══════ 9. RISK ALERTS ═══════
                if '⚠️' in log_line or 'WARNING' in log_line or 'ALERT' in log_line:
                    alert_data = {
                        'time': datetime.now().isoformat(),
                        'type': 'WARNING',
                        'message': log_line,
                        'severity': 'medium'
                    }
                    
                    if 'ERROR' in log_line or '❌' in log_line:
                        alert_data['type'] = 'ERROR'
                        alert_data['severity'] = 'high'
                    
                    extracted_data['alert'] = alert_data
                
                # ═══════ 10. PERFORMANCE METRICS ═══════
                if 'Win Rate' in log_line:
                    win_rate_match = re.search(r'(\d+\.?\d*)%', log_line)
                    if win_rate_match:
                        extracted_data['win_rate'] = float(win_rate_match.group(1))
                
                return extracted_data if extracted_data else None
                
            except Exception as e:
                logger.error(f"Error parsing log line: {e}")
                return None
    
    def _extract_trade(self, log_line: str) -> Optional[Dict]:
        """Extract trade details from log line"""
        try:
            trade = {
                'time': datetime.now().isoformat(),
                'type': 'BUY' if 'BUY' in log_line else 'SELL'
            }
            
            # Extract symbol
            symbol_match = re.search(r'([A-Z]{2,20})', log_line)
            if symbol_match:
                trade['symbol'] = symbol_match.group(1)
            
            # Extract price
            price_match = re.search(r'@\s*Rs\.?(\d+\.?\d*)', log_line)
            if not price_match:
                price_match = re.search(r'Price:\s*Rs\.?(\d+\.?\d*)', log_line)
            if price_match:
                trade['price'] = float(price_match.group(1))
            
            # Extract quantity
            qty_match = re.search(r'Qty:\s*(\d+)', log_line)
            if not qty_match:
                qty_match = re.search(r'Quantity:\s*(\d+)', log_line)
            if qty_match:
                trade['quantity'] = int(qty_match.group(1))
            
            # Extract P&L if available
            pnl_match = re.search(r'P&L:\s*Rs\.([+-]?\d+\.?\d*)', log_line)
            if pnl_match:
                trade['pnl'] = float(pnl_match.group(1))
            
            return trade if 'symbol' in trade else None
            
        except Exception as e:
            return None
    
    def _extract_position(self, log_line: str) -> Optional[Dict]:
        """Extract position details"""
        try:
            position = {'time': datetime.now().isoformat()}
            
            # Extract symbol
            symbol_match = re.search(r'([A-Z]{2,20})', log_line)
            if symbol_match:
                position['symbol'] = symbol_match.group(1)
            
            # Extract quantity
            qty_match = re.search(r'Qty:\s*([+-]?\d+)', log_line)
            if qty_match:
                position['quantity'] = int(qty_match.group(1))
            
            # Extract entry price
            entry_match = re.search(r'Entry:\s*Rs\.?(\d+\.?\d*)', log_line)
            if entry_match:
                position['entry_price'] = float(entry_match.group(1))
            
            # Extract current price
            current_match = re.search(r'Current:\s*Rs\.?(\d+\.?\d*)', log_line)
            if current_match:
                position['current_price'] = float(current_match.group(1))
            
            # Extract P&L
            pnl_match = re.search(r'P&L:\s*Rs\.([+-]?\d+\.?\d*)', log_line)
            if pnl_match:
                position['pnl'] = float(pnl_match.group(1))
            
            # Calculate P&L % if prices available
            if 'entry_price' in position and 'current_price' in position:
                position['pnl_percent'] = ((position['current_price'] - position['entry_price']) / position['entry_price']) * 100
            
            return position if 'symbol' in position else None
            
        except Exception as e:
            return None
    
    def _extract_model_prediction(self, log_line: str) -> Optional[Dict]:
        """Extract AI model prediction"""
        try:
            prediction = {'time': datetime.now().isoformat()}
            
            # Extract model name
            model_match = re.search(r'Model:\s*([A-Za-z0-9_]+)', log_line)
            if model_match:
                prediction['model'] = model_match.group(1)
            
            # Extract prediction
            pred_match = re.search(r'Prediction:\s*([A-Za-z]+)', log_line)
            if pred_match:
                prediction['prediction'] = pred_match.group(1)
            
            # Extract confidence
            conf_match = re.search(r'Confidence:\s*(\d+\.?\d*)%?', log_line)
            if conf_match:
                prediction['confidence'] = float(conf_match.group(1))
            
            return prediction if 'model' in prediction else None
            
        except Exception as e:
            return None
    
    def _extract_news_sentiment(self, log_line: str) -> Optional[Dict]:
        """Extract news sentiment"""
        try:
            sentiment = {'time': datetime.now().isoformat()}
            
            # Extract symbol
            symbol_match = re.search(r'([A-Z]{2,20})', log_line)
            if symbol_match:
                sentiment['symbol'] = symbol_match.group(1)
            
            # Extract sentiment score
            score_match = re.search(r'Sentiment:\s*([+-]?\d+\.?\d*)', log_line)
            if score_match:
                sentiment['score'] = float(score_match.group(1))
            
            # Extract sentiment type
            if 'POSITIVE' in log_line or '✅' in log_line:
                sentiment['type'] = 'POSITIVE'
            elif 'NEGATIVE' in log_line or '❌' in log_line:
                sentiment['type'] = 'NEGATIVE'
            else:
                sentiment['type'] = 'NEUTRAL'
            
            return sentiment
            
        except Exception as e:
            return None
    
    def _extract_order_flow(self, log_line: str) -> Optional[Dict]:
        """Extract order flow data"""
        try:
            order = {'time': datetime.now().isoformat()}
            
            # Extract order ID
            id_match = re.search(r'Order\s*ID:\s*(\w+)', log_line)
            if id_match:
                order['order_id'] = id_match.group(1)
            
            # Extract status
            if 'PLACED' in log_line:
                order['status'] = 'PLACED'
            elif 'FILLED' in log_line or 'EXECUTED' in log_line:
                order['status'] = 'FILLED'
            elif 'REJECTED' in log_line:
                order['status'] = 'REJECTED'
            elif 'CANCELLED' in log_line:
                order['status'] = 'CANCELLED'
            
            return order if 'status' in order else None
            
        except Exception as e:
            return None
    
    def get_comprehensive_data(self) -> Dict:
        """Get all data in one comprehensive dictionary"""
        with self.lock:
            # Calculate real-time metrics
            win_rate = (self.winning_trades / max(1, self.total_trades)) * 100
            profit_factor = self.gross_profit / max(0.01, self.gross_loss) if self.gross_loss > 0 else 0
            
            # Calculate Sharpe ratio (simplified)
            if len(self.pnl_history) > 1:
                returns = [p['value'] for p in self.pnl_history]
                avg_return = sum(returns) / len(returns)
                std_return = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
                sharpe_ratio = (avg_return / max(0.01, std_return)) if std_return > 0 else 0
            else:
                sharpe_ratio = 0
            
            return {
                # Capital & P&L
                'starting_capital': self.starting_capital,
                'current_capital': self.current_capital,
                'total_pnl': self.total_pnl,
                'pnl_percent': ((self.current_capital - self.starting_capital) / self.starting_capital) * 100,
                'capital_history': list(self.capital_history)[-100:],  # Last 100 points
                'pnl_history': list(self.pnl_history)[-100:],
                
                # Trading Stats
                'total_trades': self.total_trades,
                'winning_trades': self.winning_trades,
                'losing_trades': self.losing_trades,
                'win_rate': win_rate,
                'gross_profit': self.gross_profit,
                'gross_loss': self.gross_loss,
                
                # Performance Metrics
                'profit_factor': profit_factor,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': self.max_drawdown,
                'current_drawdown': self.current_drawdown,
                
                # Positions
                'positions': list(self.positions.values()),
                'active_positions': len(self.positions),
                
                # Recent Trades
                'recent_trades': list(self.trades)[-20:],  # Last 20 trades
                
                # AI Models
                'model_predictions': {
                    model: predictions[-10:]  # Last 10 predictions per model
                    for model, predictions in self.model_predictions.items()
                },
                
                # News Sentiment
                'news_sentiment': {
                    symbol: sentiments[-5:]  # Last 5 news per symbol
                    for symbol, sentiments in self.news_sentiment.items()
                },
                
                # Order Flow
                'recent_orders': list(self.order_flow)[-20:],
                
                # Risk Metrics
                'risk_metrics': {
                    'peak_capital': self.peak_capital,
                    'current_drawdown_pct': self.current_drawdown,
                    'max_drawdown_pct': self.max_drawdown,
                    'risk_reward_ratio': profit_factor,
                }
            }


# Global instance
ultimate_extractor = UltimateDataExtractor()
