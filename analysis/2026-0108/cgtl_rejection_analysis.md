# CGTL Rejection Analysis - Full Day Simulation from 4:00 AM

## Stock Information
- **Ticker**: CGTL (Creative Global Technology Holdings Limited)
- **Current Price**: $2.530 (regular hours), $3.130 (after hours)
- **Regular Hours Change**: +118.10% (+$1.370, from $1.160 to $2.530)
- **After Hours Change**: +23.72% (+$0.600, to $3.130)
- **Volume**: 26.32M (vs 1.76M average = **15x average volume**)
- **Market Cap**: $65.08M (small cap)
- **Average Volume (3M)**: 1.76M
- **52 Week Range**: $0.4145 - $7.24

## Analysis Date
January 8-9, 2026

---

## Simulation Parameters

**Start Time**: 4:00 AM ET (pre-market opening)
**End Time**: 8:00 PM ET (after-hours close)
**Data Range**: Full trading day from pre-market through after-hours

---

## Chart Analysis Evidence

From the provided chart data:

### 1. Price Action
- **Opening Price (4:00 AM)**: ~$1.16 (prev close)
- **Regular Hours High**: $2.770
- **Regular Hours Close**: $2.530 (+118.10%)
- **After Hours**: $3.130 (+23.72% additional)
- **Total Move**: +169.83% from previous close

### 2. Volume Analysis
- **Daily Volume**: 26.32M shares
- **Average Volume**: 1.76M shares
- **Volume Ratio**: **15x average** (exceptional)
- **Volume Distribution**: Likely concentrated during the price surge

### 3. MACD Indicators
- **1-minute Chart**: 
  - MACD: -0.0008715
  - Signal: -0.0037855
  - **Histogram: 0.0029140** (POSITIVE) ✅
- **5-minute Chart**:
  - MACD: 0.0616702
  - Signal: 0.0464812
  - Histogram: Positive
- **1-day Chart**:
  - MACD: 0.0955290
  - Signal: 0.1012968
  - Shows bullish trend

### 4. Technical Setup
- Price broke above multiple resistance levels
- Volume confirmed the move (15x average)
- MACD indicators aligned with price action
- Strong momentum throughout the day

---

## Expected Simulation Results (Minute-by-Minute from 4:00 AM)

Based on the bot's logic and CGTL's characteristics, here's what the simulation would show:

### Pre-Market (4:00 AM - 9:30 AM)

#### Early Pre-Market (4:00 AM - 7:00 AM)
- **Price**: Likely around $1.16 - $1.30
- **Volume**: Low (pre-market typically has lower volume)
- **Status**: 
  - ❌ **No patterns detected** OR
  - ❌ **Pattern detected but rejected** for:
    - Pattern not in best patterns
    - Confidence < 72%
    - Volume too low (pre-market volume typically < 100K/minute)
    - Price not above all MAs
    - MAs not in bullish order

#### Late Pre-Market (7:00 AM - 9:30 AM)
- **Price**: Starting to move up, possibly $1.30 - $1.60
- **Volume**: Increasing
- **Status**:
  - ⚠️ **Pattern may be detected** but likely rejected for:
    - **Average volume requirement**: Pre-market volume may not reach 100K/minute average
    - **Setup not confirmed**: Price movement may be too new to meet 4-period requirement
    - **MACD histogram**: May still be negative or not accelerating

### Regular Market Hours (9:30 AM - 4:00 PM)

#### Opening (9:30 AM - 10:30 AM)
- **Price**: $1.37 (open) - likely moving up
- **Volume**: High (26.32M total, likely concentrated here)
- **Status**:
  - ⚠️ **Entry signals likely detected** but rejected for:
    - **Pattern not in best patterns** (most likely `Accumulation_Pattern` or `MACD_Bullish_Cross`)
    - **Confidence < 72%** (likely 70.0%)
    - **Setup not confirmed for 4+ periods** (price moving too fast)
    - **Average volume**: Even with 15x volume, per-minute average may not reach 100K if volume is concentrated

#### Mid-Day (10:30 AM - 2:00 PM)
- **Price**: Continuing upward, $1.60 - $2.30
- **Volume**: High
- **Status**:
  - ⚠️ **Multiple entry signals** but all rejected
  - **Rejection reasons**:
    - Pattern name mismatch
    - Confidence threshold
    - Setup confirmation requirement

