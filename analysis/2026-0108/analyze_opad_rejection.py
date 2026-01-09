"""
Analyze why OPAD (Offerpad Solutions Inc) was rejected by the trading bot
OPAD showed a massive run: +4.83% during regular hours, +67.11% after hours
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
from datetime import datetime, timedelta
import pytz
from data.webull_data_api import WebullDataAPI
from analysis.pattern_detector import PatternDetector
from core.realtime_trader import RealtimeTrader

def analyze_opad_rejection():
    """Analyze why OPAD trade was rejected"""
    
    ticker = "OPAD"
    print(f"\n{'='*80}")
    print(f"ANALYZING OPAD REJECTION")
    print(f"{'='*80}\n")
    
    # Initialize components
    data_api = WebullDataAPI()
    pattern_detector = PatternDetector()
    trader = RealtimeTrader(min_confidence=0.72)
    
    # Get current time in ET
    et = pytz.timezone('US/Eastern')
    now_et = datetime.now(et)
    
    print(f"Analysis Time: {now_et.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Ticker: {ticker}\n")
    
    try:
        # Get 1-minute data (last 100 minutes)
        print("Fetching 1-minute data...")
        df_1min = data_api.get_1min_data(ticker, minutes=100)
        
        if df_1min is None or len(df_1min) == 0:
            print("❌ ERROR: No 1-minute data available")
            return
        
        print(f"✅ Retrieved {len(df_1min)} minutes of data")
        print(f"   Date range: {df_1min['timestamp'].min()} to {df_1min['timestamp'].max()}")
        
        # Get current price
        current_price = df_1min['close'].iloc[-1]
        print(f"\nCurrent Price: ${current_price:.4f}")
        
        # Calculate indicators
        print("\nCalculating indicators...")
        df_with_indicators = pattern_detector.calculate_indicators(df_1min)
        
        if len(df_with_indicators) < 30:
            print(f"❌ ERROR: Insufficient data ({len(df_1min)} minutes, need 30+)")
            return
        
        current_idx = len(df_with_indicators) - 1
        current = df_with_indicators.iloc[current_idx]
        
        print(f"✅ Indicators calculated")
        print(f"   Current index: {current_idx}")
        print(f"   Data points: {len(df_with_indicators)}")
        
        # Check basic requirements
        print(f"\n{'='*80}")
        print("CHECKING BASIC REQUIREMENTS")
        print(f"{'='*80}\n")
        
        # 1. Minimum price check
        print(f"1. Minimum Price Check:")
        print(f"   Current price: ${current_price:.4f}")
        print(f"   Minimum required: $0.50")
        if current_price >= 0.50:
            print(f"   ✅ PASS: Price above minimum")
        else:
            print(f"   ❌ FAIL: Price below minimum")
            return
        
        # 2. Volume checks
        print(f"\n2. Volume Checks:")
        
        # Check 60-minute volume
        if len(df_1min) >= 60:
            recent_volumes = df_1min['volume'].tail(60).values
            total_volume_60min = recent_volumes.sum()
            min_daily_volume = 500000
            print(f"   60-minute total volume: {total_volume_60min:,.0f}")
            print(f"   Minimum required: {min_daily_volume:,.0f}")
            if total_volume_60min >= min_daily_volume:
                print(f"   ✅ PASS: Volume sufficient")
            else:
                print(f"   ❌ FAIL: Low volume stock (total {total_volume_60min:,.0f} < {min_daily_volume:,.0f} over 60 min)")
        else:
            print(f"   ⚠️  WARNING: Less than 60 minutes of data available")
        
        # Check average volume
        if len(df_1min) >= 20:
            avg_volume_20 = df_1min['volume'].tail(20).mean()
            min_avg_volume = 100000
            print(f"   20-period average volume: {avg_volume_20:,.0f}")
            print(f"   Minimum required: {min_avg_volume:,.0f}")
            if avg_volume_20 >= min_avg_volume:
                print(f"   ✅ PASS: Average volume sufficient")
            else:
                print(f"   ❌ FAIL: Low volume stock (avg {avg_volume_20:,.0f} < {min_avg_volume:,} required)")
        
        # Check volume ratio
        volume_ratio = current.get('volume_ratio', 0)
        print(f"   Volume ratio: {volume_ratio:.2f}x")
        print(f"   Minimum required: 1.5x")
        if volume_ratio >= 1.5:
            print(f"   ✅ PASS: Volume ratio sufficient")
        else:
            print(f"   ❌ FAIL: Volume ratio {volume_ratio:.2f}x < 1.5x required")
        
        # 3. Pattern detection
        print(f"\n3. Pattern Detection:")
        lookback = df_with_indicators.iloc[:current_idx + 1]
        signals = pattern_detector._detect_bullish_patterns(
            lookback, current_idx, current, ticker, 
            now_et.strftime('%Y-%m-%d')
        )
        
        if not signals:
            print(f"   ❌ FAIL: No patterns detected")
            print(f"   This is likely the primary reason for rejection")
            return
        
        print(f"   ✅ Found {len(signals)} pattern signal(s)")
        
        # Check each signal
        best_patterns = ['Strong_Bullish_Setup', 'Volume_Breakout']
        
        for i, signal in enumerate(signals):
            print(f"\n   Signal {i+1}:")
            print(f"   Pattern: {signal.pattern_name}")
            print(f"   Confidence: {signal.confidence*100:.1f}%")
            print(f"   Entry Price: ${signal.entry_price:.4f}")
            print(f"   Target: ${signal.target_price:.4f}")
            print(f"   Stop Loss: ${signal.stop_loss:.4f}")
            
            # Check if pattern is in best patterns
            if signal.pattern_name not in best_patterns:
                print(f"   ❌ REJECTED: Pattern '{signal.pattern_name}' not in best patterns")
                print(f"      Required patterns: {best_patterns}")
                continue
            
            # Check confidence
            if signal.confidence < 0.72:
                print(f"   ❌ REJECTED: Confidence {signal.confidence*100:.1f}% < 72% required")
                continue
            
            print(f"   ✅ Pattern and confidence OK")
            
            # Validate entry signal
            print(f"\n   Validating entry signal...")
            validation_result, rejection_reason = trader._validate_entry_signal(
                df_with_indicators, current_idx, signal, log_reasons=True
            )
            
            if validation_result:
                print(f"   ✅ VALIDATION PASSED: Signal is valid!")
            else:
                print(f"   ❌ VALIDATION FAILED: {rejection_reason}")
            
            # Check setup confirmation
            setup_confirmed = trader._setup_confirmed_multiple_periods(
                df_with_indicators, current_idx, signal
            )
            if setup_confirmed:
                print(f"   ✅ Setup confirmed for multiple periods")
            else:
                print(f"   ❌ Setup not confirmed for multiple periods")
        
        # 4. Technical indicators check
        print(f"\n4. Technical Indicators:")
        close = current.get('close', 0)
        sma5 = current.get('sma_5', 0)
        sma10 = current.get('sma_10', 0)
        sma20 = current.get('sma_20', 0)
        
        print(f"   Price: ${close:.4f}")
        print(f"   SMA5: ${sma5:.4f}")
        print(f"   SMA10: ${sma10:.4f}")
        print(f"   SMA20: ${sma20:.4f}")
        
        if close > sma5 and close > sma10 and close > sma20:
            print(f"   ✅ Price above all MAs")
        else:
            print(f"   ❌ Price not above all MAs")
        
        if sma5 > sma10 and sma10 > sma20:
            print(f"   ✅ MAs in bullish order")
        else:
            print(f"   ❌ MAs not in bullish order")
        
        macd = current.get('macd', 0)
        macd_signal = current.get('macd_signal', 0)
        macd_hist = current.get('macd_hist', 0)
        
        print(f"   MACD: {macd:.4f}")
        print(f"   MACD Signal: {macd_signal:.4f}")
        print(f"   MACD Histogram: {macd_hist:.4f}")
        
        if macd > macd_signal:
            print(f"   ✅ MACD bullish")
        else:
            print(f"   ❌ MACD not bullish")
        
        if macd_hist > 0:
            print(f"   ✅ MACD histogram positive")
        else:
            print(f"   ❌ MACD histogram not positive")
        
        rsi = current.get('rsi', 50)
        print(f"   RSI: {rsi:.1f}")
        if 45 < rsi < 70:
            print(f"   ✅ RSI in optimal range")
        else:
            print(f"   ⚠️  RSI outside optimal range (45-70)")
        
        # Summary
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}\n")
        
        print("Most likely rejection reasons:")
        print("1. Pattern not in best patterns (only 'Strong_Bullish_Setup' and 'Volume_Breakout' accepted)")
        print("2. Confidence below 72%")
        print("3. Volume requirements not met (500K over 60 min, 100K/min average, 1.5x ratio)")
        print("4. Setup not confirmed for multiple periods (need 4+ periods)")
        print("5. Technical validation failed (MAs, MACD, price action, etc.)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_opad_rejection()
