# test_signals.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from strategies.the_system import TheSystemStrategy
from config.settings import StrategyConfig

def create_crossover_data():
    """Create test data with a golden cross pattern"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=3), periods=100, freq='30min')
    
    # Create data where 10SMA crosses above 50SMA at the end
    prices = []
    base = 470
    
    # First 80 points: 10SMA below 50SMA (bearish)
    for i in range(80):
        price = base + (i * 0.1) + np.random.normal(0, 0.5)
        prices.append(price)
    
    # Last 20 points: Sharp rise to create golden cross
    for i in range(20):
        price = prices[-1] + (2 + i * 0.3) + np.random.normal(0, 0.3)
        prices.append(price)
    
    data = pd.DataFrame({
        'Open': prices,
        'High': [p * 1.005 for p in prices],
        'Low': [p * 0.995 for p in prices],
        'Close': prices,
        'Volume': [100000000] * 100
    }, index=dates)
    
    return data

def test_signal_generation():
    print("Testing signal generation with forced crossover...")
    
    # Create strategy
    strategy = TheSystemStrategy(StrategyConfig.THE_SYSTEM)
    
    # Create test data with crossover
    data = create_crossover_data()
    
    # Calculate SMAs to verify crossover
    data['SMA_10'] = data['Close'].rolling(10).mean()
    data['SMA_50'] = data['Close'].rolling(50).mean()
    
    print(f"Latest price: ${data['Close'].iloc[-1]:.2f}")
    print(f"10SMA: ${data['SMA_10'].iloc[-1]:.2f}")
    print(f"50SMA: ${data['SMA_50'].iloc[-1]:.2f}")
    print(f"Previous 10SMA: ${data['SMA_10'].iloc[-2]:.2f}")
    print(f"Previous 50SMA: ${data['SMA_50'].iloc[-2]:.2f}")
    
    # Check for crossover
    current_cross = data['SMA_10'].iloc[-1] > data['SMA_50'].iloc[-1]
    previous_cross = data['SMA_10'].iloc[-2] > data['SMA_50'].iloc[-2]
    
    print(f"Crossover occurred: {not previous_cross and current_cross}")
    
    # Run strategy
    signals = strategy.analyze(data)
    
    print(f"\nGenerated {len(signals)} signals:")
    for signal in signals:
        print(f"- {signal.signal_type}: {signal.action}")
        print(f"  Confidence: {signal.confidence}%")
        print(f"  Notes: {signal.notes}")

if __name__ == "__main__":
    test_signal_generation()