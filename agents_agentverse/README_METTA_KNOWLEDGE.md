# 🧠 MeTTa Knowledge Agent

**Address:** `agent1qflfh899d98vw3337neylwjkfvc4exx6frsj6vqnaeq0ujwjf6ggcczc5y0`
**Status:** ✅ Production Ready | Internal Agent

## Overview

Symbolic AI reasoning engine using **22-protocol knowledge base** for intelligent, explainable DeFi recommendations.

## Key Features

- 🧠 22 DeFi protocols with embedded knowledge
- 🔍 Symbolic reasoning (risk-based filtering, optimization)
- 📚 Explainable AI with detailed justifications
- 🎯 Risk strategies: Conservative, Moderate, Aggressive
- ⚡ Self-contained (knowledge embedded in code)

## Protocol Knowledge Base (22 Total)

**By Risk Level:**

**Conservative (≤3.0):**
- MakerDAO (2.0), Curve (2.1), Lido (2.3), Aave-V3 (2.5), Compound-V3 (2.8), Frax (3.0), Yearn (3.2)

**Moderate (3.0-5.0):**
- Uniswap-V3 (3.5), Convex (3.5), Balancer (3.8), QuickSwap (4.0), Beefy (4.2), Stargate (4.5), Venus (4.8), Trader-Joe (4.8)

**Aggressive (5.0-8.0):**
- PancakeSwap (5.0), Synapse (5.2), GMX (5.5), Solend (5.5), Raydium (6.0)

**Coverage:** Lending, DEX, Yield Optimizers, Liquid Staking, Bridges, Stablecoins

## Symbolic Reasoning

**Conservative:**
```python
# Filter: Risk ≤ 3.0
# Optimize: Maximize risk-adjusted returns
# Priority: Capital preservation, security audits, high TVL
```

**Moderate:**
```python
# Filter: Risk ≤ 5.0
# Optimize: Balance APY and risk
# Priority: Mix of stable lending + established DEXes
```

**Aggressive:**
```python
# Filter: Risk ≤ 8.0
# Optimize: Maximize APY
# Priority: High yields with diversification
```

## Example Response

```markdown
Selected Protocols:
1. Uniswap-V3 (ethereum): 12.3% APY, Risk: 3.5/10
2. QuickSwap (polygon): 9.8% APY, Risk: 4.0/10
3. Curve (ethereum): 6.1% APY, Risk: 2.5/10
4. Aave-V3 (polygon): 5.4% APY, Risk: 2.0/10

Symbolic Reasoning (MeTTa KB):
- Strategy: Balanced risk-reward optimization
- Chain Diversification: 2 blockchains for reduced correlation
- Portfolio Risk: 3.3/10 | Expected APY: 8.9%
- Knowledge Base: 22 protocols analyzed across 5 chains

Applied Rules:
✓ Protocol security analysis (audits, TVL)
✓ Historical performance patterns
✓ Risk-adjusted return optimization
✓ Cross-chain diversification
```

## Deployment

1. Copy `agents_agentverse/2_metta_knowledge.py` to Agentverse
2. Deploy as "YieldSwarm MeTTa Knowledge"
3. Knowledge base is embedded (lines 55-245) - no external files needed!

---

**More Info:** [Main README](../README.md) | [MeTTa KB File](../metta_kb/defi_protocols.metta)
