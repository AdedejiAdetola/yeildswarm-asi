# 🧪 YieldSwarm AI - Local Testing Guide

This guide shows you how to test all 6 agents locally and verify they're working correctly.

---

## 🚀 Quick Start - Run All Agents

### Option 1: Automated Launcher (Recommended)
```bash
./run_all_agents.sh
```
This opens 6 terminal windows automatically.

### Option 2: Manual Launch
Open 6 separate terminal windows and run:

```bash
# Terminal 1 - Portfolio Coordinator (ASI:One Interface)
python3 agents/portfolio_coordinator.py

# Terminal 2 - Chain Scanner (Multi-chain Monitoring)
python3 agents/chain_scanner.py

# Terminal 3 - MeTTa Knowledge (DeFi Intelligence)
python3 agents/metta_knowledge.py

# Terminal 4 - Strategy Engine (Optimization)
python3 agents/strategy_engine.py

# Terminal 5 - Execution Agent (Transaction Handling)
python3 agents/execution_agent.py

# Terminal 6 - Performance Tracker (Analytics)
python3 agents/performance_tracker.py
```

---

## ✅ Expected Output Per Agent

### 1. Portfolio Coordinator (Terminal 1)
```
============================================================
YieldSwarm AI - Portfolio Coordinator Agent
============================================================
Agent Address: agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f
Port: 8000
ASI:One Compatible: YES ✓
Environment: development
============================================================

🚀 Starting agent...

INFO: [yieldswarm-coordinator]: Starting agent with address: agent1q...
INFO: [yieldswarm-coordinator]: Portfolio Coordinator Agent started
INFO: [yieldswarm-coordinator]: ASI:One compatible: YES
INFO: [yieldswarm-coordinator]: Chat Protocol: ENABLED
INFO: [yieldswarm-coordinator]: Manifest published successfully: AgentChatProtocol
INFO: [yieldswarm-coordinator]: Starting server on http://0.0.0.0:8000
```

**What to verify:**
- ✅ Agent address starts with `agent1q...`
- ✅ Port 8000 is listening
- ✅ "ASI:One Compatible: YES ✓"
- ✅ "Chat Protocol: ENABLED"
- ✅ "Manifest published successfully"

---

### 2. Chain Scanner (Terminal 2)
```
============================================================
YieldSwarm AI - Chain Scanner Agent
============================================================
Agent Address: agent1q...
Port: 8001
Chains: Ethereum, Solana, BSC, Polygon, Arbitrum
Protocols: 20+ DeFi protocols
Environment: development
============================================================

🚀 Starting 24/7 monitoring...

INFO: [yieldswarm-scanner]: Chain Scanner Agent started
INFO: [yieldswarm-scanner]: Monitoring chains: Ethereum, Solana, BSC, Polygon, Arbitrum
INFO: [yieldswarm-scanner]: Scan interval: 30 seconds
INFO: [yieldswarm-scanner]: Starting server on http://0.0.0.0:8001

[Wait 30 seconds, then you'll see:]

INFO: [yieldswarm-scanner]: 🔍 Scanning all chains for yield opportunities...
INFO: [yieldswarm-scanner]: ✅ Found 12 opportunities
INFO: [yieldswarm-scanner]:   1. Raydium on solana: 22.45% APY (Risk: 5.5)
INFO: [yieldswarm-scanner]:   2. PancakeSwap on bsc: 18.67% APY (Risk: 5.0)
INFO: [yieldswarm-scanner]:   3. GMX on arbitrum: 15.23% APY (Risk: 5.5)
```

**What to verify:**
- ✅ Agent starts on port 8001
- ✅ Lists all 5 chains
- ✅ **Every 30 seconds**, shows scanning activity
- ✅ Shows "Found X opportunities" with APY percentages
- ✅ Top 3 opportunities displayed with risk scores

---

