# Local Agent Setup - COMPLETE

## What Was Done

### 1. Converted All Agents from Mailbox to Local Mode

**Changed:**
- `mailbox=True` → `endpoint=["http://127.0.0.1:PORT/submit"]`

**Affected Files:**
- ✅ `agents/chain_scanner.py` (Port 8001)
- ✅ `agents/strategy_engine.py` (Port 8003)
- ✅ `agents/execution_agent.py` (Port 8004)
- ✅ `agents/performance_tracker.py` (Port 8005)
- ✅ `agents/metta_knowledge.py` (Port 8002)
- ✅ `agents/portfolio_coordinator.py` (Port 8000)

### 2. Updated Configuration

**File: `utils/config.py`**
- Added all agent addresses (deterministic, based on seeds)
- Addresses are now available for agent-to-agent communication

### 3. Created Helper Tools

**New Files:**
- `get_agent_addresses.py` - Displays all agent addresses and Inspector URLs
- `LOCAL_AGENT_GUIDE.md` - Comprehensive setup and troubleshooting guide
- `SETUP_COMPLETE.md` - This file

---

## Key Understanding

### The Almanac Warning is NORMAL

```
WARNING: I do not have enough funds to register on Almanac contract
```

**This warning is expected and can be ignored!**

- Local agents use HTTP endpoints for direct communication
- Almanac registration is only for Agentverse-hosted agents
- Your agents will work perfectly without Almanac
- No funds needed for local development

---

## How to Use

### 1. View Agent Addresses
```bash
source venv/bin/activate
python get_agent_addresses.py
```

### 2. Run Chain Scanner (Example)
```bash
source venv/bin/activate
python agents/chain_scanner.py
```

**You'll see:**
- ✅ Agent starts on port 8001
- ✅ Endpoint: http://127.0.0.1:8001/submit
- ✅ Agent Inspector URL displayed
- ⚠️  Almanac warning (IGNORE - this is normal)
- ✅ Agent begins scanning chains

### 3. Monitor with Agent Inspector

Open the Inspector URL in your browser:
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9
```

While your agent is running, you'll see:
- Real-time logs
- Message activity
- Agent state
- Event history

### 4. Run All Agents

Use separate terminals or the script:
```bash
./run_all_agents.sh
```

---

## Agent Inspector URLs

### Chain Scanner
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9

### Strategy Engine
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8003&address=agent1qtf787vn9h78j6quv4fs0axl4xw3s3r39el93rv88jlwz3uvugt02u4tsjy

### Execution Agent
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8004&address=agent1qd0av377w59qnel53yrjf29s2syy43ef4ld6haput6z020jqfjdwqysurfy

### Performance Tracker
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8005&address=agent1qg8chd6dzhpl6hfvgtqvx7q0yhmyx9phyewe6dus3lal8s67qa0sje3k0fk

### MeTTa Knowledge
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1q29zr74zz6q3052glhefcuyv7n24c78lcrjd9lpav7npw48wx8k0k9xa4rh

### Portfolio Coordinator
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8000&address=agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f

---

## Next Steps

### Immediate Testing
1. Run Chain Scanner: `python agents/chain_scanner.py`
2. Open Inspector URL in browser
3. Watch it scan for yield opportunities every 30 seconds

### Enable Inter-Agent Communication

Currently, agents run independently. To enable communication:

**Example: Chain Scanner → Strategy Engine**

In `agents/chain_scanner.py` (around line 218-222), uncomment:
```python
opportunity_data = OpportunityData(
    opportunities=all_opportunities,
    timestamp=datetime.now(timezone.utc)
)
await ctx.send(config.STRATEGY_ADDRESS, opportunity_data)
```

Then add a message handler in `agents/strategy_engine.py`:
```python
@strategy_engine.on_message(model=OpportunityData)
async def handle_opportunities(ctx: Context, sender: str, msg: OpportunityData):
    ctx.logger.info(f"📨 Received {len(msg.opportunities)} opportunities")
    # Process opportunities...
```

### Full System Integration
1. Uncomment all message handlers in agent files
2. Run all 6 agents simultaneously
3. Test end-to-end workflow:
   - Scanner finds opportunities
   - MeTTa provides intelligence
   - Strategy Engine calculates allocation
   - Coordinator approves
   - Execution Agent executes (simulated)
   - Performance Tracker monitors results

---

## Verification Checklist

- ✅ All agents converted to local mode (endpoint-based)
- ✅ Agent addresses added to config
- ✅ Helper script created (get_agent_addresses.py)
- ✅ Documentation created (LOCAL_AGENT_GUIDE.md)
- ✅ Almanac warning understood (it's normal!)
- ✅ Agent Inspector URLs available
- ✅ Ready to run and test

---

## Resources

- **Local Setup Guide**: `LOCAL_AGENT_GUIDE.md`
- **Get Addresses**: `python get_agent_addresses.py`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Testing Guide**: `LOCAL_TESTING_GUIDE.md`

---

## Quick Start

```bash
# Activate environment
source venv/bin/activate

# Test single agent
python agents/chain_scanner.py

# In another terminal, run another agent
python agents/strategy_engine.py

# Open Inspector URLs in browser to monitor
```

You're all set! Your agents are configured for local development with full Inspector support.
