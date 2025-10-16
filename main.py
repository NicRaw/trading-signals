from dotenv import load_dotenv
load_dotenv()

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

from config.settings import StrategyConfig, EmailConfig
from strategies.the_system import TheSystemStrategy
from data.market_data import MarketDataFetcher
from notifications.email_notifier import EmailNotifier
from utils.market_hours import is_market_hours
from strategies.base_strategy import Signal

class StateManager:
    """Manages signal state to detect changes"""
    
    def __init__(self, state_file: str = "state/last_signal.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(exist_ok=True)
    
    def load_last_state(self) -> Optional[Dict]:
        """Load the last known signal state"""
        if not self.state_file.exists():
            return None
        
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state: {e}")
            return None
    
    def save_current_state(self, signals: List[Signal]):
        """Save current signal state"""
        if not signals:
            state = {
                'timestamp': datetime.now().isoformat(),
                'signal_type': None,
                'confidence': 0,
                'price': 0
            }
        else:
            # Save highest confidence signal
            top_signal = max(signals, key=lambda s: s.confidence)
            state = {
                'timestamp': datetime.now().isoformat(),
                'signal_type': top_signal.signal_type,
                'confidence': top_signal.confidence,
                'price': top_signal.current_price,
                'action': top_signal.action
            }
        
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"State saved: {state['signal_type'] or 'No signal'}")
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def has_state_changed(self, current_signals: List[Signal]) -> bool:
        """Check if signal state has changed meaningfully"""
        last_state = self.load_last_state()
        
        # First run - always notify
        if last_state is None:
            print("First run - will send notification")
            return True
        
        # Current state
        if not current_signals:
            current_signal_type = None
            current_confidence = 0
        else:
            top_signal = max(current_signals, key=lambda s: s.confidence)
            current_signal_type = top_signal.signal_type
            current_confidence = top_signal.confidence
        
        last_signal_type = last_state.get('signal_type')
        last_confidence = last_state.get('confidence', 0)
        
        # Check for changes
        signal_type_changed = current_signal_type != last_signal_type
        
        # Significant confidence change (>15% change)
        confidence_changed_significantly = abs(current_confidence - last_confidence) > 15
        
        # New signal appeared
        new_signal_appeared = last_signal_type is None and current_signal_type is not None
        
        # Signal disappeared
        signal_disappeared = last_signal_type is not None and current_signal_type is None
        
        if signal_type_changed:
            print(f"Signal type changed: {last_signal_type} → {current_signal_type}")
            return True
        
        if new_signal_appeared:
            print(f"New signal appeared: {current_signal_type}")
            return True
        
        if signal_disappeared:
            print(f"Signal disappeared (was: {last_signal_type})")
            return True
        
        if current_signal_type and confidence_changed_significantly:
            print(f"Significant confidence change: {last_confidence}% → {current_confidence}%")
            return True
        
        print(f"No significant state change (current: {current_signal_type}, {current_confidence}%)")
        return False

class TradingSignalSystem:
    def __init__(self):
        print("Initializing Trading Signal System...")
        
        # Verify environment
        email_config = EmailConfig()
        if not email_config.sender_email:
            print("WARNING: Email not configured")
        else:
            print(f"Email configured for: {email_config.sender_email}")
        
        self.strategies = []
        self.data_fetcher = MarketDataFetcher()
        self.email_notifier = EmailNotifier(email_config)
        self.state_manager = StateManager()
        
        # Load enabled strategies
        if StrategyConfig.THE_SYSTEM['enabled']:
            self.strategies.append(TheSystemStrategy(StrategyConfig.THE_SYSTEM))
    
    def run_scan(self, force_notify: bool = False) -> List[Signal]:
        """Run scan and notify only on state changes"""
        print(f"\n{'='*60}")
        print(f"Trading Signal Scan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Check market hours
        market_open = is_market_hours()
        print(f"Market status: {'OPEN' if market_open else 'CLOSED'}")
        
        if not market_open:
            print("Market closed - skipping scan")
            return []
        
        all_signals = []
        
        # Run all strategies
        for strategy in self.strategies:
            try:
                print(f"\nRunning strategy: {strategy.name}")
                
                # Get required data
                data_req = strategy.get_required_data()
                
                if 'symbols' in data_req:
                    symbols = data_req['symbols']
                    print(f"Fetching data for: {', '.join(symbols)}")
                    
                    market_data = self.data_fetcher.get_data(
                        symbols,
                        data_req['timeframe'], 
                        data_req['periods']
                    )
                    
                    if not market_data or all(df.empty for df in market_data.values()):
                        print(f"No data available for {strategy.name}")
                        continue
                    
                    print(f"Data fetched: {', '.join([f'{s} ({len(d)} pts)' for s, d in market_data.items()])}")
                    
                    signals = strategy.analyze(market_data)
                
                else:
                    print(f"Invalid data requirements for {strategy.name}")
                    continue
                
                # Filter by confidence
                min_confidence = strategy.config.get('min_confidence', 0)
                valid_signals = [s for s in signals if s.confidence >= min_confidence]
                
                all_signals.extend(valid_signals)
                
                if valid_signals:
                    print(f"\n✓ Generated {len(valid_signals)} signal(s):")
                    for signal in valid_signals:
                        print(f"  • {signal.signal_type}: {signal.confidence}% confidence")
                        print(f"    Action: {signal.action}")
                else:
                    print(f"No signals met minimum confidence threshold ({min_confidence}%)")
                
            except Exception as e:
                print(f"Error running {strategy.name}: {e}")
                import traceback
                traceback.print_exc()
        
        # Check if state changed
        state_changed = self.state_manager.has_state_changed(all_signals) or force_notify
        
        # Save current state
        self.state_manager.save_current_state(all_signals)
        
        # Send notifications only if state changed
        if state_changed and all_signals:
            print(f"\n{'='*60}")
            print("State changed - sending notification")
            print(f"{'='*60}")
            
            if not self.email_notifier.config.sender_email:
                print("Email not configured - skipping notification")
            else:
                success = self.email_notifier.send_signals(all_signals)
                if success:
                    print("✓ Email notification sent")
                else:
                    print("✗ Failed to send email")
        elif state_changed:
            print("\nState changed but no signals - not sending notification")
        else:
            print("\nNo state change - skipping notification")
        
        return all_signals

def main():
    """Main entry point"""
    system = TradingSignalSystem()
    
    # Check for force notify flag (for testing)
    force_notify = '--force' in os.sys.argv
    
    signals = system.run_scan(force_notify=force_notify)
    
    print(f"\n{'='*60}")
    print(f"Scan completed - {len(signals)} signal(s) found")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