### 3. MeTTa Knowledge (Terminal 3)
```
============================================================
YieldSwarm AI - MeTTa Knowledge Agent
============================================================
Agent Address: agent1q...
Port: 8002
Protocols in Knowledge Base: 7
Environment: development
============================================================

Protocols:
  • Aave-V3: Risk 2.0, TVL $5,000,000,000
  • Uniswap-V3: Risk 3.5, TVL $3,200,000,000
  • Raydium: Risk 5.5, TVL $450,000,000
  • PancakeSwap: Risk 5.0, TVL $1,200,000,000
  • Curve: Risk 2.5, TVL $2,800,000,000
  • Venus: Risk 4.0, TVL $680,000,000
  • Solend: Risk 4.5, TVL $280,000,000

🚀 Starting knowledge agent...

INFO: [yieldswarm-metta]: MeTTa Knowledge Agent started
INFO: [yieldswarm-metta]: Knowledge base loaded: 7 protocols
INFO: [yieldswarm-metta]: MeTTa reasoning: ENABLED (simulated)
INFO: [yieldswarm-metta]:   ✓ Aave-V3
INFO: [yieldswarm-metta]:   ✓ Uniswap-V3
INFO: [yieldswarm-metta]:   ✓ Raydium
INFO: [yieldswarm-metta]:   ✓ PancakeSwap
INFO: [yieldswarm-metta]:   ✓ Curve
INFO: [yieldswarm-metta]: Starting server on http://0.0.0.0:8002

[Wait 5 minutes, then you'll see:]

INFO: [yieldswarm-metta]: 🧠 Updating DeFi knowledge base...
INFO: [yieldswarm-metta]: ✅ Knowledge base updated
```

**What to verify:**
- ✅ Agent starts on port 8002
- ✅ Shows 7 protocols loaded
- ✅ Lists each protocol with risk score and TVL
- ✅ "MeTTa reasoning: ENABLED (simulated)"
- ✅ **Every 5 minutes**, shows knowledge update

---

### 4. Strategy Engine (Terminal 4)
```
============================================================
YieldSwarm AI - Strategy Engine Agent
============================================================
Agent Address: agent1q...
Port: 8003
Optimization: Multi-objective (yield, risk, gas)
Environment: development
============================================================

🚀 Starting strategy optimization...

INFO: [yieldswarm-strategy]: Strategy Engine Agent started
INFO: [yieldswarm-strategy]: Optimization algorithms: ACTIVE
INFO: [yieldswarm-strategy]: Risk profiles: Conservative, Moderate, Aggressive
INFO: [yieldswarm-strategy]: Starting server on http://0.0.0.0:8003
```

**What to verify:**
- ✅ Agent starts on port 8003
- ✅ Shows optimization algorithms active
- ✅ Lists all 3 risk profiles
- ✅ Server running and ready for strategy requests

---

### 5. Execution Agent (Terminal 5)
```
============================================================
YieldSwarm AI - Execution Agent
============================================================
Agent Address: agent1q...
Port: 8004
Safety Features: MEV Protection, Transaction Simulation
Environment: development
============================================================

🚀 Starting execution engine...

INFO: [yieldswarm-execution]: Execution Agent started
INFO: [yieldswarm-execution]: MEV protection: ENABLED
INFO: [yieldswarm-execution]: Transaction simulation: ENABLED
INFO: [yieldswarm-execution]: Cross-chain bridges: 5 supported
INFO: [yieldswarm-execution]: Starting server on http://0.0.0.0:8004
```

**What to verify:**
- ✅ Agent starts on port 8004
- ✅ "MEV protection: ENABLED"
- ✅ "Transaction simulation: ENABLED"
- ✅ Shows cross-chain bridge support
- ✅ Server ready for execution requests

---

### 6. Performance Tracker (Terminal 6)
```
============================================================
YieldSwarm AI - Performance Tracker Agent
============================================================
Agent Address: agent1q...
Port: 8005
Tracking: P&L, APY, Gas Costs, Tax Reports
Environment: development
============================================================

🚀 Starting performance tracking...

INFO: [yieldswarm-tracker]: Performance Tracker Agent started
INFO: [yieldswarm-tracker]: Portfolio tracking: ENABLED
INFO: [yieldswarm-tracker]: Tax reporting: ENABLED (IRS Form 8949 ready)
INFO: [yieldswarm-tracker]: Update interval: 3600 seconds (1 hour)
INFO: [yieldswarm-tracker]: Starting server on http://0.0.0.0:8005

[Wait 1 hour, then you'll see:]

INFO: [yieldswarm-tracker]: 🔄 Tracking portfolio performance...
INFO: [yieldswarm-tracker]: ✅ Performance metrics updated
```

