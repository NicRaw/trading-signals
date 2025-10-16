from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

@dataclass
class EmailConfig:
    enabled: bool = True
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = os.getenv("SENDER_EMAIL", "")
    sender_password: str = os.getenv("SENDER_PASSWORD", "")
    recipient_email: str = os.getenv("RECIPIENT_EMAIL", "")

@dataclass
class DataConfig:
    alphavantage_api_key: str = os.getenv("ALPHAVANTAGE_API_KEY", "")
    cache_duration_minutes: int = 5

@dataclass
class MarketConfig:
    timezone: str = "US/Eastern"
    market_open: str = "09:30"
    market_close: str = "16:00"
    scan_interval: int = 30

class StrategyConfig:
    THE_SYSTEM = {
        'enabled': True,
        'sma_10_period': 10,
        'sma_50_period': 50,
        'timeframe': '1d',  # Alpha Vantage gives us daily data
        'min_confidence': 60,
        'oversold_threshold': -3.0,
        'overbought_threshold': 3.0
    }