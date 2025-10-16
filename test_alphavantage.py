import requests
import pandas as pd
from datetime import datetime

def test_alphavantage(api_key):
    """Simple test of Alpha Vantage API"""
    print("Testing Alpha Vantage API...")
    
    # Basic API call for SPY daily data
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "SPY",
        "apikey": api_key,
        "outputsize": "compact"  # Last 100 data points
    }
    
    try:
        print("Making API request...")
        response = requests.get(url, params=params, timeout=15)
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            return False
            
        data = response.json()
        print("Response received, checking content...")
        
        # Check for errors
        if "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return False
            
        if "Note" in data:
            print(f"API Note: {data['Note']}")
            return False
            
        # Check for data
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            print(f"Success! Got {len(time_series)} data points")
            
            # Show latest data point
            latest_date = max(time_series.keys())
            latest_data = time_series[latest_date]
            latest_close = latest_data["4. close"]
            
            print(f"Latest date: {latest_date}")
            print(f"Latest SPY close: ${latest_close}")
            
            return True
        else:
            print("No time series data found in response")
            print("Response keys:", list(data.keys()))
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        return False

# Run the test
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "WSX7H7P2WR12YTGT"
    
    if API_KEY == "YOUR_API_KEY_HERE":
        API_KEY = input("Enter your Alpha Vantage API key: ")
    
    success = test_alphavantage(API_KEY)
    
    if success:
        print("\nAlpha Vantage is working! We can use this for the trading system.")
    else:
        print("\nAlpha Vantage test failed.")