**What to verify:**
- ✅ Agent starts on port 8005
- ✅ "Portfolio tracking: ENABLED"
- ✅ "Tax reporting: ENABLED"
- ✅ **Every hour**, shows performance update
- ✅ Server ready for analytics requests

---

## 🧪 Run the Test Suite

After all agents are running, run the test script:

```bash
python3 test_local_interaction.py
```

This will:
1. Check if all 6 agents are reachable
2. Verify their HTTP endpoints
3. Show expected outputs
4. Guide you through next steps

---

## 📊 What Should Be Happening

### Active Agents (Always)
- **Portfolio Coordinator**: Listening for ASI:One messages on port 8000
- **All Agents**: HTTP servers running, ready to receive inter-agent messages

### Periodic Activity

| Agent | Interval | Activity |
|-------|----------|----------|
| **Chain Scanner** | Every 30s | Scans all chains, logs top 3 opportunities |
| **MeTTa Knowledge** | Every 5m | Updates DeFi knowledge base |
| **Performance Tracker** | Every 1h | Updates portfolio metrics |
| **Strategy Engine** | On-demand | Processes strategy requests |
| **Execution Agent** | On-demand | Executes transactions |
| **Portfolio Coordinator** | On-demand | Processes user chat messages |

---

## ⚠️ Common Issues

### "Address already in use" error
One of the ports (8000-8005) is already taken.
```bash
# Find what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### "No module named 'uagents'" error
Dependencies not installed in current environment.
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Warning: "No endpoints provided. Skipping registration"
This is **normal** for local testing! It means the agent isn't registered on Agentverse yet.
- Agents still work locally
- To fix: Add mailbox keys to `.env` and deploy to Agentverse

---

## ✅ Success Checklist

- [ ] All 6 agents started without errors
- [ ] Each agent shows its unique address (agent1q...)
- [ ] All agents on different ports (8000-8005)
- [ ] Chain Scanner logs opportunities every 30 seconds
- [ ] MeTTa Knowledge updates every 5 minutes
- [ ] No "ImportError" or "ModuleNotFoundError" messages
- [ ] Each agent shows "Starting server on http://0.0.0.0:PORT"

---

## 🚀 Next Steps

### 1. Local Testing Complete ✅
All agents running and showing activity? Great!

### 2. Deploy to Agentverse 🌐
```bash
# Get mailbox keys
1. Go to https://agentverse.ai
2. Create account (free)
3. Create 6 agents → Get 6 mailbox keys
4. Update .env with keys:
   COORDINATOR_MAILBOX_KEY="..."
   SCANNER_MAILBOX_KEY="..."
   # etc.

# Restart all agents with mailbox keys
# They'll auto-register on Agentverse
```

### 3. Test via ASI:One 💬
```bash
1. Go to https://asi1.ai
2. Search for "yieldswarm-coordinator"
3. Start chat session
4. Try: "Invest 5 ETH with moderate risk"
5. See your agent respond!
```

### 4. Record Demo Video 📹
- Show all 6 agents running
- Demonstrate ASI:One interaction
- Explain multi-agent coordination
- Show MeTTa knowledge base
- 3-5 minutes total

### 5. Submit to Hackathon 🏆
- Push code to GitHub (public repo)
- Upload demo video
- Fill out submission form
- Include all agent addresses

---

## 🐝 YieldSwarm AI - Ready to Win!

**Status**: ✅ Local testing complete
**Next**: 🚀 Deploy to Agentverse
**Goal**: 🏆 Win the ASI Alliance Hackathon

---

*For more info, see:*
- `README.md` - Complete project overview
- `DEPLOYMENT_GUIDE.md` - Agentverse deployment steps
- `WINNING_PROJECT_PLAN.md` - Full project strategy
