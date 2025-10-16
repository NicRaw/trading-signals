from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Union

load_dotenv()

class MarketDataFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        
        if not self.api_key:
            print("WARNING: No ALPHAVANTAGE_API_KEY found in environment variables")
            print("Add ALPHAVANTAGE_API_KEY=your_key to your .env file")
        
    def get_data(self, symbols: Union[str, List[str]], timeframe: str = '1d', periods: int = 100) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Get market data for one or multiple symbols
        
        Args:
            symbols: Single symbol string or list of symbols
            timeframe: Time interval (currently supports '1d' daily data)
            periods: Number of periods to fetch
            
        Returns:
            For single symbol: DataFrame
            For multiple symbols: Dict[symbol -> DataFrame]
        """
        # Handle single symbol case (backward compatibility)
        if isinstance(symbols, str):
            return self._get_single_symbol_data(symbols, timeframe, periods)
        
        # Handle multiple symbols case
        if isinstance(symbols, list):
            return self._get_multi_symbol_data(symbols, timeframe, periods)
        
        raise ValueError("symbols must be a string or list of strings")
    
    def _get_single_symbol_data(self, symbol: str, timeframe: str, periods: int) -> pd.DataFrame:
        """Get data for a single symbol (original functionality)"""
        cache_key = f"{symbol}_{timeframe}_{periods}"
        now = datetime.now()
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if now - cached_time < self.cache_duration:
                print(f"Using cached data for {symbol}")
                return cached_data
        
        print(f"Fetching fresh data for {symbol} from Alpha Vantage...")
        
        # If no API key, fall back to synthetic data
        if not self.api_key:
            print("No API key available, using synthetic data")
            return self._create_synthetic_data(symbol)
        
        # Try to get real data from Alpha Vantage
        data = self._fetch_from_alphavantage(symbol)
        
        if data.empty:
            print("Alpha Vantage failed, using synthetic data")
            data = self._create_synthetic_data(symbol)
        
        # Cache successful result
        if not data.empty:
            self.cache[cache_key] = (data, now)
        
        return data
    
    def _get_multi_symbol_data(self, symbols: List[str], timeframe: str, periods: int) -> Dict[str, pd.DataFrame]:
        """Get data for multiple symbols"""
        result = {}
        
        for symbol in symbols:
            print(f"Fetching data for {symbol}...")
            
            # Add delay between API calls to avoid rate limits
            if len(result) > 0:
                print("Waiting 12 seconds between API calls to respect rate limits...")
                time.sleep(12)  # Alpha Vantage free tier: 5 calls per minute
            
            try:
                data = self._get_single_symbol_data(symbol, timeframe, periods)
                if not data.empty:
                    result[symbol] = data
                    print(f"Successfully fetched {len(data)} data points for {symbol}")
                else:
                    print(f"Failed to fetch data for {symbol}")
                    
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                # Continue with other symbols even if one fails
                continue
        
        return result
    
    def _fetch_from_alphavantage(self, symbol: str) -> pd.DataFrame:
        """Fetch data from Alpha Vantage API"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": "compact"  # Last 100 data points
            }
            
            print(f"Making API request for {symbol}...")
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"HTTP Error for {symbol}: {response.status_code}")
                return pd.DataFrame()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                print(f"Alpha Vantage Error for {symbol}: {data['Error Message']}")
                return pd.DataFrame()
            
            if "Note" in data:
                print(f"Alpha Vantage Rate Limit for {symbol}: {data['Note']}")
                return pd.DataFrame()
            
            # Parse the time series data
            if "Time Series (Daily)" not in data:
                print(f"No time series data in response for {symbol}")
                return pd.DataFrame()
            
            time_series = data["Time Series (Daily)"]
            
            # Convert to DataFrame
            df_data = []
            for date_str, values in time_series.items():
                df_data.append({
                    'Open': float(values['1. open']),
                    'High': float(values['2. high']),
                    'Low': float(values['3. low']),
                    'Close': float(values['4. close']),
                    'Volume': int(values['5. volume'])
                })
            
            # Create DataFrame with dates as index
            dates = [pd.to_datetime(date) for date in time_series.keys()]
            df = pd.DataFrame(df_data, index=dates)
            df.sort_index(inplace=True)  # Sort by date
            
            print(f"Successfully fetched {len(df)} data points for {symbol}")
            print(f"Date range: {df.index[0].date()} to {df.index[-1].date()}")
            print(f"Latest close: ${df['Close'].iloc[-1]:.2f}")
            
            return df
            
        except Exception as e:
            print(f"Alpha Vantage fetch error for {symbol}: {e}")
            return pd.DataFrame()
    
    def _create_synthetic_data(self, symbol: str) -> pd.DataFrame:
        """Create synthetic data as fallback"""
        import numpy as np
        import random
        
        # Base prices for different symbols
        base_prices = {
            'SPY': 475.0,
            'QQQ': 380.0,
            'AAPL': 190.0,
            'MSFT': 380.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Create 100 periods of daily data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=120), 
            periods=100, 
            freq='D'
        )
        
        # Use symbol-specific seed for consistent but different data per symbol
        symbol_seed = hash(symbol) % 1000
        np.random.seed(symbol_seed)
        
        # Generate realistic price movements
        returns = np.random.normal(0, 0.015, 100)  # Daily volatility
        prices = [base_price]
        
        for i in range(1, 100):
            # Add trend and mean reversion
            trend = 0.0005  # Slight upward trend
            mean_reversion = -0.02 * (prices[-1] - base_price) / base_price
            
            price_change = returns[i] + trend + mean_reversion
            new_price = prices[-1] * (1 + price_change)
            prices.append(max(new_price, base_price * 0.85))
        
        # Create OHLC data
        data = []
        for i, close_price in enumerate(prices):
            daily_range = close_price * 0.02  # 2% daily range
            high = close_price + abs(np.random.normal(0, daily_range/4))
            low = close_price - abs(np.random.normal(0, daily_range/4))
            open_price = prices[i-1] * (1 + np.random.normal(0, 0.005)) if i > 0 else close_price
            
            data.append({
                'Open': open_price,
                'High': max(high, close_price, open_price),
                'Low': min(low, close_price, open_price),
                'Close': close_price,
                'Volume': random.randint(80000000, 200000000)
            })
        
        df = pd.DataFrame(data, index=dates)
        print(f"Created synthetic {symbol} data: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
        return df