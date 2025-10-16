# api/scan.py (for Vercel)
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import TradingSignalSystem
from datetime import datetime
import json

def handler(request, context):
    """Vercel serverless function handler"""
    try:
        system = TradingSignalSystem()
        signals = system.run_scan()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'success': True,
                'message': f'Scan completed at {datetime.now().isoformat()}',
                'signals_generated': len(signals),
                'timestamp': datetime.now().isoformat()
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }
