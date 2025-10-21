# 👀 Chain Scanner Agent

**Address:** `agent1qtn2hgpdfl0he2h88xncvrdvyk5vd9xtsruw9vzua8tgnejtxxpzy8suu8r`
**Status:** ✅ Production Ready | Internal Agent

## Overview

Multi-chain opportunity detection engine. Monitors 5 blockchains and 20+ DeFi protocols to find yield opportunities matching user criteria.

## Key Features

- 🌐 5 chains: Ethereum, Polygon, Solana, BSC, Arbitrum
- 📊 20+ protocols: Uniswap, Aave, Raydium, PancakeSwap, GMX, etc.
- 🔍 Risk-based filtering (APY, risk score, chains)
- 📈 Realistic APY variations with market dynamics
- ⚡ Self-contained (no external dependencies)

## Supported Protocols

| Chain | Protocols | Risk Range |
|-------|-----------|------------|
| **Ethereum** | Aave-V3, Uniswap-V3, Curve | 2.0-3.5 |
| **Polygon** | Aave-V3, QuickSwap | 2.0-4.0 |
| **Solana** | Raydium, Solend | 5.5-6.0 |
| **BSC** | PancakeSwap, Venus | 4.8-5.0 |
| **Arbitrum** | GMX, Uniswap-V3 | 3.5-5.5 |

## How It Works

1. **Receive Request** - Get chains, min APY, max risk from Coordinator
2. **Generate Opportunities** - Create realistic APY variations for each protocol
3. **Filter** - Keep only opportunities matching criteria
4. **Send Response** - Return filtered opportunities to Coordinator

## Example

**Request:**
```json
{
  "chains": ["ethereum", "polygon"],
  "min_apy": 4.0,
  "max_risk_score": 5.0
}
```

**Response:**
```json
{
  "opportunities": [
    {"protocol": "Uniswap-V3", "apy": 12.3, "risk_score": 3.5},
    {"protocol": "QuickSwap", "apy": 9.8, "risk_score": 4.0},
    {"protocol": "Curve", "apy": 6.1, "risk_score": 2.5}
  ]
}
```

## Deployment

1. Copy `agents_agentverse/1_chain_scanner.py` to Agentverse
2. Deploy as "YieldSwarm Chain Scanner"
3. Copy agent address for coordinator configuration

---

**More Info:** [Main README](../README.md) | [Testing Guide](../TESTING_GUIDE.md)
