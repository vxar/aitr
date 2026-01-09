# OPAD Rejection Analysis

## Stock Information
- **Ticker**: OPAD (Offerpad Solutions Inc)
- **Current Price**: $1.520 (regular hours), $2.540 (after hours)
- **Regular Hours Change**: +4.83% (+$0.070)
- **After Hours Change**: +67.11% (+$1.020)
- **Volume**: 6.20M (daily volume)

## Analysis Date
January 8, 2026

---

## Bot Entry Criteria (Strict Requirements)

Based on the code review, the bot has **very strict entry criteria** that must ALL pass:

### 1. Pattern Requirements
- **Only 2 patterns accepted**:
  - `Strong_Bullish_Setup` (multiple indicators align)
  - `Volume_Breakout` (high volume with price breakout)
- **Rejection if**: Pattern is `Accumulation_Pattern`, `MACD_Bullish_Cross`, `Oversold_Recovery`, or any other pattern

### 2. Confidence Requirements
- **Minimum confidence**: 72% (0.72)
- **Rejection if**: Confidence < 72%

### 3. Volume Requirements (MULTIPLE CHECKS)
The bot has **4 separate volume checks** that must ALL pass:

#### a) 60-Minute Total Volume
- **Required**: Minimum 500,000 shares over last 60 minutes
- **Rejection if**: Total volume < 500K over 60 minutes

#### b) Average Volume
- **Required**: Minimum 100,000 shares/minute average over last 20 periods
- **Rejection if**: Average volume < 100K/minute

#### c) Volume Ratio
- **Required**: Current volume must be ≥ 1.5x the average volume
- **Rejection if**: Volume ratio < 1.5x

#### d) Volume Trend
- **Required**: Volume must be increasing (not declining)
- **Rejection if**: Volume declining 10%+ over last 5 periods

### 4. Price Requirements
- **Minimum price**: $0.50
- **Rejection if**: Price < $0.50

### 5. Technical Indicator Requirements (ALL MUST PASS)

#### a) Moving Averages
- Price must be **above ALL** MAs (SMA5, SMA10, SMA20)
- MAs must be in **bullish order**: SMA5 > SMA10 > SMA20
- **Rejection if**: Price not above all MAs OR MAs not in bullish order

#### b) MACD
- MACD must be **> MACD Signal** (bullish)
- MACD histogram must be **positive**
- MACD histogram must be **accelerating** (3%+ increase for normal stocks, 2%+ for fast movers)
- **Rejection if**: Any MACD condition fails

#### c) Price Action
- Price must be making **higher highs** (within 5% of recent high)
- Price must be making **higher lows** (uptrend confirmation)
- Price must show **upward momentum** (not declining)
- Price must be in **longer-term uptrend** (2%+ gain over 15 periods)
- **Rejection if**: Any price action condition fails

#### d) RSI
- RSI should be in optimal range (45-70) for scoring
- **Rejection if**: RSI > 85 (extremely overbought) OR RSI < 25 (extremely oversold)

### 6. Setup Confirmation
- **Required**: Setup must be confirmed for **at least 4 periods**
- Checks last 6 periods to ensure setup conditions have been building
- **Rejection if**: Setup not confirmed for multiple periods

### 7. False Breakout Detection
- **Rejection if**: False breakout detected (price rejected from highs with high volume)

### 8. Volatility Check
- **Rejection if**: Price range > 8% in 5 periods (too volatile)
- **Exception**: Fast movers bypass this check

### 9. Scoring System
- Must score **6/8 points** (normal stocks) or **5/8 points** (fast movers)
- Points awarded for:
  - Price momentum (2.5%+ gain = 1 point, 1%+ = 0.5 points)
  - Volume ratio (2.5x+ = 1 point, 1.8x+ = 0.5 points)
  - Volume trend (30%+ increase = 1 point, 10%+ = 0.5 points)
  - RSI in optimal range (45-70 = 1 point, 40-45 or 70-75 = 0.5 points)
  - MACD acceleration (10%+ = 1 point, 5%+ = 0.5 points)
  - Price stability (low volatility = 1 point)
  - Volume consistency (1 point)
  - Momentum consistency (1 point)

---

## Most Likely Rejection Reasons for OPAD

Based on the image showing OPAD with +51.14% gain and the bot's strict criteria, here are the **most probable rejection reasons**:

