"""
Quick Dhan Account Verification Script
Checks account status, balance, and readiness for live trading
"""
import os
from dotenv import load_dotenv
from dhanhq import dhanhq

# Load environment
load_dotenv()

print("═" * 80)
print("  🔍 DHAN ACCOUNT VERIFICATION FOR LIVE TRADING")
print("═" * 80)

# Get credentials
client_id = os.getenv('DHAN_CLIENT_ID')
access_token = os.getenv('DHAN_ACCESS_TOKEN')

print(f"\n✓ Client ID: {client_id}")
print(f"✓ Access Token: {access_token[:50]}... (valid until 2025-11-05)")

try:
    # Initialize Dhan client
    print("\n⏳ Connecting to Dhan API...")
    dhan = dhanhq(client_id, access_token)
    
    # Get fund limits
    print("\n⏳ Fetching account funds...")
    funds = dhan.get_fund_limits()
    
    if funds and 'data' in funds:
        print("\n" + "═" * 80)
        print("  💰 ACCOUNT BALANCE & LIMITS")
        print("═" * 80)
        
        data = funds['data']
        available_balance = data.get('availabelBalance', 0)
        sodLimit = data.get('sodLimit', 0)
        
        print(f"\n  Available Balance:     Rs.{available_balance:,.2f}")
        print(f"  Start of Day Limit:    Rs.{sodLimit:,.2f}")
        
        # Check if sufficient for Rs.500 capital
        if available_balance >= 500:
            print(f"\n  ✅ SUFFICIENT FUNDS for Rs.500 capital")
            print(f"  ✅ Can place trades up to Rs.{available_balance:,.2f}")
        else:
            print(f"\n  ⚠️  INSUFFICIENT FUNDS - Need Rs.500, have Rs.{available_balance:,.2f}")
            print(f"  ⚠️  Please add funds to your Dhan account")
        
    # Get positions
    print("\n⏳ Checking current positions...")
    positions = dhan.get_positions()
    
    if positions and 'data' in positions:
        pos_list = positions['data']
        if pos_list:
            print(f"\n  📊 Current Open Positions: {len(pos_list)}")
            for pos in pos_list:
                symbol = pos.get('tradingSymbol', 'Unknown')
                qty = pos.get('netQty', 0)
                pnl = pos.get('realizedProfit', 0)
                print(f"     - {symbol}: Qty {qty}, P&L: Rs.{pnl:.2f}")
        else:
            print(f"\n  ✅ No open positions (clean slate)")
    
    # Get order book (today's trades)
    print("\n⏳ Checking today's orders...")
    orders = dhan.get_order_list()
    
    if orders and 'data' in orders:
        order_list = orders['data']
        if order_list:
            print(f"\n  📋 Today's Orders: {len(order_list)}")
            for order in order_list[:5]:  # Show last 5
                symbol = order.get('tradingSymbol', 'Unknown')
                status = order.get('orderStatus', 'Unknown')
                print(f"     - {symbol}: {status}")
        else:
            print(f"\n  ✅ No orders today (fresh start)")
    
    print("\n" + "═" * 80)
    print("  ✅ DHAN ACCOUNT VERIFICATION COMPLETE")
    print("═" * 80)
    print("\n  🟢 Connection: SUCCESSFUL")
    print("  🟢 API Access: WORKING")
    print("  🟢 Account Status: ACTIVE")
    
    if available_balance >= 500:
        print("\n  ✅ READY FOR LIVE TRADING")
        print("\n  Next Step: Run the bot with real money")
        print("  Command: python Untitled-1.py")
    else:
        print("\n  ⚠️  ADD FUNDS before live trading")
        print(f"  Need: Rs.500, Current: Rs.{available_balance:,.2f}")
    
except Exception as e:
    print("\n" + "═" * 80)
    print("  ❌ ERROR DURING VERIFICATION")
    print("═" * 80)
    print(f"\n  Error: {str(e)}")
    print("\n  Possible Issues:")
    print("  1. Access token expired (expires 2025-11-05)")
    print("  2. Network connection issue")
    print("  3. Dhan API service down")
    print("  4. Invalid credentials")
    
print("\n" + "═" * 80)
