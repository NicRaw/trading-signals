from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass
class Signal:
    strategy_name: str
    symbol: str
    signal_type: str  # 'BUY_CROSS', 'SELL_CROSS', 'BOUNCE', 'CASH', 'SHORT'
    confidence: float  # 0-100
    timestamp: datetime
    current_price: float
    sma_10: float
    sma_50: float
    distance_from_50sma: float  # percentage
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    notes: str = ""
    action: str = ""  # What to do on Trading212

class BaseStrategy(ABC):
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> List[Signal]:
        pass
    
    @abstractmethod
    def get_required_data(self) -> Dict:
        pass