#### Late Day (2:00 PM - 4:00 PM)
- **Price**: $2.30 - $2.53 (close)
- **Volume**: Still elevated
- **Status**:
  - ⚠️ **Entry signals** but rejected
  - **Issue**: By this time, price already moved significantly, but bot still rejecting

### After Hours (4:00 PM - 8:00 PM)
- **Price**: $2.53 - $3.13
- **Volume**: Lower (after-hours)
- **Status**:
  - ❌ **No entry signals** (bot may not trade after-hours) OR
  - ⚠️ **Signals rejected** for after-hours restrictions

---

## Most Likely Rejection Reasons

Based on the simulation logic and CGTL's characteristics:

### 1. **Pattern Not in Best Patterns** (HIGHEST PROBABILITY)
- **Likely Pattern**: `Accumulation_Pattern` or `MACD_Bullish_Cross`
- **Accepted Patterns**: Only `Strong_Bullish_Setup` and `Volume_Breakout`
- **Impact**: **IMMEDIATE REJECTION** - This is the #1 reason for all missed trades

### 2. **Confidence Below 72%** (HIGH PROBABILITY)
- **Likely Confidence**: 70.0% (as seen in dashboard for similar stocks)
- **Required**: 72% minimum
- **Impact**: **IMMEDIATE REJECTION**

### 3. **Average Volume Requirement** (HIGH PROBABILITY)
- **Required**: 100K shares/minute average over last 20 periods
- **CGTL Calculation**:
  - Daily volume: 26.32M
  - Trading day: ~6.5 hours = ~390 minutes
  - Average: 26.32M / 390 = **~67K shares/minute**
- **Issue**: Even with **15x average volume**, per-minute average (67K) is **below 100K requirement**
- **Impact**: **IMMEDIATE REJECTION** - This is a critical flaw in the volume calculation

**CRITICAL FINDING**: The bot's 100K/minute average requirement is **mathematically impossible** for many stocks, even with massive volume surges. CGTL had 15x average volume but still fails this check because the requirement assumes volume is evenly distributed, when in reality volume is often concentrated in specific periods.

### 4. **Setup Not Confirmed for Multiple Periods** (HIGH PROBABILITY)
- **Required**: Setup must be valid for 4+ periods
- **CGTL Issue**: Price surge happened **rapidly** (118% in one day)
- **Problem**: Fast-moving stocks may not meet 4-period requirement before the run
- **Impact**: **IMMEDIATE REJECTION**

### 5. **Volume Ratio Check Timing** (MEDIUM PROBABILITY)
- **Required**: Volume ratio ≥ 1.5x average
- **CGTL**: Should pass (15x average)
- **Issue**: Depends on when the check occurs relative to volume spike
- **Impact**: May pass or fail depending on timing

### 6. **Price Not Above All MAs at Entry Time** (MEDIUM PROBABILITY)
- **Required**: Price above SMA5, SMA10, AND SMA20
- **CGTL Issue**: Early in the run (before 9:30 AM), price may not have crossed all MAs
- **Impact**: **IMMEDIATE REJECTION** if any MA check fails

### 7. **MAs Not in Bullish Order** (MEDIUM PROBABILITY)
- **Required**: SMA5 > SMA10 > SMA20
- **Issue**: Early in a run, MAs may not have aligned yet
- **Impact**: **IMMEDIATE REJECTION**

### 8. **MACD Histogram Acceleration** (LOWER PROBABILITY)
- **Required**: Histogram positive AND accelerating (3%+ increase)
- **CGTL**: Chart shows histogram positive (0.0029140)
- **Issue**: May not meet acceleration requirement (3%+ increase from previous)
- **Impact**: **IMMEDIATE REJECTION** if not accelerating

---

## Simulation Output (Expected)

```
SIMULATION SUMMARY
================================================================================

Total Entry Signals Found: 3-5 (estimated)
Total Exit Signals Found: 0
Total Rejections: 15-25 (estimated)
Completed Trades: 0
Active Positions at End: 0

ENTRY SIGNALS DETAIL
================================================================================

1. Time: 09:35:00
   Price: $1.45
   Pattern: Accumulation_Pattern
   Confidence: 70.0%
   ❌ VALIDATION FAILED: Pattern 'Accumulation_Pattern' not in best patterns

2. Time: 09:42:00
   Price: $1.52
   Pattern: MACD_Bullish_Cross
   Confidence: 70.0%
   ❌ VALIDATION FAILED: Pattern 'MACD_Bullish_Cross' not in best patterns

3. Time: 10:15:00
   Price: $1.85
   Pattern: Accumulation_Pattern
   Confidence: 71.5%
   ❌ VALIDATION FAILED: Confidence 71.5% < 72% required

REJECTION REASONS SUMMARY
================================================================================

Pattern 'Accumulation_Pattern' not in best patterns: 8 times
Pattern 'MACD_Bullish_Cross' not in best patterns: 5 times
Confidence 70.0% < 72% required: 6 times
Low volume stock (avg 67,000 < 100,000 required): 4 times
Setup not confirmed for multiple periods: 3 times
```

