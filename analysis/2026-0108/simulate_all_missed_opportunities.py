"""
Simulate trading for CGTL, OPAD, CETX, and LRHC from 4:00 AM
Test the updated code (Priority 1-3 fixes) to see what trades would be placed
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

def simulate_stock(ticker, data_api, pattern_detector, trader):
    """Simulate trading for a single stock from 4:00 AM"""
    
    print(f"\n{'='*80}")
    print(f"SIMULATING {ticker} FROM 4:00 AM")
    print(f"{'='*80}\n")
    
    try:
        # Fetch extended data (500 minutes to cover from 4:00 AM)
        print(f"Fetching data for {ticker}...")
        df_1min = data_api.get_1min_data(ticker, minutes=500)
        
        if df_1min is None or len(df_1min) == 0:
            print(f"❌ ERROR: No data available for {ticker}")
            return None
        
        print(f"✅ Retrieved {len(df_1min)} minutes of data")
        print(f"   Date range: {df_1min['timestamp'].min()} to {df_1min['timestamp'].max()}")
        
        # Filter data from 4:00 AM ET onwards
        df_1min['timestamp'] = pd.to_datetime(df_1min['timestamp'])
        if df_1min['timestamp'].dt.tz is None:
            df_1min['timestamp'] = df_1min['timestamp'].dt.tz_localize('US/Eastern')
        
        # Find 4:00 AM on the trading day
        trading_day = df_1min['timestamp'].min().date()
        et = pytz.timezone('US/Eastern')
        start_time = et.localize(datetime.combine(trading_day, datetime.min.time().replace(hour=4, minute=0)))
        
        print(f"Trading Day: {trading_day}")
        print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Filter data from 4:00 AM
        df_filtered = df_1min[df_1min['timestamp'] >= start_time].copy()
        
        if len(df_filtered) == 0:
            print(f"⚠️  No data from 4:00 AM, using all available data")
            df_filtered = df_1min.copy()
        
        print(f"✅ Filtered to {len(df_filtered)} minutes from 4:00 AM onwards")
        print(f"   Data range: {df_filtered['timestamp'].min()} to {df_filtered['timestamp'].max()}")
        
        # Calculate indicators
        print("Calculating indicators...")
        df_with_indicators = pattern_detector.calculate_indicators(df_filtered)
        
        if len(df_with_indicators) < 30:
            print(f"❌ ERROR: Insufficient data ({len(df_with_indicators)} points, need 30+)")
            return None
        
        print(f"✅ Indicators calculated for {len(df_with_indicators)} data points")
        
        # Track simulation results
        active_position = None
        completed_trades = []
        entry_signals = []
        exit_signals = []
        rejection_log = []
        
        # Simulate minute by minute from 4:00 AM
        start_idx = 30  # Need enough history for indicators
        
        print(f"\n{'='*80}")
        print("SIMULATING MINUTE BY MINUTE")
        print(f"{'='*80}\n")
        
        for idx in range(start_idx, len(df_with_indicators)):
            current = df_with_indicators.iloc[idx]
            current_time = pd.to_datetime(current['timestamp'])
            current_price = current['close']
            
            # Only process during trading hours (4:00 AM - 8:00 PM ET)
            hour = current_time.hour
            if hour < 4 or hour >= 20:
                continue
            
            # Check for entry signals (only if no active position)
            if active_position is None:
                entry_signal = trader.analyze_data(
                    df_with_indicators.iloc[:idx+1],
                    ticker,
                    current_price
                )
                
                if entry_signal:
                    entry_info = {
                        'time': current_time,
                        'price': entry_signal.price,
                        'pattern': entry_signal.pattern_name,
                        'confidence': entry_signal.confidence,
                        'target': entry_signal.target_price,
                        'stop': entry_signal.stop_loss,
                        'reason': entry_signal.reason
                    }
                    entry_signals.append(entry_info)
                    
                    print(f"\n{'='*60}")
                    print(f"✅ ENTRY SIGNAL at {current_time.strftime('%H:%M:%S')}")
                    print(f"   Price: ${current_price:.4f}")
                    print(f"   Pattern: {entry_signal.pattern_name}")
                    print(f"   Confidence: {entry_signal.confidence*100:.1f}%")
                    print(f"   Target: ${entry_signal.target_price:.4f}")
                    print(f"   Stop Loss: ${entry_signal.stop_loss:.4f}")
                    print(f"   Reason: {entry_signal.reason}")
                    
                    # Check validation
                    lookback = df_with_indicators.iloc[:idx+1]
                    signals = pattern_detector._detect_bullish_patterns(
                        lookback, idx, current, ticker, 
                        current_time.strftime('%Y-%m-%d')
                    )
                    
                    if signals:
                        for sig in signals:
                            if sig.pattern_name == entry_signal.pattern_name:
                                validation_result, rejection_reason = trader._validate_entry_signal(
                                    df_with_indicators, idx, sig, log_reasons=True
                                )
                                
                                if validation_result:
                                    setup_confirmed = trader._setup_confirmed_multiple_periods(
                                        df_with_indicators, idx, sig
                                    )
                                    
                                    if setup_confirmed:
                                        print(f"   ✅ VALIDATION PASSED - ENTRY EXECUTED")
                                        # Enter position
                                        active_position = {
                                            'entry_time': current_time,
                                            'entry_price': entry_signal.price,
                                            'pattern': entry_signal.pattern_name,
                                            'target': entry_signal.target_price,
                                            'stop': entry_signal.stop_loss,
                                            'max_price': entry_signal.price
                                        }
                                    else:
                                        print(f"   ❌ SETUP NOT CONFIRMED - Entry rejected")
                                        rejection_log.append({
                                            'time': current_time,
                                            'price': current_price,
                                            'reason': 'Setup not confirmed for multiple periods'
                                        })
                                else:
                                    print(f"   ❌ VALIDATION FAILED: {rejection_reason}")
                                    rejection_log.append({
                                        'time': current_time,
                                        'price': current_price,
                                        'reason': rejection_reason
                                    })
            
            # Check for exit signals on active position
            if active_position is not None:
                exit_signals_list = trader._check_exit_signals(
                    df_with_indicators.iloc[:idx+1],
                    ticker,
                    current_price
                )
                
                for exit_signal in exit_signals_list:
                    exit_info = {
                        'time': current_time,
                        'price': exit_signal.price,
                        'reason': exit_signal.reason
                    }
                    exit_signals.append(exit_info)
                    
                    print(f"\n{'='*60}")
                    print(f"🛑 EXIT SIGNAL at {current_time.strftime('%H:%M:%S')}")
                    print(f"   Price: ${current_price:.4f}")
                    print(f"   Reason: {exit_signal.reason}")
                    
                    # Close position
                    pnl_pct = ((current_price - active_position['entry_price']) / active_position['entry_price']) * 100
                    pnl_dollars = (current_price - active_position['entry_price']) * 1000  # Assume 1000 shares
                    
                    trade = {
                        'ticker': ticker,
                        'entry_time': active_position['entry_time'],
                        'exit_time': current_time,
                        'entry_price': active_position['entry_price'],
                        'exit_price': current_price,
                        'pnl_pct': pnl_pct,
                        'pnl_dollars': pnl_dollars,
                        'pattern': active_position['pattern'],
                        'exit_reason': exit_signal.reason,
                        'hold_time_minutes': (current_time - active_position['entry_time']).total_seconds() / 60
                    }
                    completed_trades.append(trade)
                    
                    print(f"   Entry: ${active_position['entry_price']:.4f} @ {active_position['entry_time'].strftime('%H:%M:%S')}")
                    print(f"   Exit: ${current_price:.4f} @ {current_time.strftime('%H:%M:%S')}")
                    print(f"   P&L: {pnl_pct:.2f}% (${pnl_dollars:,.2f})")
                    print(f"   Hold Time: {trade['hold_time_minutes']:.1f} minutes")
                    
                    active_position = None
            
            # Update max price if position active
            if active_position is not None:
                if current_price > active_position['max_price']:
                    active_position['max_price'] = current_price
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"{ticker} SIMULATION SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Entry Signals Found: {len(entry_signals)}")
        print(f"Exit Signals Found: {len(exit_signals)}")
        print(f"Completed Trades: {len(completed_trades)}")
        print(f"Rejections: {len(rejection_log)}")
        print(f"Active Position at End: {'Yes' if active_position else 'No'}")
        
        if active_position:
            final_price = df_with_indicators['close'].iloc[-1]
            final_pnl = ((final_price - active_position['entry_price']) / active_position['entry_price']) * 100
            print(f"   Final Price: ${final_price:.4f}")
            print(f"   Unrealized P&L: {final_pnl:.2f}%")
        
        # Return results
        return {
            'ticker': ticker,
            'entry_signals': entry_signals,
            'exit_signals': exit_signals,
            'completed_trades': completed_trades,
            'rejections': rejection_log,
            'active_position': active_position,
            'final_price': df_with_indicators['close'].iloc[-1] if len(df_with_indicators) > 0 else None
        }
        
    except Exception as e:
        print(f"\n❌ ERROR simulating {ticker}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run simulation for all stocks"""
    
    print(f"\n{'='*80}")
    print("MISSED OPPORTUNITIES SIMULATION")
    print("Testing Updated Code (Priority 1-3 Fixes)")
    print(f"{'='*80}\n")
    
    # Initialize components
    data_api = WebullDataAPI()
    pattern_detector = PatternDetector()
    trader = RealtimeTrader(min_confidence=0.72)
    
    # Stocks to simulate
    stocks = ['CGTL', 'OPAD', 'CETX', 'LRHC']
    
    all_results = []
    
    for ticker in stocks:
        result = simulate_stock(ticker, data_api, pattern_detector, trader)
        if result:
            all_results.append(result)
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print("COMPREHENSIVE SUMMARY - ALL STOCKS")
    print(f"{'='*80}\n")
    
    total_trades = 0
    total_pnl = 0
    
    for result in all_results:
        ticker = result['ticker']
        trades = result['completed_trades']
        entries = result['entry_signals']
        
        print(f"\n{ticker}:")
        print(f"  Entry Signals: {len(entries)}")
        print(f"  Completed Trades: {len(trades)}")
        
        if entries:
            print(f"  Entry Times:")
            for entry in entries:
                print(f"    - {entry['time'].strftime('%H:%M:%S')} @ ${entry['price']:.4f} ({entry['pattern']}, {entry['confidence']*100:.1f}%)")
        
        if trades:
            print(f"  Trades:")
            for i, trade in enumerate(trades, 1):
                print(f"    Trade {i}:")
                print(f"      Entry: {trade['entry_time'].strftime('%H:%M:%S')} @ ${trade['entry_price']:.4f}")
                print(f"      Exit: {trade['exit_time'].strftime('%H:%M:%S')} @ ${trade['exit_price']:.4f}")
                print(f"      P&L: {trade['pnl_pct']:.2f}% (${trade['pnl_dollars']:,.2f})")
                print(f"      Hold: {trade['hold_time_minutes']:.1f} min")
                print(f"      Pattern: {trade['pattern']}")
                print(f"      Exit Reason: {trade['exit_reason']}")
                total_trades += 1
                total_pnl += trade['pnl_dollars']
        
        if result['active_position']:
            pos = result['active_position']
            final_pnl = ((result['final_price'] - pos['entry_price']) / pos['entry_price']) * 100
            print(f"  Active Position:")
            print(f"    Entry: {pos['entry_time'].strftime('%H:%M:%S')} @ ${pos['entry_price']:.4f}")
            print(f"    Current: ${result['final_price']:.4f}")
            print(f"    Unrealized P&L: {final_pnl:.2f}%")
    
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print(f"{'='*80}\n")
    print(f"Total Stocks Analyzed: {len(all_results)}")
    print(f"Total Entry Signals: {sum(len(r['entry_signals']) for r in all_results)}")
    print(f"Total Completed Trades: {total_trades}")
    print(f"Total P&L: ${total_pnl:,.2f}")
    if total_trades > 0:
        print(f"Average P&L per Trade: ${total_pnl/total_trades:,.2f}")

if __name__ == "__main__":
    main()
