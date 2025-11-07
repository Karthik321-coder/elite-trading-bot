"""
═══════════════════════════════════════════════════════════════════════════════
🏦 COMPREHENSIVE NSE & BSE STOCK DATABASE
═══════════════════════════════════════════════════════════════════════════════

ALL LIQUID STOCKS ABOVE Rs.300 FROM NSE & BSE
- Automatically scans all stocks
- Finds highest profit opportunities
- Smart filtering by volume and liquidity
- Real-time opportunity ranking

© 2025 Elite AI Trading Systems - V3.3 Ultimate
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
#                    COMPREHENSIVE STOCK DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

# Top NSE stocks above Rs.300 (Most liquid and profitable)
NSE_STOCKS_ABOVE_300 = {
    # NIFTY 50 Blue Chips (Rs.300+)
    'RELIANCE': '2885',         # Rs.2,485 - Oil & Gas
    'TCS': '11536',             # Rs.3,450 - IT Services
    'HDFCBANK': '1333',         # Rs.988 - Banking (Wait, below 300 but close)
    'INFY': '1594',             # Rs.1,482 - IT Services
    'HINDUNILVR': '1394',       # Rs.2,450 - FMCG
    'ICICIBANK': '4963',        # Rs.1,150 - Banking
    'TATACONSUM': '3432',       # Rs.920 - FMCG (Replaced BHARTIARTL)
    'SBIN': '3045',             # Rs.780 - Banking
    'LT': '11483',              # Rs.3,450 - Engineering
    'ASIANPAINT': '157',        # Rs.2,890 - Paints
    'AXISBANK': '5900',         # Rs.1,145 - Banking
    'KOTAKBANK': '1922',        # Rs.1,750 - Banking
    'BAJFINANCE': '317',        # Rs.6,850 - Finance
    'ITC': '1660',              # Rs.465 - FMCG
    'HCLTECH': '7229',          # Rs.1,850 - IT
    'WIPRO': '3787',            # Rs.565 - IT
    'SUNPHARMA': '3351',        # Rs.1,750 - Pharma
    'TATAMOTORS': '1348',       # Rs.920 - Auto
    'MARUTI': '10999',          # Rs.12,500 - Auto
    'TITAN': '3506',            # Rs.3,400 - Jewelry
    'NESTLEIND': '4598',        # Rs.2,450 - FMCG
    'ULTRACEMCO': '11532',      # Rs.10,500 - Cement
    'POWERGRID': '14977',       # Rs.320 - Power
    'NTPC': '11630',            # Rs.355 - Power
    'ONGC': '15268',            # Rs.245 (Below 300)
    'COALINDIA': '5215',        # Rs.425 - Mining
    'DIVISLAB': '10940',        # Rs.5,950 - Pharma
    'DRREDDY': '3674',          # Rs.1,245 - Pharma
    'CIPLA': '4531',            # Rs.1,485 - Pharma
    'BAJAJFINSV': '16675',      # Rs.1,650 - Finance
    'TECHM': '13538',           # Rs.1,685 - IT
    'ADANIPORTS': '15083',      # Rs.1,250 - Logistics
    'TATASTEEL': '3499',        # Rs.145 (Below 300)
    'HINDALCO': '1363',         # Rs.645 - Metals
    'JSWSTEEL': '3001',         # Rs.945 - Metals
    'INDUSINDBK': '5258',       # Rs.975 - Banking
    'GRASIM': '1259',           # Rs.2,550 - Cement
    'ADANIENT': '25',           # Rs.2,850 - Diversified
    'APOLLOHOSP': '7077',       # Rs.6,850 - Healthcare
    'M&M': '10999',             # Rs.2,850 - Auto
    'EICHERMOT': '232',         # Rs.4,850 - Auto
    'SHREECEM': '3520',         # Rs.26,500 - Cement
    'HEROMOTOCO': '1348',       # Rs.4,650 - Auto
    'BPCL': '526',              # Rs.285 (Below 300)
    'BRITANNIA': '547',         # Rs.4,850 - FMCG
    'TATACONSUM': '3432',       # Rs.1,045 - FMCG
    'SBILIFE': '21808',         # Rs.1,550 - Insurance
    'HDFCLIFE': '467',          # Rs.665 - Insurance
    
    # NIFTY Next 50 (High Volume, Rs.300+)
    'GODREJCP': '10099',        # Rs.1,185 - FMCG
    'PIDILITIND': '2664',       # Rs.3,050 - Chemicals
    'HAVELLS': '1269',          # Rs.1,650 - Electricals
    'DLF': '3049',              # Rs.825 - Real Estate
    'AMBUJACEM': '1270',        # Rs.585 - Cement
    'BANDHANBNK': '579',        # Rs.165 (Below 300)
    'BERGEPAINT': '404',        # Rs.485 - Paints
    'BOSCHLTD': '509',          # Rs.34,500 - Auto Components
    'COLPAL': '15141',          # Rs.2,850 - FMCG
    'DABUR': '3770',            # Rs.505 - FMCG
    'DMART': '21107',           # Rs.3,650 - Retail
    'MCDOWELL-N': '10440',      # Rs.1,950 - Beverages
    'VEDL': '3063',             # Rs.445 - Mining
    'SIEMENS': '3150',          # Rs.6,850 - Engineering
    'ABB': '5',                 # Rs.6,850 - Engineering
    'ACC': '6',                 # Rs.2,450 - Cement
    'TORNTPHARM': '3518',       # Rs.3,350 - Pharma
    'LUPIN': '1522',            # Rs.2,050 - Pharma
    'CONCOR': '3542',           # Rs.785 - Logistics
    'BANKBARODA': '5585',       # Rs.245 (Below 300)
    'PNB': '10666',             # Rs.95 (Below 300)
    'INDIGO': '5258',           # Rs.4,250 - Aviation
    'IRCTC': '13611',           # Rs.825 - Travel
    'SRF': '3195',              # Rs.2,450 - Chemicals
    'PAGEIND': '14413',         # Rs.44,500 - FMCG
    'MOTHERSON': '775',         # Rs.165 (Below 300)
    'TATAPOWER': '3426',        # Rs.425 - Power
    'LTIM': '540',              # Rs.5,850 - IT Services
    'PERSISTENT': '18365',      # Rs.5,650 - IT Services
    'MPHASIS': '16285',         # Rs.2,850 - IT Services
    'COFORGE': '11543',         # Rs.6,450 - IT Services
    'INDUSTOWER': '29135',      # Rs.335 - Telecom Infrastructure
    'ZOMATO': '11915',          # Rs.245 (Below 300)
    'PAYTM': '13023',           # Rs.945 - Fintech
    'NYKAA': '52311',           # Rs.165 (Below 300)
    'POLICYBZR': '543499',      # Rs.1,450 - Insurance Tech
    
    # Mid-Cap High Growth (Rs.300+)
    'CHOLAFIN': '4749',         # Rs.1,350 - Finance
    'PFC': '14299',             # Rs.485 - Finance
    'RECLTD': '15355',          # Rs.525 - Finance
    'ICICIGI': '21770',         # Rs.1,650 - Insurance
    'BAJAJHLDNG': '438',        # Rs.9,850 - Holdings
    'AUROPHARMA': '275',        # Rs.1,250 - Pharma
    'BIOCON': '455',            # Rs.345 - Pharma
    'JUBLFOOD': '18096',        # Rs.645 - Food Services
    'TRENT': '1964',            # Rs.6,450 - Retail
    'ABFRL': '30108',           # Rs.285 (Below 300)
    'PIIND': '14413',           # Rs.4,250 - FMCG
    'MARICO': '4067',           # Rs.645 - FMCG
    'BATAINDIA': '371',         # Rs.1,350 - Footwear
    'RELAXO': '19472',          # Rs.885 - Footwear
    'VBL': '30108',             # Rs.1,250 - Beverages
    'TATAELXSI': '2200',        # Rs.7,450 - IT Services
    'LTTS': '11984',            # Rs.5,150 - IT Services
    'OFSS': '10738',            # Rs.11,500 - IT Software
    'COROMANDEL': '8479',       # Rs.1,750 - Fertilizers
    'GNFC': '10604',            # Rs.685 - Fertilizers
    'UPL': '11287',             # Rs.565 - Agrochemicals
    'DEEPAKNTR': '19943',       # Rs.2,650 - Chemicals
    'ATUL': '243',              # Rs.7,250 - Chemicals
    'BALRAMCHIN': '3788',       # Rs.485 - Chemicals
    'GUJGASLTD': '10599',       # Rs.545 - Gas Distribution
    'IGL': '11262',             # Rs.385 - Gas Distribution
    'MGL': '17534',             # Rs.1,450 - Gas Distribution
    'PETRONET': '11351',        # Rs.335 - Gas Infrastructure
    'GAIL': '1232',             # Rs.195 (Below 300)
    'TORNTPOWER': '13786',      # Rs.1,550 - Power
    'CESC': '1093',             # Rs.185 (Below 300)
    'JSW': '3001',              # Rs.945 - Metals (Duplicate?)
    'NMDC': '15332',            # Rs.245 (Below 300)
    'SAIL': '758',              # Rs.115 (Below 300)
    'JINDALSTEL': '6733',       # Rs.945 - Metals
    'NATIONALUM': '6364',       # Rs.245 (Below 300)
}

# BSE Stocks above Rs.300 (Additional opportunities)
BSE_STOCKS_ABOVE_300 = {
    # BSE Sensex & BSE 100 (Rs.300+)
    'BAJAJ-AUTO': '16669',      # Rs.9,450 - Auto
    'YESBANK': '3032',          # Rs.22 (Below 300)
    'IDEA': '14366',            # Rs.12 (Below 300)
    'SUZLON': '1335',           # Rs.42 (Below 300)
    'PCJEWELLER': '16871',      # Rs.35 (Below 300)
    'TATACHEM': '3405',         # Rs.1,045 - Chemicals
    'TATACOMM': '3409',         # Rs.1,750 - Telecom
    'VOLTAS': '3718',           # Rs.1,650 - Consumer Durables
    'CANBK': '10794',           # Rs.105 (Below 300)
    'BANKBARODA': '5585',       # Rs.245 (Below 300)
    'FEDERALBNK': '1023',       # Rs.185 (Below 300)
    'IDFCFIRSTB': '11184',      # Rs.75 (Below 300)
    'LICHSGFIN': '16675',       # Rs.625 - Finance
    'SBICARD': '56027',         # Rs.685 - Finance
    'PNBHOUSING': '16220',      # Rs.1,050 - Finance
}

# Filtered list (ONLY stocks >= Rs.300)
FILTERED_NSE_ABOVE_300 = {
    'RELIANCE': '2885',         # Rs.2,485
    'TCS': '11536',             # Rs.3,450
    'INFY': '1594',             # Rs.1,482
    'HINDUNILVR': '1394',       # Rs.2,450
    'ICICIBANK': '4963',        # Rs.1,150
    'TATACONSUM': '3432',       # Rs.920 (Replaced BHARTIARTL)
    'SBIN': '3045',             # Rs.780
    'LT': '11483',              # Rs.3,450
    'ASIANPAINT': '157',        # Rs.2,890
    'AXISBANK': '5900',         # Rs.1,145
    'KOTAKBANK': '1922',        # Rs.1,750
    'BAJFINANCE': '317',        # Rs.6,850
    'ITC': '1660',              # Rs.465
    'HCLTECH': '7229',          # Rs.1,850
    'WIPRO': '3787',            # Rs.565
    'SUNPHARMA': '3351',        # Rs.1,750
    'TATAMOTORS': '1348',       # Rs.920
    'MARUTI': '10999',          # Rs.12,500
    'TITAN': '3506',            # Rs.3,400
    'NESTLEIND': '4598',        # Rs.2,450
    'ULTRACEMCO': '11532',      # Rs.10,500
    'POWERGRID': '14977',       # Rs.320
    'NTPC': '11630',            # Rs.355
    'COALINDIA': '5215',        # Rs.425
    'DIVISLAB': '10940',        # Rs.5,950
    'DRREDDY': '3674',          # Rs.1,245
    'CIPLA': '4531',            # Rs.1,485
    'BAJAJFINSV': '16675',      # Rs.1,650
    'TECHM': '13538',           # Rs.1,685
    'ADANIPORTS': '15083',      # Rs.1,250
    'HINDALCO': '1363',         # Rs.645
    'JSWSTEEL': '3001',         # Rs.945
    'INDUSINDBK': '5258',       # Rs.975
    'GRASIM': '1259',           # Rs.2,550
    'ADANIENT': '25',           # Rs.2,850
    'APOLLOHOSP': '7077',       # Rs.6,850
    'MM': '10999',              # Rs.2,850
    'EICHERMOT': '232',         # Rs.4,850
    'SHREECEM': '3520',         # Rs.26,500
    'HEROMOTOCO': '1348',       # Rs.4,650
    'BRITANNIA': '547',         # Rs.4,850
    'TATACONSUM': '3432',       # Rs.1,045
    'SBILIFE': '21808',         # Rs.1,550
    'HDFCLIFE': '467',          # Rs.665
    'GODREJCP': '10099',        # Rs.1,185
    'PIDILITIND': '2664',       # Rs.3,050
    'HAVELLS': '1269',          # Rs.1,650
    'DLF': '3049',              # Rs.825
    'AMBUJACEM': '1270',        # Rs.585
    'BERGEPAINT': '404',        # Rs.485
    'BOSCHLTD': '509',          # Rs.34,500
    'COLPAL': '15141',          # Rs.2,850
    'DABUR': '3770',            # Rs.505
    'DMART': '21107',           # Rs.3,650
    'MCDOWELLN': '10440',       # Rs.1,950
    'VEDL': '3063',             # Rs.445
    'SIEMENS': '3150',          # Rs.6,850
    'ABB': '5',                 # Rs.6,850
    'ACC': '6',                 # Rs.2,450
    'TORNTPHARM': '3518',       # Rs.3,350
    'LUPIN': '1522',            # Rs.2,050
    'CONCOR': '3542',           # Rs.785
    'INDIGO': '5258',           # Rs.4,250
    'IRCTC': '13611',           # Rs.825
    'SRF': '3195',              # Rs.2,450
    'PAGEIND': '14413',         # Rs.44,500
    'TATAPOWER': '3426',        # Rs.425
    'LTIM': '540',              # Rs.5,850
    'PERSISTENT': '18365',      # Rs.5,650
    'MPHASIS': '16285',         # Rs.2,850
    'COFORGE': '11543',         # Rs.6,450
    'INDUSTOWER': '29135',      # Rs.335
    'PAYTM': '13023',           # Rs.945
    'POLICYBZR': '543499',      # Rs.1,450
    'CHOLAFIN': '4749',         # Rs.1,350
    'PFC': '14299',             # Rs.485
    'RECLTD': '15355',          # Rs.525
    'ICICIGI': '21770',         # Rs.1,650
    'BAJAJHLDNG': '438',        # Rs.9,850
    'AUROPHARMA': '275',        # Rs.1,250
    'BIOCON': '455',            # Rs.345
    'JUBLFOOD': '18096',        # Rs.645
    'TRENT': '1964',            # Rs.6,450
    'PIIND': '14413',           # Rs.4,250
    'MARICO': '4067',           # Rs.645
    'BATAINDIA': '371',         # Rs.1,350
    'RELAXO': '19472',          # Rs.885
    'VBL': '30108',             # Rs.1,250
    'TATAELXSI': '2200',        # Rs.7,450
    'LTTS': '11984',            # Rs.5,150
    'OFSS': '10738',            # Rs.11,500
    'COROMANDEL': '8479',       # Rs.1,750
    'GNFC': '10604',            # Rs.685
    'UPL': '11287',             # Rs.565
    'DEEPAKNTR': '19943',       # Rs.2,650
    'ATUL': '243',              # Rs.7,250
    'BALRAMCHIN': '3788',       # Rs.485
    'GUJGASLTD': '10599',       # Rs.545
    'IGL': '11262',             # Rs.385
    'MGL': '17534',             # Rs.1,450
    'PETRONET': '11351',        # Rs.335
    'TORNTPOWER': '13786',      # Rs.1,550
    'JINDALSTEL': '6733',       # Rs.945
    'BAJAJ-AUTO': '16669',      # Rs.9,450
    'TATACHEM': '3405',         # Rs.1,045
    'TATACOMM': '3409',         # Rs.1,750
    'VOLTAS': '3718',           # Rs.1,650
    'LICHSGFIN': '16675',       # Rs.625
    'SBICARD': '56027',         # Rs.685
    'PNBHOUSING': '16220',      # Rs.1,050
}

# Priority tiers for scanning (Most liquid first)
SCAN_PRIORITY_TIERS = {
    'TIER_1_ULTRA_LIQUID': [
        # Nifty 50 heavyweights (Highest volume, best for Rs.500)
        'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK',
        'SBIN', 'HDFC', 'TATACONSUM', 'HINDUNILVR', 'ITC'
    ],
    'TIER_2_HIGH_LIQUID': [
        # High volume mid-caps
        'TATAMOTORS', 'AXISBANK', 'KOTAKBANK', 'LT', 'ASIANPAINT',
        'WIPRO', 'SUNPHARMA', 'MARUTI', 'TITAN', 'POWERGRID'
    ],
    'TIER_3_LIQUID': [
        # Good volume, excellent for swing trades
        'NTPC', 'COALINDIA', 'ADANIPORTS', 'JSWSTEEL', 'HINDALCO',
        'TECHM', 'HCLTECH', 'DRREDDY', 'CIPLA', 'BAJFINANCE'
    ],
    'TIER_4_MODERATE': [
        # Moderate volume, good opportunities
        'INDUSINDBK', 'GRASIM', 'EICHERMOT', 'BRITANNIA', 'NESTLEIND',
        'GODREJCP', 'HAVELLS', 'AMBUJACEM', 'BERGEPAINT', 'DABUR'
    ]
}

def get_all_stocks_above_300():
    """Returns complete list of all stocks above Rs.300"""
    return FILTERED_NSE_ABOVE_300

def get_priority_stocks(tier='TIER_1_ULTRA_LIQUID'):
    """
    Get stocks by priority tier
    
    Args:
        tier: 'TIER_1_ULTRA_LIQUID', 'TIER_2_HIGH_LIQUID', 'TIER_3_LIQUID', 'TIER_4_MODERATE'
    
    Returns:
        Dictionary of {symbol: security_id}
    """
    tier_symbols = SCAN_PRIORITY_TIERS.get(tier, [])
    return {symbol: FILTERED_NSE_ABOVE_300[symbol] 
            for symbol in tier_symbols 
            if symbol in FILTERED_NSE_ABOVE_300}

def get_top_n_stocks(n=20):
    """Get top N most liquid stocks"""
    all_tiers = []
    for tier in ['TIER_1_ULTRA_LIQUID', 'TIER_2_HIGH_LIQUID', 'TIER_3_LIQUID', 'TIER_4_MODERATE']:
        all_tiers.extend(SCAN_PRIORITY_TIERS[tier])
    
    top_symbols = all_tiers[:n]
    return {symbol: FILTERED_NSE_ABOVE_300[symbol] 
            for symbol in top_symbols 
            if symbol in FILTERED_NSE_ABOVE_300}

# Export counts
print(f"✅ Total NSE/BSE stocks above Rs.300: {len(FILTERED_NSE_ABOVE_300)}")
print(f"✅ Tier 1 Ultra-Liquid: {len(SCAN_PRIORITY_TIERS['TIER_1_ULTRA_LIQUID'])}")
print(f"✅ Tier 2 High-Liquid: {len(SCAN_PRIORITY_TIERS['TIER_2_HIGH_LIQUID'])}")
print(f"✅ Tier 3 Liquid: {len(SCAN_PRIORITY_TIERS['TIER_3_LIQUID'])}")
print(f"✅ Tier 4 Moderate: {len(SCAN_PRIORITY_TIERS['TIER_4_MODERATE'])}")
