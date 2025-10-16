import yfinance as yf
import requests
from datetime import datetime, timedelta

def test_yfinance_detailed():
    """Comprehensive test of yfinance functionality"""
    print("Testing yfinance API in detail...")
    
    # Test 1: Basic internet connectivity
    print("\n1. Testing internet connectivity...")
    try:
        response = requests.get("https://finance.yahoo.com", timeout=10)
        print(f"Yahoo Finance accessible: {response.status_code == 200}")
    except Exception as e:
        print(f"Internet/Yahoo Finance issue: {e}")
        return False
    
    # Test 2: Simple ticker info
    print("\n2. Testing basic ticker info...")
    try:
        spy = yf.Ticker("SPY")
        info = spy.info
        if info and 'symbol' in info:
            print(f"SPY info accessible: {info.get('longName', 'Unknown')}")
            print(f"Current price estimate: ${info.get('regularMarketPrice', 'N/A')}")
        else:
            print("Could not get ticker info")
    except Exception as e:
        print(f"Ticker info error: {e}")
    
    # Test 3: Different time periods and intervals
    test_configs = [
        ("1d", "1m"),   # 1 day of 1-minute data
        ("5d", "5m"),   # 5 days of 5-minute data  
        ("1mo", "1h"),  # 1 month of 1-hour data
        ("3mo", "1d"),  # 3 months of daily data
        ("1y", "1d"),   # 1 year of daily data
    ]
    
    print("\n3. Testing different data periods...")
    successful_configs = []
    
    for period, interval in test_configs:
        try:
            print(f"Trying period={period}, interval={interval}...")
            spy = yf.Ticker("SPY")
            data = spy.history(period=period, interval=interval, timeout=15)
            
            if not data.empty:
                latest_price = data['Close'].iloc[-1]
                print(f"  SUCCESS: Got {len(data)} points, latest=${latest_price:.2f}")
                successful_configs.append((period, interval, len(data)))
            else:
                print(f"  FAILED: No data returned")
                
        except Exception as e:
            print(f"  ERROR: {e}")
    
    # Test 4: Manual date range
    print("\n4. Testing manual date ranges...")
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        spy = yf.Ticker("SPY")
        data = spy.history(start=start_date, end=end_date, interval="1d")
        
        if not data.empty:
            print(f"Manual date range SUCCESS: {len(data)} days of data")
            print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
            print(f"Latest close: ${data['Close'].iloc[-1]:.2f}")
        else:
            print("Manual date range FAILED: No data")
            
    except Exception as e:
        print(f"Manual date range ERROR: {e}")
    
    # Test 5: Alternative symbols
    print("\n5. Testing alternative symbols...")
    test_symbols = ["AAPL", "MSFT", "QQQ", "IVV"]  # IVV is another S&P 500 ETF
    
    for symbol in test_symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d", interval="1d")
            if not data.empty:
                print(f"  {symbol}: SUCCESS ({len(data)} points)")
                break
        except:
            print(f"  {symbol}: FAILED")
    
    # Summary
    print(f"\nSUMMARY:")
    print(f"Successful configurations: {len(successful_configs)}")
    for period, interval, points in successful_configs:
        print(f"  {period}/{interval}: {points} data points")
    
    return len(successful_configs) > 0

def test_alternative_data_sources():
    """Test alternative data sources if yfinance fails"""
    print("\nTesting alternative data sources...")
    
    # Test Alpha Vantage (free tier available)
    print("1. Alpha Vantage API test...")
    try:
        # This would require an API key, but we can test the endpoint
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&apikey=demo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("  Alpha Vantage accessible (would need API key)")
        else:
            print("  Alpha Vantage not accessible")
    except:
        print("  Alpha Vantage connection failed")
    
    # Test Polygon.io (has free tier)
    print("2. Polygon.io API test...")
    try:
        # Test with demo endpoint
        url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/day/2023-01-01/2023-01-02?apikey=demo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("  Polygon.io accessible (would need API key)")
        else:
            print("  Polygon.io not accessible")
    except:
        print("  Polygon.io connection failed")
    
    return True