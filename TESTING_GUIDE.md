# YieldSwarm AI - Testing Guide

**Version:** 1.0
**Last Updated:** October 21, 2025
**Status:** Production Ready

---

## Quick Start

The easiest way to test YieldSwarm AI is through the deployed coordinator on Agentverse/ASI:One.

**Coordinator Address:** `agent1qwumkwejd0rxnxxu64yrl7vj3f29ydvvq85yntvrvjyzpce86unwxhfdz5a`

---

## Test Scenarios

### ✅ Valid Input Tests

#### 1. Basic Investment Request
```
Input: "Invest 10 ETH with moderate risk"

Expected Response:
- Portfolio allocation with 4 protocols
- Expected APY around 9-12%
- Risk score around 3-4/10
- Mix of Ethereum and Polygon protocols
- MeTTa reasoning explaining choices
```

#### 2. Conservative Strategy
```
Input: "Invest 5 ETH with conservative risk"

Expected Response:
- Lower-risk protocols (Aave, Curve, MakerDAO, Lido)
- Expected APY around 4-7%
- Risk score below 3/10
- Focus on lending and stablecoin protocols
- Reasoning emphasizes capital preservation
```

#### 3. Aggressive Strategy
```
Input: "Invest 20 ETH with aggressive risk"

Expected Response:
- Higher-yield protocols (Raydium, GMX, Uniswap-V3, Trader-Joe)
- Expected APY around 12-18%
- Risk score around 5-7/10
- Mix of DEXes and higher-risk opportunities
- Reasoning mentions maximum yield potential
```

#### 4. Chain-Specific Request
```
Input: "Invest 10 ETH on Ethereum with moderate risk"

Expected Response:
- Only Ethereum-based protocols
- Common protocols: Aave-V3, Uniswap-V3, Curve, Convex
- Single-chain deployment noted
- Lower gas costs mentioned
```

#### 5. Multi-Currency Test
```
Input: "Invest 50 USDC with moderate risk"

Expected Response:
- Portfolio allocation adjusted for USDC
- Stablecoin-focused protocols preferred
- Similar risk/reward profile
```

---

### ⚠️ Invalid Input Tests

#### 1. Greeting
```
Input: "hello"

Expected Response:
👋 Hello! Great to meet you!

I'm YieldSwarm AI - I help optimize DeFi portfolios using 6 specialized AI agents.

**Try these commands:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH with conservative risk on Ethereum"
• "Invest 50 ETH with aggressive risk"

Ready to optimize your yield? Tell me how much you'd like to invest!
```

#### 2. Random Text
```
Input: "sdhflsj"

Expected Response:
🤔 I didn't quite understand that.

I'm specialized in DeFi portfolio optimization. Here's how to use me:

**Example requests:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH with conservative risk"
• "Invest 20 ETH with aggressive risk on Polygon"

**Need help?** Just ask: "How do I use this?" or "Show me examples"

What would you like to invest?
```

#### 3. Help Request
```
Input: "help"

Expected Response:
📚 **YieldSwarm AI - Usage Guide**

I analyze 50+ DeFi protocols across 5 chains and create optimized portfolio strategies.

[Full usage guide with examples]
```

#### 4. Short Input
```
Input: "hi"

Expected Response:
👋 Hello! I'm YieldSwarm AI, your DeFi portfolio optimizer.

[Usage instructions]
```

---

## Response Structure

Every valid investment request should return:

### 1. Portfolio Allocation
```markdown
## 📊 Recommended Allocation

### 1. Uniswap-V3 (ethereum)
- Amount: **3.50 ETH** (35.0%)
- Expected APY: **12.21%**
- Risk Score: 3.5/10

### 2. QuickSwap (polygon)
- Amount: **3.00 ETH** (30.0%)
- Expected APY: **9.75%**
- Risk Score: 4.0/10

[... more allocations ...]
```

### 2. Portfolio Metrics
```markdown
## 📈 Portfolio Metrics
- **Expected APY:** 9.18%
- **Portfolio Risk:** 3.2/10
- **Estimated Gas:** 0.0451 ETH
```

### 3. MeTTa AI Analysis
```markdown
## 🧠 MeTTa AI Analysis
Symbolic Reasoning (MeTTa Knowledge Base):
- Strategy: Balanced risk-reward optimization...
- Chain Diversification: 2 blockchain(s)...
- Knowledge Base: 22 protocols analyzed across 5 chains
```

### 4. Strategy Reasoning
```markdown
## ⚙️ Strategy Reasoning
Portfolio Strategy for MODERATE risk profile:

Allocation Breakdown:
[Detailed breakdown]

Powered by 6 specialized AI agents via YieldSwarm AI 🐝
```

---

## System Flow Verification

