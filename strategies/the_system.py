# strategies/the_system.py - Enhanced version with all missing elements
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from .base_strategy import BaseStrategy, Signal

class TheSystemStrategy(BaseStrategy):
    def __init__(self, config: Dict):
        super().__init__("The System", config)
        
        # Moving average periods
        self.sma_10 = config.get('sma_10_period', 10)
        self.sma_50 = config.get('sma_50_period', 50)
        self.sma_200 = config.get('sma_200_period', 200)
        self.ema_9 = config.get('ema_9_period', 9)
        self.ema_21 = config.get('ema_21_period', 21)
        
        # Thresholds
        self.oversold_threshold = config.get('oversold_threshold', -3.0)
        self.overbought_threshold = config.get('overbought_threshold', 3.0)
        
        # NASDAQ analysis settings
        self.nasdaq_weight = config.get('nasdaq_confirmation_weight', 0.3)
        self.nasdaq_lookback = config.get('nasdaq_lookback_days', 5)
        
        # Fed calendar (simplified - in production could use economic calendar API)
        self.fed_blackout_dates = self._get_fed_calendar()
        
        # Higher timeframe settings
        self.check_higher_timeframes = config.get('check_higher_timeframes', True)
        
    def get_required_data(self) -> Dict:
        return {
            'symbols': ['SPY', 'QQQ'],  # SPY for signals, QQQ for NASDAQ analysis
            'timeframe': self.config['timeframe'],
            'periods': max(self.sma_200, 100) + 20  # Ensure enough data for 200SMA
        }
    
    def debug_analysis(self, spy_data, nasdaq_data):
        """Debug function to see why no signals are generated"""
        
        # Calculate basic state
        spy_data = self._calculate_all_moving_averages(spy_data)
        market_state = self._analyze_current_market_state(spy_data, nasdaq_data)
        
        print("\nDEBUG - Market State Analysis:")
        print(f"  Current price: ${market_state['current_price']:.2f}")
        print(f"  10SMA: ${market_state['sma_10']:.2f}")
        print(f"  50SMA: ${market_state['sma_50']:.2f}")
        print(f"  Distance from 50SMA: {market_state['distance_50sma']:.1f}%")
        print(f"  SMA trend: {market_state['sma_trend']}")
        print(f"  EMA trend: {market_state['ema_trend']}")
        print(f"  Overbought threshold: {self.overbought_threshold}%")
        
        print(f"\nDEBUG - Signal Conditions:")
        print(f"  Is distance > overbought threshold? {market_state['distance_50sma']} > {self.overbought_threshold} = {market_state['distance_50sma'] > self.overbought_threshold}")
        print(f"  Is SMA trend bullish? {market_state['sma_trend'] == 'bullish'}")
        
        # Check NASDAQ analysis
        nasdaq_analysis = market_state['nasdaq_analysis']
        print(f"\nDEBUG - NASDAQ Analysis:")
        print(f"  Leadership: {nasdaq_analysis['leadership']}")
        print(f"  Confidence modifier: {nasdaq_analysis['confidence_modifier']}")
        print(f"  Note: {nasdaq_analysis['note']}")
    
    def analyze(self, data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """Enhanced analysis incorporating all System elements"""
        spy_data = data.get('SPY')
        nasdaq_data = data.get('QQQ')  # Using QQQ as NASDAQ proxy
        
        if spy_data is None or spy_data.empty:
            return []
            
        # Check minimum data requirements - need at least 50 periods for basic analysis
        min_required = max(self.sma_50, 50)
        if len(spy_data) < min_required:
            print(f"Insufficient data: {len(spy_data)} points, need at least {min_required}")
            return []
        
        # Check for Fed event (flag but don't block)
        fed_warning = self._get_fed_warning()
        
        signals = []
        
        # Calculate all moving averages
        spy_data = self._calculate_all_moving_averages(spy_data)
        
        # Get current market state
        market_state = self._analyze_current_market_state(spy_data, nasdaq_data)
        
        ##FOR DEBUGGING PURPOSES##
        self.debug_analysis(spy_data, nasdaq_data)
        
        # Generate signals based on comprehensive analysis
        signals.extend(self._check_crossover_signals(spy_data, market_state, fed_warning))
        signals.extend(self._check_bounce_signals(spy_data, market_state, fed_warning))
        signals.extend(self._check_profit_taking_signals(spy_data, market_state, fed_warning))
        
        return signals
    
    def _calculate_all_moving_averages(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all required moving averages"""
        # Simple Moving Averages
        data['SMA_10'] = data['Close'].rolling(window=self.sma_10).mean()
        data['SMA_50'] = data['Close'].rolling(window=self.sma_50).mean()
        
        # Only calculate 200SMA if we have enough data
        if len(data) >= self.sma_200:
            data['SMA_200'] = data['Close'].rolling(window=self.sma_200).mean()
            print(f"Calculated 200SMA with {len(data)} data points")
        else:
            data['SMA_200'] = None
            print(f"Skipping 200SMA calculation - only {len(data)} data points available (need {self.sma_200})")
        
        # Exponential Moving Averages
        data['EMA_9'] = data['Close'].ewm(span=self.ema_9).mean()
        data['EMA_21'] = data['Close'].ewm(span=self.ema_21).mean()
        
        return data
    
    def _analyze_current_market_state(self, spy_data: pd.DataFrame, nasdaq_data: pd.DataFrame) -> Dict:
        """Comprehensive market state analysis"""
        current = spy_data.iloc[-1]
        previous = spy_data.iloc[-2]
        
        # Basic price and MA data
        current_price = current['Close']
        current_sma_10 = current['SMA_10']
        current_sma_50 = current['SMA_50']
        current_sma_200 = current['SMA_200']
        current_ema_9 = current['EMA_9']
        current_ema_21 = current['EMA_21']
        
        # Distance calculations  
        distance_50sma = ((current_price - current_sma_50) / current_sma_50) * 100
        
        # Only calculate 200SMA distance if we have 200SMA data
        if current_sma_200 is not None and not pd.isna(current_sma_200):
            distance_200sma = ((current_price - current_sma_200) / current_sma_200) * 100
            long_term_trend = "bullish" if current_price > current_sma_200 else "bearish"
        else:
            distance_200sma = None
            long_term_trend = "unknown (insufficient data)"
        
        # Trend analysis
        sma_trend = "bullish" if current_sma_10 > current_sma_50 else "bearish"
        ema_trend = "bullish" if current_ema_9 > current_ema_21 else "bearish"
        
        # NASDAQ analysis
        nasdaq_analysis = self._analyze_nasdaq_leadership(spy_data, nasdaq_data)
        
        # Higher timeframe context (simplified - using longer MAs as proxy)
        higher_tf_context = self._analyze_higher_timeframe_context(spy_data)
        
        return {
            'current_price': current_price,
            'sma_10': current_sma_10,
            'sma_50': current_sma_50,
            'sma_200': current_sma_200,
            'ema_9': current_ema_9,
            'ema_21': current_ema_21,
            'distance_50sma': distance_50sma,
            'distance_200sma': distance_200sma,
            'sma_trend': sma_trend,
            'ema_trend': ema_trend,
            'long_term_trend': long_term_trend,
            'nasdaq_analysis': nasdaq_analysis,
            'higher_tf_context': higher_tf_context,
            'previous_sma_10': previous['SMA_10'],
            'previous_sma_50': previous['SMA_50']
        }
    
    def _analyze_nasdaq_leadership(self, spy_data: pd.DataFrame, nasdaq_data: pd.DataFrame) -> Dict:
        """Analyze NASDAQ leadership vs SPY"""
        if nasdaq_data is None or nasdaq_data.empty or len(nasdaq_data) < self.nasdaq_lookback:
            return {
                'relative_strength': 0,
                'leadership': 'unknown',
                'confidence_modifier': 0,
                'note': 'No NASDAQ data available'
            }
        
        # Calculate recent performance
        spy_recent = spy_data['Close'].iloc[-self.nasdaq_lookback:]
        nasdaq_recent = nasdaq_data['Close'].iloc[-self.nasdaq_lookback:]
        
        if len(spy_recent) != len(nasdaq_recent):
            # Align data if different lengths
            min_len = min(len(spy_recent), len(nasdaq_recent))
            spy_recent = spy_recent.iloc[-min_len:]
            nasdaq_recent = nasdaq_recent.iloc[-min_len:]
        
        # Calculate relative performance over lookback period
        spy_return = (spy_recent.iloc[-1] - spy_recent.iloc[0]) / spy_recent.iloc[0]
        nasdaq_return = (nasdaq_recent.iloc[-1] - nasdaq_recent.iloc[0]) / nasdaq_recent.iloc[0]
        
        relative_strength = nasdaq_return - spy_return
        
        # Determine leadership
        if relative_strength > 0.005:  # NASDAQ outperforming by >0.5%
            leadership = 'nasdaq_leading'
            confidence_modifier = 0.2  # Boost bullish signals
        elif relative_strength < -0.005:  # NASDAQ underperforming by >0.5%
            leadership = 'nasdaq_lagging'
            confidence_modifier = -0.2  # Reduce bullish signals
        else:
            leadership = 'neutral'
            confidence_modifier = 0
        
        return {
            'relative_strength': relative_strength,
            'leadership': leadership,
            'confidence_modifier': confidence_modifier,
            'spy_return': spy_return,
            'nasdaq_return': nasdaq_return,
            'note': f"NASDAQ {'leading' if relative_strength > 0 else 'lagging'} by {abs(relative_strength)*100:.1f}%"
        }
    
    def _analyze_higher_timeframe_context(self, data: pd.DataFrame) -> Dict:
        """Analyze higher timeframe context using longer period MAs"""
        if len(data) < 100:
            return {'context': 'insufficient_data', 'note': 'Not enough data for higher TF analysis'}
        
        # Use longer period MAs as proxy for higher timeframes
        long_sma_10 = data['Close'].rolling(window=20).mean()  # ~1hr equivalent
        long_sma_50 = data['Close'].rolling(window=100).mean()  # ~4hr equivalent
        
        current_price = data['Close'].iloc[-1]
        current_long_10 = long_sma_10.iloc[-1]
        current_long_50 = long_sma_50.iloc[-1]
        
        # Determine higher timeframe trend
        if current_price > current_long_10 > current_long_50:
            context = 'strong_bullish'
        elif current_price > current_long_50:
            context = 'bullish'
        elif current_price < current_long_10 < current_long_50:
            context = 'strong_bearish'
        elif current_price < current_long_50:
            context = 'bearish'
        else:
            context = 'mixed'
        
        return {
            'context': context,
            'long_ma_10': current_long_10,
            'long_ma_50': current_long_50,
            'note': f"Higher TF: {context.replace('_', ' ').title()}"
        }
    
    def _check_crossover_signals(self, data: pd.DataFrame, market_state: Dict, fed_warning: str) -> List[Signal]:
        """Check for SMA and EMA crossover signals with confirmations"""
        signals = []
        
        # SMA Crossover Analysis
        prev_sma_10 = market_state['previous_sma_10']
        prev_sma_50 = market_state['previous_sma_50']
        current_sma_10 = market_state['sma_10']
        current_sma_50 = market_state['sma_50']
        
        # EMA Confirmation
        ema_9 = market_state['ema_9']
        ema_21 = market_state['ema_21']
        ema_confirms_bullish = ema_9 > ema_21
        ema_confirms_bearish = ema_9 < ema_21
        
        # Golden Cross (10SMA crosses above 50SMA)
        bullish_cross = (prev_sma_10 <= prev_sma_50) and (current_sma_10 > current_sma_50)
        
        if bullish_cross and market_state['current_price'] > current_sma_50:
            confidence = 85
            
            # Apply confirmations
            nasdaq_boost = market_state['nasdaq_analysis']['confidence_modifier']
            confidence += nasdaq_boost * 100
            
            # EMA confirmation
            if ema_confirms_bullish:
                confidence += 5
                ema_note = "EMA confirms bullish momentum"
            else:
                confidence -= 10
                ema_note = "EMA shows mixed signals"
            
            # Higher timeframe confirmation
            if market_state['higher_tf_context']['context'] in ['strong_bullish', 'bullish']:
                confidence += 5
                htf_note = "Higher timeframes support"
            else:
                confidence -= 10
                htf_note = "Higher timeframes show resistance"
            
            # 200SMA context (only if we have data)
            if market_state['current_price'] > market_state['sma_200'] if market_state['sma_200'] is not None else True:
                if market_state['sma_200'] is not None:
                    sma200_note = "Above 200SMA (bullish long-term)"
                else:
                    sma200_note = "200SMA unavailable (insufficient data)"
            else:
                confidence -= 15
                sma200_note = "Below 200SMA (bearish long-term)"
            
            confidence = max(min(confidence, 100), 0)  # Clamp to 0-100
            
            # Build notes with Fed warning if applicable
            notes = f"Golden cross confirmed! {ema_note}. {htf_note}. {sma200_note}. {market_state['nasdaq_analysis']['note']}"
            if fed_warning:
                notes = f"🚨 {fed_warning} 🚨 {notes}"
            
            signals.append(Signal(
                strategy_name=self.name,
                symbol='SPY',
                signal_type='BUY_CROSS',
                confidence=confidence,
                timestamp=datetime.now(),
                current_price=market_state['current_price'],
                sma_10=current_sma_10,
                sma_50=current_sma_50,
                distance_from_50sma=market_state['distance_50sma'],
                stop_loss=current_sma_50 * 0.99,
                action="BUY SPY calls or UPRO shares",
                notes=notes
            ))
        
        # Death Cross (10SMA crosses below 50SMA)
        bearish_cross = (prev_sma_10 >= prev_sma_50) and (current_sma_10 < current_sma_50)
        
        if bearish_cross:
            confidence = 85
            
            # Apply confirmations
            nasdaq_impact = market_state['nasdaq_analysis']['confidence_modifier']
            confidence -= nasdaq_impact * 100  # Reverse for bearish signal
            
            # EMA confirmation
            if ema_confirms_bearish:
                confidence += 5
                ema_note = "EMA confirms bearish momentum"
            else:
                confidence -= 10
                ema_note = "EMA shows mixed signals"
            
            # Determine action based on market conditions
            distance = market_state['distance_50sma']
            if distance > -2:
                action = "GO TO CASH (sell positions)"
            else:
                action = "GO SHORT (SPY puts or SPXU shares)"
            
            confidence = max(min(confidence, 100), 0)
            
            # Build notes with Fed warning if applicable
            notes = f"Death cross! {ema_note}. {market_state['nasdaq_analysis']['note']}"
            if fed_warning:
                notes = f"🚨 {fed_warning} 🚨 {notes}"
            
            signals.append(Signal(
                strategy_name=self.name,
                symbol='SPY',
                signal_type='SELL_CROSS',
                confidence=confidence,
                timestamp=datetime.now(),
                current_price=market_state['current_price'],
                sma_10=current_sma_10,
                sma_50=current_sma_50,
                distance_from_50sma=distance,
                action=action,
                notes=notes
            ))
        
        return signals
    
    def _check_bounce_signals(self, data: pd.DataFrame, market_state: Dict, fed_warning: str) -> List[Signal]:
        """Check for oversold bounce opportunities"""
        signals = []
        
        distance = market_state['distance_50sma']
        current_price = market_state['current_price']
        sma_10 = market_state['sma_10']
        
        # Only consider bounces in oversold conditions
        if distance < self.oversold_threshold and current_price > sma_10:
            # Additional confirmations for bounce signals
            confidence = 70
            
            # Check if near 200SMA support (only if we have 200SMA data)
            distance_200 = market_state['distance_200sma']
            if distance_200 is not None and abs(distance_200) < 2:  # Within 2% of 200SMA
                confidence += 10
                sma200_note = "Near 200SMA support"
            elif distance_200 is not None:
                sma200_note = f"{distance_200:.1f}% from 200SMA"
            else:
                sma200_note = "200SMA unavailable (insufficient data)"
            
            # NASDAQ confirmation
            if market_state['nasdaq_analysis']['leadership'] == 'nasdaq_leading':
                confidence += 10
                nasdaq_note = "NASDAQ showing leadership"
            else:
                nasdaq_note = market_state['nasdaq_analysis']['note']
            
            # Higher timeframe check
            htf_context = market_state['higher_tf_context']['context']
            if htf_context in ['strong_bearish', 'bearish']:
                confidence -= 20
                htf_note = "Higher timeframes bearish - risky bounce"
            else:
                htf_note = "Higher timeframes neutral/bullish"
            
            confidence = max(min(confidence, 100), 0)
            
            # Build notes with Fed warning if applicable
            notes = f"Oversold bounce setup! {distance:.1f}% below 50SMA. {sma200_note}. {nasdaq_note}. {htf_note}"
            if fed_warning:
                notes = f"🚨 {fed_warning} 🚨 {notes}"
            
            signals.append(Signal(
                strategy_name=self.name,
                symbol='SPY',
                signal_type='BOUNCE',
                confidence=confidence,
                timestamp=datetime.now(),
                current_price=current_price,
                sma_10=sma_10,
                sma_50=market_state['sma_50'],
                distance_from_50sma=distance,
                stop_loss=sma_10 * 0.995,
                action="SMALL POSITION: SPY calls (short-term bounce play)",
                notes=notes
            ))
        
        return signals
    
    def _check_profit_taking_signals(self, data: pd.DataFrame, market_state: Dict, fed_warning: str) -> List[Signal]:
        """Check for overbought profit-taking opportunities"""
        signals = []
        
        distance = market_state['distance_50sma']
        
        # Enhanced overbought analysis
        if distance > self.overbought_threshold and market_state['sma_trend'] == 'bullish':
            confidence = 60
            
            # Check multiple timeframe alignment
            htf_context = market_state['higher_tf_context']['context']
            if htf_context == 'strong_bullish':
                confidence -= 15  # Less urgent to take profits in strong uptrend
                htf_note = "Strong uptrend - consider partial profits only"
            elif htf_context in ['mixed', 'bearish']:
                confidence += 15  # More urgent in weakening trend
                htf_note = "Higher timeframes weakening - good time for profits"
            else:
                htf_note = "Monitor higher timeframes"
            
            # NASDAQ divergence check
            nasdaq_leadership = market_state['nasdaq_analysis']['leadership']
            if nasdaq_leadership == 'nasdaq_lagging':
                confidence += 10
                nasdaq_note = "NASDAQ lagging - concerning for tech leadership"
            else:
                nasdaq_note = market_state['nasdaq_analysis']['note']
            
            # Distance from 200SMA (only if we have 200SMA data)
            distance_200 = market_state['distance_200sma']
            if distance_200 is not None and distance_200 > 10:  # Very extended from long-term average
                confidence += 10
                sma200_note = f"Very extended: {distance_200:.1f}% above 200SMA"
            elif distance_200 is not None:
                sma200_note = f"{distance_200:.1f}% above 200SMA"
            else:
                sma200_note = "200SMA unavailable (insufficient data)"
            
            confidence = max(min(confidence, 100), 0)
            print(f"DEBUG - Overbought signal confidence: {confidence}%")
            
            # Build notes with Fed warning if applicable
            notes = f"Overbought: {distance:.1f}% above 50SMA. {sma200_note}. {nasdaq_note}. {htf_note}"
            if fed_warning:
                notes = f"🚨 {fed_warning} 🚨 {notes}"
            
            signals.append(Signal(
                strategy_name=self.name,
                symbol='SPY',
                signal_type='OVERBOUGHT',
                confidence=confidence,
                timestamp=datetime.now(),
                current_price=market_state['current_price'],
                sma_10=market_state['sma_10'],
                sma_50=market_state['sma_50'],
                distance_from_50sma=distance,
                action="CONSIDER PROFIT TAKING on long positions",
                notes=notes
            ))
        
        return signals
    
    def _get_fed_warning(self) -> str:
        """Get Fed event warning if applicable"""
        today = datetime.now().date()
        
        for blackout_date in self.fed_blackout_dates:
            days_diff = (blackout_date - today).days
            
            if days_diff == 0:
                return "FED MEETING TODAY - EXTREME VOLATILITY EXPECTED"
            elif days_diff == 1:
                return "FED MEETING TOMORROW - HIGH VOLATILITY LIKELY"
            elif days_diff == -1:
                return "FED MEETING YESTERDAY - VOLATILITY MAY CONTINUE"
            elif abs(days_diff) <= 2:
                return f"FED MEETING IN {abs(days_diff)} DAYS - CONSIDER VOLATILITY RISK"
        
        return ""
    
    def _get_fed_calendar(self) -> List:
        """Get Fed calendar dates (simplified version)"""
        # In production, this could integrate with economic calendar APIs
        # For now, using approximate 2025 FOMC meeting dates
        from datetime import date
        
        return [
            date(2025, 1, 29),  # FOMC Meeting
            date(2025, 3, 19),  # FOMC Meeting
            date(2025, 5, 1),   # FOMC Meeting
            date(2025, 6, 18),  # FOMC Meeting
            date(2025, 7, 30),  # FOMC Meeting
            date(2025, 9, 17),  # FOMC Meeting (today's date for testing)
            date(2025, 11, 6),  # FOMC Meeting
            date(2025, 12, 17), # FOMC Meeting
        ]

# Enhanced configuration for the strategy
class EnhancedStrategyConfig:
    THE_SYSTEM = {
        'enabled': True,
        'sma_10_period': 10,
        'sma_50_period': 50,
        'sma_200_period': 200,
        'ema_9_period': 9,
        'ema_21_period': 21,
        'timeframe': '1d',
        'min_confidence': 60,
        'oversold_threshold': -3.0,
        'overbought_threshold': 3.0,
        'nasdaq_confirmation_weight': 0.3,
        'nasdaq_lookback_days': 5,
        'check_higher_timeframes': True,
        'enable_fed_calendar': True
    }