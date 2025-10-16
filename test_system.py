import os
os.environ['SENDER_EMAIL'] = 'nntrawhani@gmail.com'  # Temporary for testing
os.environ['SENDER_PASSWORD'] = 'cuiiudovetekuglq'
os.environ['RECIPIENT_EMAIL'] = 'nic@vula.vc'

from main import TradingSignalSystem

print("Testing system initialization...")
system = TradingSignalSystem()
print("System initialized successfully!")

print("Testing data fetch...")
signals = system.run_scan()
print(f"Test completed. Found {len(signals)} signals.")