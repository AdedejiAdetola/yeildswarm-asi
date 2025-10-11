# YieldSwarm AI - Quick Action Guide

## 🎯 What You Need to Do RIGHT NOW (In Order)

### 1️⃣ Test ASI:One (15 minutes) - CRITICAL

```bash
# Step 1: Ensure Portfolio Coordinator is running
ps aux | grep portfolio_coordinator

# If not running:
source venv/bin/activate
python agents/portfolio_coordinator.py
```

**Then**:
1. Open browser: https://asi1.ai
2. Search: **"yieldswarm-coordinator"**
3. OR search by address: **agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f**
4. If found: Start chat and test
5. If not found: Wait 10 minutes, try again

**Test Commands**:
```
help
Invest 5 ETH with moderate risk
Show my portfolio
```

---

### 2️⃣ Update README (15 minutes) - CRITICAL

Add these at the top of README.md:

```markdown
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## 🤖 Try It on ASI:One

Visit https://asi1.ai and search for **"yieldswarm-coordinator"**

Test command: `Invest 10 ETH with moderate risk on Ethereum`

## 📋 Agent Addresses

| Agent | Address | ASI:One | Port |
|-------|---------|---------|------|
| **Portfolio Coordinator** | `agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f` | ✅ YES | 8000 |
| **Chain Scanner** | `agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9` | - | 8001 |
| **MeTTa Knowledge** | `agent1q29zr74zz6q3052glhefcuyv7n24c78lcrjd9lpav7npw48wx8k0k9xa4rh` | - | 8002 |
| **Strategy Engine** | `agent1qtf787vn9h78j6quv4fs0axl4xw3s3r39el93rv88jlwz3uvugt02u4tsjy` | - | 8003 |
| **Execution Agent** | `agent1qd0av377w59qnel53yrjf29s2syy43ef4ld6haput6z020jqfjdwqysurfy` | - | 8004 |
| **Performance Tracker** | `agent1qg8chd6dzhpl6hfvgtqvx7q0yhmyx9phyewe6dus3lal8s67qa0sje3k0fk` | - | 8005 |
```

---

### 3️⃣ Record Demo Video (60 minutes) - CRITICAL

**Script** (Practice this first):

**0:00-0:30 - Introduction**
> "Hi, I'm presenting YieldSwarm AI - an autonomous multi-agent DeFi yield optimizer built for the ASI Alliance Hackathon.
>
> The problem: Finding optimal yields across multiple chains and protocols is complex and time-consuming.
>
> Our solution: 6 specialized AI agents that work together to scan, analyze, and optimize your DeFi investments in real-time."

**0:30-2:30 - Live Demo**
> "Let me show you how it works on ASI:One..."
>
> [Switch to browser showing https://asi1.ai]
>
> "I'm searching for our Portfolio Coordinator agent... here it is.
>
> [Click on agent, start chat]
>
> Let me make an investment request: 'Invest 10 ETH with moderate risk on Ethereum and Polygon'
>
> [Show agent response]
>
> You can see the Portfolio Coordinator parsing my request and immediately coordinating with the other 5 agents:
> - Chain Scanner finds opportunities
> - MeTTa Knowledge analyzes protocol risks
> - Strategy Engine calculates optimal allocation
> - Execution Agent would handle transactions
> - Performance Tracker monitors results"

**2:30-3:30 - Technical Architecture**
> [Switch to terminal/code]
>
> "Under the hood, we're using:
> - Fetch.ai's uAgents framework for all 6 agents
> - The Chat Protocol for ASI:One compatibility
> - MeTTa knowledge graphs for intelligent decision-making
> - Multi-chain RPC connections to Ethereum, Solana, BSC, Polygon, and Arbitrum
>
> [Show terminal logs]
>
> You can see the Chain Scanner actively finding opportunities across 5 chains... it's discovered 11 protocols offering 17-24% APY."

**3:30-4:00 - Impact & Conclusion**
> "YieldSwarm AI solves a real problem: automated, intelligent yield optimization across multiple chains.
>
> Users can simply chat in natural language, and our agent swarm handles the complexity.
>
> Try it yourself at asi1.ai - search for 'yieldswarm-coordinator'.
>
> Thank you!"

**Recording Tips**:
1. Use OBS Studio or Loom (free)
2. Record in 1080p
3. Use clear audio (test first)
4. Show: ASI:One chat + terminal logs side by side
5. Keep it under 5 minutes
6. Add captions if possible

---

## 📊 Current Status Summary

### ✅ What's Working:
- All 6 agents deployed with mailbox mode
- Almanac registration successful
- Portfolio Coordinator has full Chat Protocol
- Multi-chain scanning active (11 opportunities found!)
- Agent coordination architecture complete

### 🎯 What You Need:
1. Test ASI:One (verify it works)
2. Add badges to README
3. Record demo video

**You're 80% done! Just need documentation and demo.**

---

## 🚨 Common Issues & Quick Fixes

### "Can't find agent on ASI:One"
**Fix**: Wait 10-15 minutes for Almanac propagation

### "Agent not running"
```bash
# Start all agents
bash deploy_agents.sh

# Check they're running
ps aux | grep "python agents"
```

### "Need to stop agents"
```bash
pkill -f "python agents/"
```

### "Check agent logs"
```bash
# All logs
tail -f logs/*.log

# Just coordinator
tail -f logs/coordinator.log
```

---

## 📁 File Checklist for Submission

Required in your GitHub repo:

- [ ] README.md with badges
- [ ] Agent addresses table
- [ ] Instructions to run
- [ ] Demo video (3-5 min)
- [ ] All agent code files
- [ ] requirements.txt
- [ ] .env.example (NO real keys!)
- [ ] Clear architecture documentation

---

## 🎬 After You Submit

1. Keep agents running during judging period
2. Monitor ASI:One for any test interactions
3. Be ready to demo live if needed
4. Check GitHub repo is public

---

## 💡 Quick Win Ideas (If You Have Extra Time)

1. **Add screenshots to README**: ASI:One chat + Agentverse dashboard
2. **Create architecture diagram**: Visual showing 6 agents
3. **Add more examples**: Show different risk levels, chains
4. **Enhance error handling**: Better user messages in chat
5. **Add metrics**: Show real performance data in agent logs

---

## 🏆 Success Formula

Your project **will score well** if:

1. ✅ ASI:One chat works flawlessly
2. ✅ Demo video is clear and engaging
3. ✅ Documentation is comprehensive
4. ✅ Code is clean and well-commented
5. ✅ Real-world problem clearly solved

**Focus on these 3 things NOW**:
1. Test ASI:One (15 min)
2. Update README (15 min)
3. Record video (60 min)

Total: **90 minutes to submission-ready** 🚀

---

## 📞 Need Help?

Check these resources:
- Full deployment plan: `DEPLOYMENT_PLAN.md`
- Agent logs: `logs/` directory
- Agentverse docs: https://docs.agentverse.ai
- ASI:One: https://asi1.ai

---

**You've got this! The hard part (building the agents) is done. Now just showcase it! 💪**
