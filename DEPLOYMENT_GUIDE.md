# YieldSwarm AI - Deployment Guide

## 🎯 Overview

This guide walks you through deploying YieldSwarm AI agents to Agentverse and testing via ASI:One.

---

## 📋 Prerequisites

- ✅ All 6 agents built and tested locally
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Agentverse account created at [agentverse.ai](https://agentverse.ai)

---

## 🚀 Step-by-Step Deployment

### Step 1: Get Agentverse Mailbox Keys

1. Go to [https://agentverse.ai](https://agentverse.ai)
2. Sign in / Create account
3. Navigate to "Agents" → "Create Agent"
4. For each agent, get a mailbox API key:
   - Click "Local Agents"
   - Click "Connect Local Agent"
   - Copy the Mailbox API Key

You need **6 mailbox keys** (one for each agent):
- Portfolio Coordinator
- Chain Scanner
- MeTTa Knowledge
- Strategy Engine
- Execution Agent
- Performance Tracker

### Step 2: Configure Environment Variables

Edit your `.env` file:

```bash
# Agentverse Mailbox Keys
COORDINATOR_MAILBOX_KEY="your-coordinator-mailbox-key-here"
SCANNER_MAILBOX_KEY="your-scanner-mailbox-key-here"
METTA_MAILBOX_KEY="your-metta-mailbox-key-here"
STRATEGY_MAILBOX_KEY="your-strategy-mailbox-key-here"
EXECUTION_MAILBOX_KEY="your-execution-mailbox-key-here"
TRACKER_MAILBOX_KEY="your-tracker-mailbox-key-here"

# Agent Seeds (use unique phrases for production)
COORDINATOR_SEED="my-unique-coordinator-seed-phrase"
SCANNER_SEED="my-unique-scanner-seed-phrase"
METTA_SEED="my-unique-metta-seed-phrase"
STRATEGY_SEED="my-unique-strategy-seed-phrase"
EXECUTION_SEED="my-unique-execution-seed-phrase"
TRACKER_SEED="my-unique-tracker-seed-phrase"

# Environment
ENVIRONMENT="production"  # Change to production for deployment
```

⚠️ **Important**: Use the same seed phrase across sessions to maintain the same agent address!

### Step 3: Deploy Agents

Open 6 terminal windows and run each agent:

#### Terminal 1: Portfolio Coordinator
```bash
source venv/bin/activate
python agents/portfolio_coordinator.py
```

Look for output:
```
Portfolio Coordinator Agent started
Agent address: agent1q2x3y4z5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p1q2
ASI:One compatible: YES
Chat Protocol: ENABLED
Manifest published successfully: AgentChatProtocol
Registration on Almanac API successful
```

**Copy the agent address!** You'll need it for the README.

#### Terminal 2: Chain Scanner
```bash
source venv/bin/activate
python agents/chain_scanner.py
```

#### Terminal 3: MeTTa Knowledge
```bash
source venv/bin/activate
python agents/metta_knowledge.py
```

#### Terminal 4: Strategy Engine
```bash
source venv/bin/activate
python agents/strategy_engine.py
```

#### Terminal 5: Execution Agent
```bash
source venv/bin/activate
python agents/execution_agent.py
```

#### Terminal 6: Performance Tracker
```bash
source venv/bin/activate
python agents/performance_tracker.py
```

### Step 4: Verify Registration on Agentverse

1. Go to [Agentverse Dashboard](https://agentverse.ai)
2. Navigate to "Agents"
3. You should see all 6 agents listed:
   - yieldswarm-coordinator (with Chat Protocol badge)
   - yieldswarm-scanner
   - yieldswarm-metta
   - yieldswarm-strategy
   - yieldswarm-execution
   - yieldswarm-tracker

4. Check each agent's details:
   - ✅ Agent address visible
   - ✅ Status: Online
   - ✅ Protocol manifest published (for coordinator)

### Step 5: Update README with Agent Addresses

Edit `README.md` and add the actual agent addresses:

```markdown
## 🤖 Agent Addresses (Agentverse)

| Agent | Address | ASI:One Compatible | Port |
|-------|---------|-------------------|------|
| **Portfolio Coordinator** | `agent1q2x3y4z5...` | ✅ YES | 8000 |
| **Chain Scanner** | `agent1qa1b2c3d4...` | - | 8001 |
| **MeTTa Knowledge** | `agent1qe5f6g7h8...` | - | 8002 |
| **Strategy Engine** | `agent1qi9j0k1l2...` | - | 8003 |
| **Execution Agent** | `agent1qm3n4o5p6...` | - | 8004 |
| **Performance Tracker** | `agent1qq7r8s9t0...` | - | 8005 |
```

---

## 🧪 Testing via ASI:One

### Step 1: Access ASI:One Interface

1. Go to [ASI:One](https://asi1.ai) (or relevant ASI:One interface)
2. Sign in with your account

### Step 2: Find Your Agent

1. Search for "yieldswarm-coordinator"
2. Or search by agent address: `agent1q...`
3. Click on the agent to open chat

### Step 3: Test Natural Language Interaction

Try these test commands:

#### Test 1: Help Command
```
You: "help"

Expected Response:
🤖 YieldSwarm AI Commands:
Investment: 'Invest [amount] [currency] with [risk] risk'
Portfolio: 'Show my portfolio' or 'Check performance'
...
```

#### Test 2: Conservative Investment
```
You: "I want to invest 5 ETH conservatively on Ethereum"

Expected Response:
✅ Investment Request Parsed:
Amount: 5.0 ETH
Risk Level: conservative
Chains: ethereum
...
```

#### Test 3: Aggressive Multi-Chain
```
You: "Maximize 10 ETH aggressively across Solana and BSC"

Expected Response:
✅ Investment Request Parsed:
Amount: 10.0 ETH
Risk Level: aggressive
Chains: solana, bsc
...
```

#### Test 4: Portfolio Status
```
You: "Show my portfolio"

Expected Response:
📊 Portfolio Status:
...
```

### Step 4: Verify Agent Logs

Check terminal outputs to see agents responding:

- **Coordinator**: Should log "Received message from..."
- **Scanner**: Should continue scanning chains
- **Other agents**: Should show ready status

---

## 🎥 Recording Demo Video

### Preparation

1. ✅ All agents running and registered on Agentverse
2. ✅ ASI:One interface accessible
3. ✅ Test interactions working
4. ✅ Screen recording software ready (OBS, Loom, etc.)

### Video Structure (3-5 minutes)

#### Segment 1: Problem Statement (30 seconds)
- Explain DeFi yield optimization challenge
- Show market size ($20B+)
- Highlight pain points (manual management, missed opportunities)

#### Segment 2: Solution Overview (45 seconds)
- Introduce YieldSwarm AI
- Show 6-agent architecture diagram
- Highlight ASI Alliance technology stack

#### Segment 3: Live Demo (2 minutes)
**Screen recording:**
1. Open ASI:One interface
2. Find yieldswarm-coordinator agent
3. Start chat session
4. Demo 1: "Invest 5 ETH conservatively on Ethereum"
   - Show parsed request
   - Show strategy generation
5. Demo 2: "Show my portfolio"
   - Show portfolio metrics
6. Show terminal windows with agents working
7. Show Agentverse dashboard with all 6 agents online

#### Segment 4: Technical Highlights (45 seconds)
- MeTTa knowledge graphs (show code snippet)
- Multi-agent coordination
- Cross-chain capabilities
- MEV protection

#### Segment 5: Impact & Conclusion (30 seconds)
- Real-world impact (15-30% return improvement)
- Market opportunity
- ASI Alliance integration
- Call to action

### Recording Tips

- **Resolution**: 1920x1080 minimum
- **Frame rate**: 30 fps minimum
- **Audio**: Clear narration with good microphone
- **Pace**: Not too fast, allow viewers to read text
- **Highlight**: Use cursor highlights or zoom for important parts
- **Edit**: Cut any errors or long pauses

---

## 📝 Final Submission Checklist

Before submitting to the hackathon:

### Code & Repository
- [ ] All 6 agents implemented and tested
- [ ] Git repository initialized with clear commit history
- [ ] README.md with Innovation Lab badges
- [ ] Agent addresses documented in README
- [ ] .env.example provided (no secrets!)
- [ ] requirements.txt complete
- [ ] Code comments clear and helpful

### Documentation
- [ ] README.md comprehensive
- [ ] SETUP.md with installation instructions
- [ ] DEPLOYMENT_GUIDE.md (this file)
- [ ] WINNING_PROJECT_PLAN.md included
- [ ] Architecture diagrams (in README)

### Deployment
- [ ] All agents registered on Agentverse
- [ ] Chat Protocol enabled and working
- [ ] Protocol manifests published
- [ ] Agents discoverable in Almanac
- [ ] ASI:One interaction tested and working

### Demo Video
- [ ] Video recorded (3-5 minutes)
- [ ] Uploaded to YouTube/Vimeo
- [ ] Link added to README
- [ ] Shows live agent interaction
- [ ] Demonstrates all key features

### Submission Form
- [ ] GitHub repository link
- [ ] Demo video link
- [ ] Agent addresses provided
- [ ] Project description submitted
- [ ] All hackathon requirements met

---

## 🐛 Troubleshooting

### Issue: Agent won't start
**Solution:**
- Check `.env` configuration
- Verify Python 3.10+ installed
- Check all dependencies installed: `pip list`
- Look for port conflicts (8000-8005)

### Issue: Agent not appearing on Agentverse
**Solution:**
- Verify mailbox key is correct in `.env`
- Check agent logs for "Registration successful" message
- Ensure internet connection stable
- Try restarting agent

### Issue: Chat Protocol not working
**Solution:**
- Verify `publish_manifest=True` in coordinator agent
- Check logs for "Manifest published successfully"
- Restart coordinator agent
- Clear ASI:One cache

### Issue: Agents can't communicate
**Solution:**
- Verify all agents running simultaneously
- Check agent addresses are correct in config
- Look for network/firewall issues
- Check logs for connection errors

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ All 6 agents visible on Agentverse dashboard
✅ Portfolio Coordinator discoverable on ASI:One
✅ Natural language chat working
✅ Agents logging activity correctly
✅ Demo video recorded and uploaded
✅ README updated with agent addresses
✅ All documentation complete

---

## 🏆 Ready to Win!

With YieldSwarm AI deployed:

- **Functionality**: 6 agents working together ✅
- **ASI Tech**: Full stack integration ✅
- **Innovation**: First symbolic AI DeFi optimizer ✅
- **Impact**: Solves $20B+ market problem ✅
- **Presentation**: Professional docs + demo ✅

**Good luck with the hackathon! 🚀**

---

## 📞 Need Help?

- Check [SETUP.md](SETUP.md) for installation issues
- Review [README.md](README.md) for architecture details
- See [WINNING_PROJECT_PLAN.md](WINNING_PROJECT_PLAN.md) for full context
- Agentverse docs: https://docs.agentverse.ai
- Fetch.ai docs: https://docs.fetch.ai
