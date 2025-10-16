import pytz
from datetime import datetime, time

def is_market_hours() -> bool:
    """Check if US stock market is currently open"""
    et = pytz.timezone('US/Eastern')
    now = datetime.now(et)
    
    # Check if weekend
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Market hours: 9:30 AM - 4:00 PM ET
    market_open = time(9, 30)
    market_close = time(16, 0)
    current_time = now.time()
    
    return market_open <= current_time <= market_close