# ⚙️ Strategy Engine Agent

**Address:** `agent1qwqr4489ww7kplx456w5tpj4548s743wvp7ly3qjd6aurgp04cf4zswgyal`
**Status:** ✅ Production Ready | Internal Agent

## Overview

Portfolio optimization engine that creates risk-adjusted allocations across protocols with gas estimation.

## Key Features

- 📊 Risk-based allocation models
- 💰 Gas cost estimation per chain
- 🎯 Diversification across protocols and chains
- 📈 Weighted APY and risk calculations
- 📝 Detailed strategy reasoning

## Allocation Models

### Conservative (50/30/15/5)
Heavily favors safest protocol, minimizes exposure to lower-ranked options.
- **Target APY:** 4-7%
- **Portfolio Risk:** 2.0-2.5/10
- **Strategy:** Capital preservation

### Moderate (35/30/20/15)
Balanced distribution for optimal risk/reward.
- **Target APY:** 8-12%
- **Portfolio Risk:** 3.0-4.0/10
- **Strategy:** Balanced growth

### Aggressive (40/30/20/10)
More even distribution for higher yields.
- **Target APY:** 14-18%
- **Portfolio Risk:** 5.0-6.5/10
- **Strategy:** Maximum returns

## Gas Costs by Chain

```python
Ethereum:  0.015 ETH  (~$30)
Polygon:   0.0001 ETH (~$0.20)
Arbitrum:  0.0008 ETH (~$1.60)
Solana:    0.00001 ETH (~$0.02)
BSC:       0.0002 ETH (~$0.40)
```

## How It Works

1. **Filter Opportunities** - Keep only MeTTa-recommended protocols
2. **Calculate Allocations** - Apply allocation model based on risk level
3. **Calculate Metrics** - Expected APY, portfolio risk, gas costs
4. **Generate Reasoning** - Explain strategy rationale
5. **Send Response** - Return complete strategy to Coordinator

## Example Output

**Moderate Risk (10 ETH):**
```
Allocations:
1. Uniswap-V3 (ethereum): 3.50 ETH (35.0%) - 12.3% APY, Risk: 3.5/10
2. QuickSwap (polygon): 3.00 ETH (30.0%) - 9.8% APY, Risk: 4.0/10
3. Curve (ethereum): 2.00 ETH (20.0%) - 6.1% APY, Risk: 2.5/10
4. Aave-V3 (polygon): 1.50 ETH (15.0%) - 5.4% APY, Risk: 2.0/10

Portfolio Metrics:
• Expected APY: 9.28%
• Portfolio Risk: 3.23/10
• Gas Cost: 0.0151 ETH
• Chains Used: 2 (Ethereum, Polygon)
```

## Portfolio Calculations

**Expected APY:**
```
35% × 12.3% + 30% × 9.8% + 20% × 6.1% + 15% × 5.4% = 9.28%
```

**Portfolio Risk:**
```
35% × 3.5 + 30% × 4.0 + 20% × 2.5 + 15% × 2.0 = 3.23/10
```

## Deployment

1. Copy `agents_agentverse/3_strategy_engine.py` to Agentverse
2. Deploy as "YieldSwarm Strategy Engine"
3. Copy agent address for coordinator configuration

---


