# 📈 Algorithmic Trading Signal System

```
 ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌     ▐░░▌
 ▀▀▀▀█░█▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌   ▐░▐░▌
     ▐░▌     ▐░▌       ▐░▌▐░▌               ▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌          ▐░▌▐░▌ ▐░▌▐░▌
     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▐░▌ ▐░▌
     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌
     ▐░▌     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌   ▀   ▐░▌
     ▐░▌     ▐░▌       ▐░▌▐░▌                         ▐░▌     ▐░▌               ▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌
     ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌      ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌
     ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌
      ▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀ 
```

> **A production-ready, modular algorithmic trading system that analyzes market conditions and sends intelligent alerts only when conditions change.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://img.shields.io/badge/automated-GitHub%20Actions-green.svg)](https://github.com/features/actions)
[![Cost: $0](https://img.shields.io/badge/cost-$0-success.svg)](https://github.com)

---

## 🚀 What Is This?

This is a **sophisticated trading signal system** that monitors market conditions 24/7 and sends you email alerts when trading opportunities arise. Built with a modular architecture, it currently implements **"The System"** by @TraderBrianJones - a proven moving average crossover strategy used by professional traders.

**Smart notifications**: You only get alerted when market conditions **change**, not every 30 minutes. No spam, just actionable signals.

### ✨ Key Features

- 📊 **Multi-Strategy Architecture** - Easily add and manage multiple trading strategies
- 🧠 **Intelligent State Tracking** - Only alerts on meaningful changes
- 📧 **Email Notifications** - Detailed, pyramid-structured alerts with full technical analysis
- 🔄 **Automated Scanning** - Runs every 30 minutes during market hours via GitHub Actions
- 📈 **Real Market Data** - Powered by Alpha Vantage API
- 🎯 **Configurable** - Granular parameter control with preset configurations
- 💰 **Completely Free** - Zero cost to run ($0/month)

---

## 🎯 Current Strategy: "The System"

Implements Brian Jones' "The System" - a comprehensive moving average strategy that includes:

- **10/50 SMA Crossovers** - Golden/Death cross signals
- **9/21 EMA Confirmations** - Short-term momentum validation  
- **NASDAQ Leadership Analysis** - Relative strength vs S&P 500
- **Higher Timeframe Context** - Multi-timeframe trend analysis
- **200 SMA Long-term Trend** - Market regime identification
- **Fed Calendar Integration** - Volatility warnings during FOMC meetings
- **Oversold Bounce Detection** - Counter-trend opportunity identification
- **Overbought Profit Taking** - Exit signal generation

### Signal Types

| Signal | Action | Confidence | Description |
|--------|--------|------------|-------------|
| 🟢 **BUY_CROSS** | Buy SPY calls/UPRO | 70-100% | Golden cross confirmed with confirmations |
| 🔴 **SELL_CROSS** | Go to cash/short | 70-100% | Death cross - exit or short positions |
| 🔵 **BOUNCE** | Small long position | 60-80% | Oversold bounce opportunity |
| 🟡 **OVERBOUGHT** | Take profits | 45-75% | Extended move - consider profit taking |

---

## 📦 Quick Start

### Prerequisites

- Python 3.9+
- GitHub account (for automated deployment)
- Gmail account (for notifications)
- Alpha Vantage API key (free)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/trading-signals.git
cd trading-signals

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Test the system
python main.py --force
```

### Environment Variables

Create a `.env` file in the root directory:

```env
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_phone_email@gmail.com
ALPHAVANTAGE_API_KEY=your_alphavantage_key
```

**Getting API Keys:**

1. **Gmail App Password**: 
   - Enable 2FA on your Google account
   - Go to [Google Account → Security → App Passwords](https://myaccount.google.com/apppasswords)
   - Generate a new app password for "Mail"

2. **Alpha Vantage API Key**:
   - Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Enter your email to get a free API key instantly

---

## ☁️ Cloud Deployment (GitHub Actions)

### Why GitHub Actions?

- ✅ **Completely free** for public repositories
- ✅ **2000 minutes/month** free (more than enough)
- ✅ **Reliable cron scheduling** every 30 minutes
- ✅ **Full audit logs** of every scan
- ✅ **No server management** required

### Deployment Steps

1. **Fork or Clone This Repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/trading-signals.git
   cd trading-signals
   ```

2. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/trading-signals.git
   git push -u origin main
   ```

3. **Add GitHub Secrets**
   
   Navigate to: `Your Repo → Settings → Secrets and variables → Actions`
   
   Click **"New repository secret"** and add:
   
   | Secret Name | Value |
   |-------------|-------|
   | `SENDER_EMAIL` | Your Gmail address |
   | `SENDER_PASSWORD` | Your Gmail app password |
   | `RECIPIENT_EMAIL` | Where to receive alerts |
   | `ALPHAVANTAGE_API_KEY` | Your Alpha Vantage API key |

4. **Enable GitHub Actions**
   - Go to the **Actions** tab in your repo
   - Click **"I understand my workflows, go ahead and enable them"**
   - The workflow will now run automatically every 30 minutes during market hours

5. **Test It**
   - Go to **Actions** → **Trading Signal Scanner**
   - Click **"Run workflow"** → **"Run workflow"**
   - Check the logs to verify everything works

---

## 🔔 How Notifications Work

### Smart State Tracking

The system tracks the last known market state and **only sends notifications when conditions change**:

```
Previous State: No Signal
Current State: OVERBOUGHT (65% confidence)
Action: ✅ SEND NOTIFICATION

Previous State: OVERBOUGHT (65% confidence)
Current State: OVERBOUGHT (67% confidence)  
Action: ❌ NO NOTIFICATION (minor change)

Previous State: OVERBOUGHT (65% confidence)
Current State: OVERBOUGHT (82% confidence)
Action: ✅ SEND NOTIFICATION (>15% confidence change)

Previous State: OVERBOUGHT (65% confidence)
Current State: BUY_CROSS (85% confidence)
Action: ✅ SEND NOTIFICATION (signal type changed)
```

### Notification Triggers

You'll receive an email when:
- ✅ Signal type changes (e.g., OVERBOUGHT → BUY_CROSS)
- ✅ New signal appears (was none, now has signal)
- ✅ Signal disappears (had signal, now none)
- ✅ Confidence changes significantly (>15% change)

You **won't** be spammed with:
- ❌ Repeated notifications for the same signal
- ❌ Minor confidence fluctuations
- ❌ Scans when market is closed

### Email Format

```
Subject: Trading Signal Alert - 1 Signal(s) - 10/16 14:30

🚨 TRADING SIGNALS 🚨
==================================================

SIGNAL #1: OVERBOUGHT
Strategy: The System
Symbol: SPY
Price: $660.00
Confidence: 65%
10SMA: $652.74
50SMA: $638.31
Distance from 50SMA: 3.4%

🎯 ACTION: CONSIDER PROFIT TAKING on long positions
📝 Notes: Overbought condition - 3.4% above 50SMA | Price: $660.00 | 
10SMA: $652.74, 50SMA: $638.31 | Strong uptrend - consider partial 
profits only | NASDAQ leading by 0.6% | Higher timeframes 
neutral/supportive | EMA9: $655.12, EMA21: $645.80
⏰ Time: 10/16/2025 14:30:15
------------------------------

⚠️ IMPORTANT REMINDERS:
• This is a signal, not financial advice
• Verify market conditions before trading
• Use proper position sizing
• Set stop losses once in profit
• Never risk more than you can afford to lose

Generated by Trading Signal System
```

---

## 🏗️ Architecture

### Project Structure

```
trading-signals/
├── .github/
│   └── workflows/
│       └── trading-signals.yml    # GitHub Actions workflow
├── config/
│   └── settings.py                # Configuration management
├── strategies/
│   ├── base_strategy.py           # Abstract strategy interface
│   └── the_system.py              # "The System" implementation
├── data/
│   └── market_data.py             # Multi-symbol data fetcher
├── notifications/
│   └── email_notifier.py          # Email alert system
├── utils/
│   ├── market_hours.py            # Market timing utilities
│   └── helpers.py                 # Helper functions
├── state/
│   └── last_signal.json           # State tracking (committed to repo)
├── main.py                        # Main entry point with state tracking
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
└── README.md                      # This file
```

### Data Flow

```
┌─────────────────┐
│  GitHub Actions │  Every 30 min during market hours
│   Cron Trigger  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Main Scanner   │  Load last state
│   with State    │  ──────────────►  state/last_signal.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Fetcher   │  Fetch SPY + QQQ
│ (Alpha Vantage) │  ──────────────►  Real-time market data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  The System     │  Calculate indicators
│   Strategy      │  Generate signals
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  State Manager  │  Compare states
│                 │  Detect changes
└────────┬────────┘
         │
         ▼
    Changed? ───No───► Skip notification
         │
        Yes
         │
         ▼
┌─────────────────┐
│ Email Notifier  │  Send alert
│                 │  ──────────────►  📧 Your phone/email
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Save State    │  Commit to repo
│                 │  ──────────────►  state/last_signal.json
└─────────────────┘
```

---

## ⚙️ Configuration

### Strategy Configurations

Three preset configurations are available in `strategies/the_system.py`:

#### 1. **Base Configuration** (Default)
Brian Jones' original parameters - balanced approach.
```python
'min_confidence': 60
'oversold_threshold': -3.0
'overbought_threshold': 3.0
```

#### 2. **Conservative Configuration**
Higher confidence requirements, fewer signals.
```python
'min_confidence': 75
'oversold_threshold': -4.0
'overbought_threshold': 2.5
```

#### 3. **Aggressive Configuration**
Lower confidence requirements, more signals.
```python
'min_confidence': 45
'oversold_threshold': -2.5
'overbought_threshold': 3.5
```

To change configuration, edit `config/settings.py`:

```python
# Use conservative settings
from strategies.the_system import StrategyConfigurations

class StrategyConfig:
    THE_SYSTEM = StrategyConfigurations.CONSERVATIVE_THE_SYSTEM
```

### Adding New Strategies

The system is designed for easy strategy expansion:

1. Create new strategy class in `strategies/your_strategy.py`
2. Inherit from `BaseStrategy`
3. Implement `analyze()` and `get_required_data()` methods
4. Add configuration to `config/settings.py`
5. Enable in strategy config

```python
class YourStrategy(BaseStrategy):
    def analyze(self, data) -> List[Signal]:
        # Your strategy logic
        pass
    
    def get_required_data(self) -> Dict:
        return {'symbols': ['SPY'], 'timeframe': '1d', 'periods': 100}
```

---

## 🧪 Testing

### Local Testing

```bash
# Test with force notification (ignores state)
python main.py --force

# Normal test (respects state)
python main.py

# Test data fetching
python -c "from data.market_data import test_multi_symbol_fetching; test_multi_symbol_fetching()"

# Test email
python -c "from dotenv import load_dotenv; load_dotenv(); from test_email import test_email_basic; test_email_basic()"
```

### GitHub Actions Testing

1. Go to **Actions** tab in your repo
2. Select **"Trading Signal Scanner"**
3. Click **"Run workflow"**
4. View logs to see detailed output

---

## 📊 Monitoring & Logs

### GitHub Actions Logs

Every scan generates detailed logs:

```
Market State Analysis:
  Current price: $660.00
  10SMA: $652.74, 50SMA: $638.31
  Distance from 50SMA: 3.4%
  SMA trend: bullish, EMA trend: bullish
  NASDAQ leading by 0.6%
  Higher TF: Bullish

✓ Generated 1 signal(s):
  • OVERBOUGHT: 65% confidence
    Action: CONSIDER PROFIT TAKING on long positions

State changed - sending notification
✓ Email notification sent
```

### State File

Check `state/last_signal.json` to see current state:

```json
{
  "timestamp": "2025-10-16T14:30:00",
  "signal_type": "OVERBOUGHT",
  "confidence": 65,
  "price": 660.0,
  "action": "CONSIDER PROFIT TAKING on long positions"
}
```

---

## 💡 Tips & Best Practices

### Trading Discipline

- ⚠️ **This system generates signals, not financial advice**
- ✅ Always verify market conditions before acting
- ✅ Use proper position sizing (risk 1-2% per trade max)
- ✅ Set stop losses once in profit
- ✅ Never override The System during Fed events without good reason
- ✅ Track your performance to refine parameters

### System Maintenance

- 🔄 **Monitor GitHub Actions** - Check for failed runs
- 📧 **Test email delivery** monthly
- 🔑 **Rotate API keys** if they get rate-limited
- 📊 **Review state changes** to understand market behavior
- 🎯 **Adjust confidence thresholds** based on performance

### Customization Ideas

- 📈 Add more strategies (momentum, mean reversion, etc.)
- 📱 SMS notifications via Twilio
- 📊 Dashboard for visualizing signals
- 🤖 Backtesting framework for strategy optimization
- 📉 Risk management module
- 💬 Discord/Slack integration

---

## 🛠️ Troubleshooting

### Common Issues

**No emails received:**
- ✅ Check spam folder
- ✅ Verify Gmail app password is correct
- ✅ Confirm 2FA is enabled on Google account
- ✅ Test with `python test_email.py`

**GitHub Actions not running:**
- ✅ Check if workflows are enabled (Actions tab)
- ✅ Verify secrets are set correctly
- ✅ Check cron schedule matches your timezone needs
- ✅ Look at Actions logs for errors

**No signals generated:**
- ✅ Market might be closed
- ✅ No state changes detected (this is normal!)
- ✅ Confidence threshold might be too high
- ✅ Check logs for market state analysis

**API rate limits:**
- ✅ Alpha Vantage free tier: 5 calls/min, 500/day
- ✅ System respects rate limits with delays
- ✅ Consider upgrading API tier if needed

---

## 🚧 Roadmap

### Phase 1: Foundation ✅
- [x] Core strategy implementation
- [x] Multi-symbol data fetching
- [x] Email notifications
- [x] State tracking
- [x] GitHub Actions deployment

### Phase 2: Enhancement 🚧
- [ ] Backtesting framework
- [ ] Performance metrics dashboard
- [ ] Additional strategies (momentum, mean reversion)
- [ ] Web interface for configuration
- [ ] Historical signal database

### Phase 3: Advanced 📋
- [ ] Machine learning signal optimization
- [ ] Portfolio management
- [ ] Risk analytics
- [ ] Multi-asset support
- [ ] Advanced charting

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- **Brian Jones** (@TraderBrianJones) - "The System" methodology
- **Alpha Vantage** - Free market data API
- **GitHub Actions** - Free automation platform

---

## ⚠️ Disclaimer

**This software is for educational purposes only.** 

Trading involves substantial risk of loss. Past performance is not indicative of future results. The signals generated by this system are not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

The authors and contributors are not responsible for any financial losses incurred from using this system.

---

## 📬 Contact & Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/trading-signals/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/trading-signals/discussions)
- ⭐ **Star this repo** if you find it useful!

---

<div align="center">

**Built with ❤️ by traders, for traders**

[⬆ Back to Top](#-algorithmic-trading-signal-system)

</div>