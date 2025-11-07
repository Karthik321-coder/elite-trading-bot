#!/usr/bin/env python3
"""
Elite Trading Bot V5.0 - Main Entry Point
Professional Automated Trading System
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.elite_trading_bot import *

if __name__ == "__main__":
    print("="*80)
    print("🚀 ELITE TRADING BOT V5.0 - STARTING...")
    print("="*80)
    
    # Run the main trading bot
    main()
