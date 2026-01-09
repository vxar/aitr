"""
Simulate CGTL trading from 4:00 AM to check why no trades were placed
CGTL showed: +118.10% during regular hours, +23.72% after hours
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from data.webull_data_api import WebullDataAPI
from analysis.pattern_detector import PatternDetector
from core.realtime_trader import RealtimeTrader

def simulate_cgtl_trading():
    """Simulate CGTL trading from 4:00 AM"""
    
    ticker = "CGTL"
    print(f"\n{'='*80}")
    print(f"CGTL FULL DAY SIMULATION (From 4:00 AM)")
    print(f"{'='*80}\n")
    
    # Initialize components
    data_api = WebullDataAPI()
    pattern_detector = PatternDetector()
    trader = RealtimeTrader(min_confidence=0.72)
    
    # Get current date and set start time to 4:00 AM ET
    et = pytz.timezone('US/Eastern')
    now_et = datetime.now(et)
    
    # Get data for today (or most recent trading day)
    # Fetch enough data to cover from 4:00 AM
    print("Fetching 1-minute data from 4:00 AM...")
    print("Note: Fetching extended data to cover pre-market and regular hours...")
    
    # Try to get data - we need enough to cover from 4:00 AM
    # Pre-market starts at 4:00 AM ET, regular market at 9:30 AM ET
    # So we need at least 6.5 hours of pre-market + regular hours = ~390 minutes minimum
    # Let's fetch 500 minutes to be safe
    df_1min = data_api.get_1min_data(ticker, minutes=500)
    
    if df_1min is None or len(df_1min) == 0:
        print("❌ ERROR: No data available")
        return
    
    print(f"✅ Retrieved {len(df_1min)} minutes of data")
    print(f"   Date range: {df_1min['timestamp'].min()} to {df_1min['timestamp'].max()}")
    
    # Filter data from 4:00 AM ET onwards
    df_1min['timestamp'] = pd.to_datetime(df_1min['timestamp'])
    if df_1min['timestamp'].dt.tz is None:
        df_1min['timestamp'] = df_1min['timestamp'].dt.tz_localize('US/Eastern')
    
    # Find 4:00 AM on the trading day
    trading_day = df_1min['timestamp'].min().date()
    start_time = et.localize(datetime.combine(trading_day, datetime.min.time().replace(hour=4, minute=0)))
    
    print(f"\nTrading Day: {trading_day}")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Filter data from 4:00 AM
    df_filtered = df_1min[df_1min['timestamp'] >= start_time].copy()
    
    if len(df_filtered) == 0:
        print("❌ ERROR: No data from 4:00 AM onwards")
        print(f"   Available data starts at: {df_1min['timestamp'].min()}")
        # Use all available data instead
        df_filtered = df_1min.copy()
        print(f"   Using all available data instead")
    
    print(f"✅ Filtered to {len(df_filtered)} minutes from 4:00 AM onwards")
    print(f"   Data range: {df_filtered['timestamp'].min()} to {df_filtered['timestamp'].max()}")
    
    # Calculate indicators for all data
    print("\nCalculating indicators...")
    df_with_indicators = pattern_detector.calculate_indicators(df_filtered)
    
    if len(df_with_indicators) < 30:
        print(f"❌ ERROR: Insufficient data after filtering ({len(df_with_indicators)} points, need 30+)")
        return
    
    print(f"✅ Indicators calculated for {len(df_with_indicators)} data points")
    
    # Track positions and trades
    active_positions = {}
    completed_trades = []
    entry_signals_found = []
    exit_signals_found = []
    rejection_reasons = []
    
    # Simulate minute by minute from 4:00 AM
    print(f"\n{'='*80}")
    print("SIMULATING MINUTE BY MINUTE")
    print(f"{'='*80}\n")
    
    # Start from index 30 (need enough history for indicators)
    start_idx = 30
    
    for idx in range(start_idx, len(df_with_indicators)):
        current = df_with_indicators.iloc[idx]
        current_time = pd.to_datetime(current['timestamp'])
        current_price = current['close']
        
        # Only process during trading hours (4:00 AM - 8:00 PM ET)
        hour = current_time.hour
        if hour < 4 or hour >= 20:
            continue
        
        # Check for entry signals
        entry_signal = trader.analyze_data(
            df_with_indicators.iloc[:idx+1],
            ticker,
            current_price
        )
        
        if entry_signal:
            entry_signals_found.append({
                'time': current_time,
                'price': entry_signal.price,
                'pattern': entry_signal.pattern_name,
                'confidence': entry_signal.confidence,
                'reason': entry_signal.reason,
                'target': entry_signal.target_price,
                'stop': entry_signal.stop_loss
            })
            
            print(f"\n{'='*60}")
            print(f"✅ ENTRY SIGNAL FOUND at {current_time.strftime('%H:%M:%S')}")
            print(f"   Price: ${current_price:.4f}")
            print(f"   Pattern: {entry_signal.pattern_name}")
            print(f"   Confidence: {entry_signal.confidence*100:.1f}%")
            print(f"   Target: ${entry_signal.target_price:.4f}")
            print(f"   Stop Loss: ${entry_signal.stop_loss:.4f}")
            print(f"   Reason: {entry_signal.reason}")
            
            # Check why it might be rejected
            lookback = df_with_indicators.iloc[:idx+1]
            signals = pattern_detector._detect_bullish_patterns(
                lookback, idx, current, ticker, 
                current_time.strftime('%Y-%m-%d')
            )
            
            if signals:
                for sig in signals:
                    if sig.pattern_name == entry_signal.pattern_name:
                        # Validate entry signal
                        validation_result, rejection_reason = trader._validate_entry_signal(
                            df_with_indicators, idx, sig, log_reasons=True
                        )
                        
                        if not validation_result:
                            print(f"   ❌ VALIDATION FAILED: {rejection_reason}")
                            rejection_reasons.append({
                                'time': current_time,
                                'price': current_price,
                                'reason': rejection_reason
                            })
                        else:
                            print(f"   ✅ VALIDATION PASSED")
                            
                            # Check setup confirmation
                            setup_confirmed = trader._setup_confirmed_multiple_periods(
                                df_with_indicators, idx, sig
                            )
                            if not setup_confirmed:
                                print(f"   ❌ SETUP NOT CONFIRMED: Setup not confirmed for multiple periods")
                                rejection_reasons.append({
                                    'time': current_time,
                                    'price': current_price,
                                    'reason': 'Setup not confirmed for multiple periods'
                                })
                            else:
                                print(f"   ✅ SETUP CONFIRMED")
        
        # Check for exit signals on active positions
        if ticker in active_positions:
            exit_signals = trader._check_exit_signals(
                df_with_indicators.iloc[:idx+1],
                ticker,
                current_price
            )
            
            for exit_signal in exit_signals:
                exit_signals_found.append({
                    'time': current_time,
                    'price': exit_signal.price,
                    'reason': exit_signal.reason
                })
                
                print(f"\n{'='*60}")
                print(f"🛑 EXIT SIGNAL at {current_time.strftime('%H:%M:%S')}")
                print(f"   Price: ${current_price:.4f}")
                print(f"   Reason: {exit_signal.reason}")
                
                # Close position
                position = active_positions.pop(ticker)
                pnl_pct = ((current_price - position['entry_price']) / position['entry_price']) * 100
                
                completed_trades.append({
                    'entry_time': position['entry_time'],
                    'exit_time': current_time,
                    'entry_price': position['entry_price'],
                    'exit_price': current_price,
                    'pnl_pct': pnl_pct,
                    'pattern': position['pattern']
                })
                
                print(f"   Entry: ${position['entry_price']:.4f} @ {position['entry_time'].strftime('%H:%M:%S')}")
                print(f"   Exit: ${current_price:.4f} @ {current_time.strftime('%H:%M:%S')}")
                print(f"   P&L: {pnl_pct:.2f}%")
        
        # Check rejection reasons from trader
        if ticker in trader.last_rejection_reasons:
            reasons = trader.last_rejection_reasons[ticker]
            if reasons:
                # Only log if we haven't seen this exact rejection recently
                last_rejection = rejection_reasons[-1] if rejection_reasons else None
                if not last_rejection or last_rejection['time'] != current_time:
                    for reason in reasons:
                        rejection_reasons.append({
                            'time': current_time,
                            'price': current_price,
                            'reason': reason
                        })
        
        # Print progress every 30 minutes
        if idx % 30 == 0:
            print(f"\n[{current_time.strftime('%H:%M:%S')}] Price: ${current_price:.4f} | "
                  f"Signals: {len(entry_signals_found)} | Rejections: {len(rejection_reasons)} | "
                  f"Active: {len(active_positions)} | Completed: {len(completed_trades)}")
    
    # Print summary
    print(f"\n{'='*80}")
    print("SIMULATION SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Total Entry Signals Found: {len(entry_signals_found)}")
    print(f"Total Exit Signals Found: {len(exit_signals_found)}")
    print(f"Total Rejections: {len(rejection_reasons)}")
    print(f"Completed Trades: {len(completed_trades)}")
    print(f"Active Positions at End: {len(active_positions)}")
    
    if entry_signals_found:
        print(f"\n{'='*80}")
        print("ENTRY SIGNALS DETAIL")
        print(f"{'='*80}\n")
        for i, signal in enumerate(entry_signals_found, 1):
            print(f"{i}. Time: {signal['time'].strftime('%H:%M:%S')}")
            print(f"   Price: ${signal['price']:.4f}")
            print(f"   Pattern: {signal['pattern']}")
            print(f"   Confidence: {signal['confidence']*100:.1f}%")
            print(f"   Target: ${signal['target']:.4f}")
            print(f"   Stop: ${signal['stop']:.4f}")
            print()
    
    if rejection_reasons:
        print(f"\n{'='*80}")
        print("REJECTION REASONS SUMMARY")
        print(f"{'='*80}\n")
        
        # Group by reason
        reason_counts = {}
        for rejection in rejection_reasons:
            reason = rejection['reason']
            if reason not in reason_counts:
                reason_counts[reason] = []
            reason_counts[reason].append(rejection)
        
        for reason, occurrences in sorted(reason_counts.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"{reason}: {len(occurrences)} times")
            # Show first few occurrences
            for occ in occurrences[:3]:
                print(f"   - {occ['time'].strftime('%H:%M:%S')} @ ${occ['price']:.4f}")
            if len(occurrences) > 3:
                print(f"   ... and {len(occurrences) - 3} more")
            print()
    
    if completed_trades:
        print(f"\n{'='*80}")
        print("COMPLETED TRADES")
        print(f"{'='*80}\n")
        for i, trade in enumerate(completed_trades, 1):
            print(f"Trade {i}:")
            print(f"   Entry: ${trade['entry_price']:.4f} @ {trade['entry_time'].strftime('%H:%M:%S')}")
            print(f"   Exit: ${trade['exit_price']:.4f} @ {trade['exit_time'].strftime('%H:%M:%S')}")
            print(f"   P&L: {trade['pnl_pct']:.2f}%")
            print(f"   Pattern: {trade['pattern']}")
            print()
    
    # Final price check
    final_price = df_with_indicators['close'].iloc[-1]
    final_time = pd.to_datetime(df_with_indicators['timestamp'].iloc[-1])
    print(f"\n{'='*80}")
    print("FINAL STATUS")
    print(f"{'='*80}\n")
    print(f"Final Price: ${final_price:.4f} @ {final_time.strftime('%H:%M:%S')}")
    print(f"Starting Price (4:00 AM): ${df_with_indicators['close'].iloc[start_idx]:.4f}")
    total_change = ((final_price - df_with_indicators['close'].iloc[start_idx]) / 
                   df_with_indicators['close'].iloc[start_idx]) * 100
    print(f"Total Change: {total_change:.2f}%")
    
    if len(entry_signals_found) == 0:
        print(f"\n❌ NO ENTRY SIGNALS FOUND - This explains why no trades were placed")
        print(f"   Possible reasons:")
        print(f"   1. No patterns detected")
        print(f"   2. Patterns detected but rejected (check rejection reasons above)")
        print(f"   3. Technical indicators not aligned")
    elif len(entry_signals_found) > 0 and len(completed_trades) == 0:
        print(f"\n⚠️  ENTRY SIGNALS FOUND BUT NO TRADES EXECUTED")
        print(f"   This means signals were rejected during validation")
        print(f"   Check rejection reasons above")

if __name__ == "__main__":
    simulate_cgtl_trading()