### Agent Communication Chain
```
User Input (ASI:One)
    ↓
1. Portfolio Coordinator (validates & parses)
    ↓
2. Chain Scanner (finds opportunities)
    ↓
3. MeTTa Knowledge (symbolic reasoning)
    ↓
4. Strategy Engine (creates allocation)
    ↓
5. Coordinator (sends response to user)
```

### Expected Timing
- Input validation: < 100ms
- Full response: 5-10 seconds (agent-to-agent communication)
- Invalid input response: < 1 second

---

## Edge Cases

### 1. Very Small Amount
```
Input: "Invest 0.1 ETH with moderate risk"

Expected: Should work but warn about gas costs
```

### 2. Very Large Amount
```
Input: "Invest 1000 ETH with moderate risk"

Expected: Should work with diversification across more protocols
```

### 3. Unsupported Chain
```
Input: "Invest 10 ETH on Avalanche"

Expected: Defaults to Ethereum/Polygon (supported chains)
```

### 4. Mixed Keywords
```
Input: "I want to invest 10 eth but be safe about it"

Expected: Parses as 10 ETH conservative risk
```

---

## Verification Checklist

When testing, verify:

- [ ] Input validation catches greetings correctly
- [ ] Input validation catches gibberish correctly
- [ ] Help request provides full guide
- [ ] Valid requests proceed to agents
- [ ] Response includes all 4 sections (allocation, metrics, MeTTa, strategy)
- [ ] Risk levels produce different protocols
  - Conservative: Low-risk protocols (Aave, Curve, Lido)
  - Moderate: Balanced mix
  - Aggressive: High-yield protocols (Raydium, GMX)
- [ ] Chain filtering works correctly
- [ ] MeTTa reasoning mentions knowledge base
- [ ] Portfolio metrics are calculated correctly
- [ ] Response time is reasonable (< 15 seconds)

---

## Known Protocol Distribution

Based on the MeTTa Knowledge Base (22 protocols):

### By Risk Level
- **Low Risk (< 3.0):** MakerDAO, Curve, Lido, Aave-V3, Rocket-Pool, Compound-V3, Frax
- **Medium Risk (3.0-5.0):** Convex, Yearn, Uniswap-V3, Balancer, QuickSwap, Beefy, Stargate, Venus, PancakeSwap
- **High Risk (> 5.0):** Raydium, Solend, GMX, Trader-Joe, Synapse

### By Chain
- **Ethereum:** 13 protocols
- **Polygon:** 11 protocols
- **Arbitrum:** 9 protocols
- **BSC:** 5 protocols
- **Solana:** 3 protocols

---

## Troubleshooting

### Issue: No response
**Solution:** Check agent is running on Agentverse, verify address

### Issue: Wrong protocols recommended
**Solution:** Verify risk level parsing, check MeTTa agent logs

### Issue: Same response for all inputs
**Solution:** Check input validation isn't blocking all requests

### Issue: Error messages
**Solution:** Check agent-to-agent communication, verify all agents deployed

---

## Testing on Local vs Agentverse

### Local Testing
```bash
# Start all agents
./start_all_agents.sh

# Send test request to coordinator
python test_agent_flow.py
```

### Agentverse Testing
- Use ASI:One chat interface
- Send messages directly to coordinator address
- Monitor agent interaction counts on dashboard

---

## Performance Benchmarks

**Expected Performance:**
- Input validation: < 100ms
- Scanner response: 1-2 seconds
- MeTTa analysis: 1-2 seconds
- Strategy generation: 1-2 seconds
- Total response time: 5-10 seconds

**Memory Usage:**
- Coordinator: ~50MB
- Scanner: ~40MB
- MeTTa: ~60MB (knowledge base loaded)
- Strategy: ~45MB

---

## Test Data Examples

### Conservative Portfolio (10 ETH)
Expected protocols: Aave-V3, Curve, MakerDAO, Lido
Expected APY: 4-6%
Expected Risk: 2.0-2.5/10

### Moderate Portfolio (10 ETH)
Expected protocols: Uniswap-V3, QuickSwap, Curve, Aave-V3
Expected APY: 8-12%
Expected Risk: 3.0-4.0/10

### Aggressive Portfolio (10 ETH)
Expected protocols: Raydium, GMX, Trader-Joe, Uniswap-V3
Expected APY: 14-18%
Expected Risk: 5.0-6.5/10

---

## Contact & Support

- **Issues:** https://github.com/your-repo/issues
- **Documentation:** README.md
- **Deployment:** HACKATHON_SUBMISSION_CHECKLIST.md

---

**Last Test Date:** October 21, 2025
**Test Status:** ✅ All scenarios passing
**Ready for Demo:** ✅ YES