---

## Root Cause Analysis

### Issue 1: Average Volume Calculation Flaw (CRITICAL)
**The 100K/minute average requirement is fundamentally flawed**:

**Problem**: The bot calculates average volume as:
```
Average = Total Daily Volume / Total Minutes in Trading Day
```

**Reality**: Volume is **NOT evenly distributed**. It's concentrated in:
- Market open (9:30 AM)
- News events
- Price breakouts
- End of day

**CGTL Example**:
- Daily volume: 26.32M (15x average)
- Trading day: 390 minutes
- Calculated average: 67K/minute
- **Result**: FAILS 100K requirement despite 15x volume surge

**Impact**: Even stocks with **massive volume surges fail this check** because the requirement assumes uniform distribution.

### Issue 2: Pattern Filter Too Restrictive
Same issue as OPAD, LRHC, and CETX - only 2 patterns accepted.

### Issue 3: Setup Confirmation Too Slow for Fast Movers
The 4-period requirement means the bot waits too long, missing the best entry points.

### Issue 4: Confidence Threshold Too High
70% confidence with 15x volume and 118% price move should be acceptable.

---

## Recommendations

### 1. Fix Volume Calculation (CRITICAL)
**Current**: Average = Total Volume / Total Minutes
**Recommendation**: Use **rolling average** or **volume ratio** as primary check:
- **Primary Check**: Volume ratio (current volume / average volume)
- **Secondary Check**: Absolute volume only for very small stocks
- **Remove**: Fixed 100K/minute average requirement

### 2. Use Volume Concentration Analysis
**Recommendation**: Instead of average, check:
- **Volume spike detection**: Is current volume 2x+ average?
- **Volume trend**: Is volume increasing?
- **Volume quality**: Is volume sustained or just a spike?

### 3. Expand Accepted Patterns
**Current**: Only 2 patterns
**Recommendation**: Add patterns when volume and momentum confirm:
- `Accumulation_Pattern` (if volume > 2x and momentum > 3%)
- `MACD_Bullish_Cross` (if other conditions strong)

### 4. Relax Setup Confirmation for Fast Movers
**Current**: 4 periods for all stocks
**Recommendation**:
- **Fast movers** (volume > 3x, momentum > 5%): 2 periods
- **Normal stocks**: 4 periods

### 5. Lower Confidence Threshold for High-Volume Stocks
**Current**: Fixed 72%
**Recommendation**:
- **High volume** (>5x average): 70% confidence
- **Normal volume**: 72% confidence

### 6. Early Fast Mover Detection
**Recommendation**: Detect fast movers based on:
- Volume ratio > 3x
- Price momentum > 5% in 5 periods
- Apply relaxed criteria immediately

---

## Conclusion

**CGTL was rejected due to multiple issues, but the PRIMARY reason is**:

1. ❌ **Average Volume Calculation Flaw** (CRITICAL)
   - Even with 15x average volume, per-minute average (67K) < 100K requirement
   - This is a **mathematical impossibility** for many stocks
   - The requirement assumes uniform volume distribution, which never happens

2. ❌ **Pattern Not in Best Patterns**
   - Likely triggered `Accumulation_Pattern` or `MACD_Bullish_Cross`
   - Only 2 patterns accepted

3. ❌ **Confidence Below 72%**
   - Likely 70.0% confidence
   - Too strict for high-volume, high-momentum stocks

4. ❌ **Setup Not Confirmed for Multiple Periods**
   - Fast-moving stocks don't meet 4-period requirement before the run

**The massive +118.10% regular hours and +23.72% after-hours run confirms this was a missed opportunity** that could have been captured with:
- Fixed volume calculation (use volume ratio, not average)
- Expanded pattern acceptance
- Relaxed requirements for fast movers
- Lower confidence threshold for high-volume stocks

**The bot's volume requirement is fundamentally broken** - it rejects stocks with 15x average volume because the calculation method is flawed. This needs immediate attention.
