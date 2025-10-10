# 🚀 YieldSwarm AI - Quick Reference Card

## ⚡ Start All Agents (Choose One Method)

### Method 1: Automated Script
```bash
./run_all_agents.sh
```

### Method 2: Manual (6 terminals)
```bash
python3 agents/portfolio_coordinator.py    # Terminal 1 - Port 8000
python3 agents/chain_scanner.py            # Terminal 2 - Port 8001
python3 agents/metta_knowledge.py          # Terminal 3 - Port 8002
python3 agents/strategy_engine.py          # Terminal 4 - Port 8003
python3 agents/execution_agent.py          # Terminal 5 - Port 8004
python3 agents/performance_tracker.py      # Terminal 6 - Port 8005
```

---

## 📋 Agent Ports Reference

| Agent | Port | Purpose |
|-------|------|---------|
| Portfolio Coordinator | 8000 | ASI:One interface |
| Chain Scanner | 8001 | Multi-chain monitoring |
| MeTTa Knowledge | 8002 | DeFi intelligence |
| Strategy Engine | 8003 | Optimization |
| Execution Agent | 8004 | Transaction handling |
| Performance Tracker | 8005 | Analytics |

---

## 🧪 Testing Commands

```bash
# Test all dependencies
python3 test_agents.py

# Test agent interactions
python3 test_local_interaction.py

# Check if agents are running
curl http://localhost:8000/  # Portfolio Coordinator
curl http://localhost:8001/  # Chain Scanner
# ... etc for all ports
```

---

## 🔑 Environment Variables (.env)

```bash
# Minimum required for local testing
COORDINATOR_SEED="yieldswarm-coordinator-dev-2025"
SCANNER_SEED="yieldswarm-scanner-dev-2025"
# ... etc

# Required for Agentverse deployment
COORDINATOR_MAILBOX_KEY="get from agentverse.ai"
SCANNER_MAILBOX_KEY="get from agentverse.ai"
# ... etc (6 total)
```

---

## 📊 Expected Activity Logs

| Agent | Frequency | What to Look For |
|-------|-----------|------------------|
| Chain Scanner | Every 30s | "Found X opportunities" + top 3 yields |
| MeTTa Knowledge | Every 5m | "Updating DeFi knowledge base..." |
| Performance Tracker | Every 1h | "Tracking portfolio performance..." |
| Others | On-demand | "Starting server" message |

---

## 🌐 Agentverse Deployment

1. **Get Mailbox Keys**
   - Go to: https://agentverse.ai
   - Sign up (free)
   - Create 6 agents
   - Copy 6 mailbox API keys

2. **Update .env**
   ```bash
   COORDINATOR_MAILBOX_KEY="your-key-1"
   SCANNER_MAILBOX_KEY="your-key-2"
   # ... etc
   ```

3. **Restart Agents**
   - Kill all agents (Ctrl+C)
   - Restart with: `./run_all_agents.sh`
   - Check Agentverse dashboard

4. **Verify Registration**
   - All 6 agents visible in Agentverse
   - Copy agent addresses
   - Update README.md with addresses

---

## 💬 Testing via ASI:One

1. Go to: https://asi1.ai
2. Search: "yieldswarm-coordinator"
3. Start chat
4. Test commands:
   - "Invest 5 ETH with moderate risk"
   - "Show my portfolio"
   - "What's the best strategy on Ethereum?"

---

## 🎬 Demo Video Checklist

Record 3-5 minute video showing:
- [ ] All 6 agents running (show terminals)
- [ ] Chain Scanner finding opportunities
- [ ] ASI:One interaction (natural language)
- [ ] Explain multi-agent coordination
- [ ] Show MeTTa knowledge base concept
- [ ] Explain cross-chain capabilities
- [ ] Show agent addresses on Agentverse

---

## 📤 Hackathon Submission

- [ ] GitHub repo public
- [ ] README.md has agent addresses
- [ ] Demo video uploaded (YouTube/Vimeo)
- [ ] Innovation Lab badges present
- [ ] All 6 agents on Agentverse
- [ ] Chat Protocol working on ASI:One
- [ ] Submission form completed

---

## ⚠️ Troubleshooting

**Port already in use?**
```bash
lsof -i :8000  # Check what's using port
kill -9 <PID>  # Kill the process
```

**Module not found?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Warning "No endpoints provided"?**
- Normal for local testing
- Add mailbox keys to deploy to Agentverse

---

## 🏆 Success Criteria

✅ All 6 agents running without errors
✅ Chain Scanner shows opportunities every 30s
✅ MeTTa updates every 5 minutes
✅ All agents on Agentverse (for submission)
✅ ASI:One chat working
✅ Demo video recorded
✅ GitHub repo public

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, setup guide |
| `LOCAL_TESTING_GUIDE.md` | Detailed testing instructions |
| `DEPLOYMENT_GUIDE.md` | Agentverse deployment steps |
| `WINNING_PROJECT_PLAN.md` | Complete hackathon strategy |
| `.env` | Configuration (NEVER commit to git) |
| `test_agents.py` | Verify dependencies |
| `run_all_agents.sh` | Launch all agents |

---

## 🐝 YieldSwarm AI

**Your autonomous multi-chain DeFi yield optimizer**

6 AI Agents | 5 Blockchains | 20+ Protocols | Powered by ASI Alliance

*Ready to win! 🏆*