### 1. **Pattern Not in Best Patterns** (HIGH PROBABILITY)
- **Issue**: OPAD likely triggered `Accumulation_Pattern` or `MACD_Bullish_Cross` pattern
- **Evidence**: The dashboard shows "Pattern 'Accumulation_Pattern' not in best patterns" for OPAD
- **Impact**: **IMMEDIATE REJECTION** - Only `Strong_Bullish_Setup` and `Volume_Breakout` are accepted

### 2. **Confidence Below 72%** (HIGH PROBABILITY)
- **Issue**: Pattern confidence was likely 70.0% (as shown in dashboard)
- **Evidence**: Dashboard shows "Confidence 70.0% < 72% required"
- **Impact**: **IMMEDIATE REJECTION** - Minimum 72% confidence required

### 3. **Volume Requirements Not Met** (MEDIUM PROBABILITY)
- **Issue**: OPAD's massive run may have happened quickly, not meeting 60-minute volume requirement
- **Possible scenarios**:
  - Volume spike happened in < 60 minutes, so 60-minute total < 500K
  - Average volume < 100K/minute
  - Volume ratio < 1.5x (if run happened very quickly)
- **Impact**: **IMMEDIATE REJECTION** if any volume check fails

### 4. **Setup Not Confirmed for Multiple Periods** (MEDIUM PROBABILITY)
- **Issue**: Massive run may have happened too quickly
- **Requirement**: Setup must be valid for at least 4 periods
- **Impact**: **IMMEDIATE REJECTION** if setup appeared suddenly

### 5. **Technical Validation Failed** (LOWER PROBABILITY)
- **Possible issues**:
  - Price not above all MAs at entry time
  - MAs not in bullish order
  - MACD not bullish or not accelerating
  - Price action conditions not met
- **Impact**: **IMMEDIATE REJECTION** if any technical check fails

---

## Dashboard Evidence

From the dashboard image, OPAD shows:
- **Status**: REJECTED
- **Rejection Reasons**:
  1. "Confidence 70.0% < 72% required"
  2. "Pattern 'Accumulation_Pattern' not in best patterns"

This confirms **TWO PRIMARY REJECTION REASONS**:
1. ✅ **Pattern rejection**: `Accumulation_Pattern` is not in the accepted best patterns list
2. ✅ **Confidence rejection**: 70.0% confidence is below the 72% minimum requirement

---

## Root Cause Analysis

### Primary Issue: Overly Restrictive Pattern Filter
The bot only accepts **2 patterns** out of many possible bullish patterns:
- `Strong_Bullish_Setup`
- `Volume_Breakout`

**Problem**: Stocks can have massive runs with other valid patterns like:
- `Accumulation_Pattern` (which OPAD triggered)
- `MACD_Bullish_Cross`
- `Oversold_Recovery`
- Other bullish patterns

### Secondary Issue: High Confidence Threshold
The 72% confidence threshold may be too high for fast-moving stocks where patterns form quickly.

---

## Recommendations

### 1. Expand Accepted Patterns
**Current**: Only 2 patterns accepted
**Recommendation**: Add more patterns to the best patterns list:
- `Accumulation_Pattern` (if volume and technicals confirm)
- `MACD_Bullish_Cross` (if other conditions are strong)
- Consider pattern quality scoring instead of binary accept/reject

### 2. Adjust Confidence Threshold for Fast Movers
**Current**: Fixed 72% for all stocks
**Recommendation**: 
- Lower threshold to 70% for fast movers (high volume + momentum)
- Use 72% for normal stocks

### 3. Relax Volume Requirements for Fast Movers
**Current**: Strict 60-minute volume requirement
**Recommendation**:
- For fast movers, use shorter timeframes (20 minutes)
- Or use relative volume (volume ratio) as primary check

### 4. Add Fast Mover Detection Earlier
**Current**: Fast mover detection happens during validation
**Recommendation**: Detect fast movers earlier and apply relaxed criteria throughout

### 5. Pattern Quality Scoring
**Current**: Binary accept/reject based on pattern name
**Recommendation**: Score patterns based on:
- Volume confirmation
- Technical indicator alignment
- Price action quality
- Momentum strength

---

## Conclusion

**OPAD was rejected due to TWO primary reasons**:
1. ❌ **Pattern 'Accumulation_Pattern' not in best patterns** (only `Strong_Bullish_Setup` and `Volume_Breakout` accepted)
2. ❌ **Confidence 70.0% < 72% required**

The bot's **overly restrictive pattern filter** is the main culprit. While the bot is designed to catch high-quality setups, it's missing legitimate opportunities by rejecting valid patterns that don't match the exact 2 pattern names.

**The massive +67.11% after-hours run confirms this was a missed opportunity** that could have been captured with more flexible pattern acceptance criteria.
