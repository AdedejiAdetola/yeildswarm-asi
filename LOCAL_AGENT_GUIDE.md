# Local Agent Setup Guide

## Understanding Local vs Hosted Agents

### Hosted Agents (Agentverse)
- Use `mailbox=True`
- Run on Agentverse cloud platform
- Require mailbox keys and Almanac registration
- Need funds for Almanac contract registration
- Communicate via Agentverse infrastructure

### Local Agents (What we're using)
- Use `endpoint=["http://127.0.0.1:PORT/submit"]`
- Run on your local machine
- **NO Almanac registration required**
- **NO funds needed**
- Communicate directly via HTTP endpoints
- Can use Agent Inspector for monitoring

---

## Current Setup

All agents have been configured for **LOCAL MODE**:

### Agent Configuration

| Agent | Port | Address | Endpoint |
|-------|------|---------|----------|
| Portfolio Coordinator | 8000 | `agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f` | http://127.0.0.1:8000/submit |
| Chain Scanner | 8001 | `agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9` | http://127.0.0.1:8001/submit |
| MeTTa Knowledge | 8002 | `agent1q29zr74zz6q3052glhefcuyv7n24c78lcrjd9lpav7npw48wx8k0k9xa4rh` | http://127.0.0.1:8002/submit |
| Strategy Engine | 8003 | `agent1qtf787vn9h78j6quv4fs0axl4xw3s3r39el93rv88jlwz3uvugt02u4tsjy` | http://127.0.0.1:8003/submit |
| Execution Agent | 8004 | `agent1qd0av377w59qnel53yrjf29s2syy43ef4ld6haput6z020jqfjdwqysurfy` | http://127.0.0.1:8004/submit |
| Performance Tracker | 8005 | `agent1qg8chd6dzhpl6hfvgtqvx7q0yhmyx9phyewe6dus3lal8s67qa0sje3k0fk` | http://127.0.0.1:8005/submit |

---

## Running Local Agents

### Option 1: Individual Terminals (Recommended for Development)

Open 6 separate terminals and run:

```bash
# Terminal 1 - Chain Scanner
source venv/bin/activate
python agents/chain_scanner.py

# Terminal 2 - MeTTa Knowledge
source venv/bin/activate
python agents/metta_knowledge.py

# Terminal 3 - Strategy Engine
source venv/bin/activate
python agents/strategy_engine.py

# Terminal 4 - Execution Agent
source venv/bin/activate
python agents/execution_agent.py

# Terminal 5 - Performance Tracker
source venv/bin/activate
python agents/performance_tracker.py

# Terminal 6 - Portfolio Coordinator
source venv/bin/activate
python agents/portfolio_coordinator.py
```

### Option 2: Use the run_all_agents.sh Script

```bash
chmod +x run_all_agents.sh
./run_all_agents.sh
```

---

## Agent Inspector

Each agent exposes an Agent Inspector URL for real-time monitoring:

### Chain Scanner Inspector
```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9
```

Simply open this URL in your browser while the agent is running to see:
- Live agent status
- Message history
- Agent interactions
- Event logs

**For other agents**: Run `python get_agent_addresses.py` to get all Inspector URLs.

---

## Understanding the Almanac Warning

When you run a local agent, you'll see:

```
WARNING: [uagents.registration]: I do not have enough funds to register on Almanac contract
```

**This is NORMAL and EXPECTED for local agents!**

- Local agents don't need Almanac registration
- They communicate directly via HTTP endpoints
- The warning can be safely ignored
- Almanac registration is only for hosted agents on Agentverse

---

## How Local Agents Communicate

### 1. Each Agent Runs on Its Own Port

```python
scanner = Agent(
    name="yieldswarm-scanner",
    seed=config.SCANNER_SEED,
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)
```

### 2. Agents Send Messages Using Addresses

```python
# Chain Scanner sends opportunities to Strategy Engine
await ctx.send(
    config.STRATEGY_ADDRESS,  # Target agent address
    opportunity_data          # Message payload
)
```

### 3. No Almanac Needed

Local agents:
- Use HTTP for direct communication
- Discover each other via addresses (not Almanac)
- Don't require blockchain transactions
- Work completely offline

---

## Testing Local Communication

### Get All Agent Addresses
```bash
source venv/bin/activate
python get_agent_addresses.py
```

### Test Agent Interaction
```bash
source venv/bin/activate
python test_local_interaction.py
```

---

## Troubleshooting

### Agent Won't Start
- Check if port is already in use: `lsof -i :8001`
- Make sure venv is activated
- Verify all dependencies installed: `pip install -r requirements.txt`

### Agents Can't Communicate
- Ensure all agents are running
- Check firewall isn't blocking localhost connections
- Verify agent addresses in `utils/config.py` match running agents

### "Module not found" Errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Key Differences from Mailbox Mode

| Feature | Mailbox Mode (Agentverse) | Local Mode (Endpoints) |
|---------|--------------------------|------------------------|
| Configuration | `mailbox=True` | `endpoint=["http://..."]` |
| Almanac Registration | Required (needs funds) | Not required |
| Communication | Via Agentverse | Direct HTTP |
| Running Location | Cloud | Your machine |
| Agent Inspector | Limited | Full access via URL |
| Suitable For | Production deployment | Development & testing |

---

## Next Steps

1. **Run all agents** using individual terminals or the script
2. **Open Agent Inspector** in browser to monitor Chain Scanner
3. **Test communication** using `test_local_interaction.py`
4. **Enable message handlers** in agent code (currently commented out)
5. **Build full workflow** with agents communicating

---

## Enabling Agent-to-Agent Communication

Currently, message handlers are commented out in the agent files. To enable:

### Example: Chain Scanner → Strategy Engine

In `agents/chain_scanner.py`, uncomment:
```python
# opportunity_data = OpportunityData(
#     opportunities=all_opportunities,
#     timestamp=datetime.now(timezone.utc)
# )
# await ctx.send(config.STRATEGY_ADDRESS, opportunity_data)
```

And in `agents/strategy_engine.py`, define handler:
```python
@strategy_engine.on_message(model=OpportunityData)
async def handle_opportunities(ctx: Context, sender: str, msg: OpportunityData):
    ctx.logger.info(f"Received {len(msg.opportunities)} opportunities from {sender}")
    # Process opportunities...
```

---

## Resources

- [uAgents Documentation](https://uagents.fetch.ai/docs)
- [Local Agents Guide](https://uagents.fetch.ai/docs/guides/run_local_agents)
- [Agent Types](https://uagents.fetch.ai/docs/guides/types)
- [Agent Inspector](https://agentverse.ai/inspect)

---

## Quick Reference Commands

```bash
# Get agent addresses
python get_agent_addresses.py

# Run individual agent
python agents/chain_scanner.py

# Run all agents
./run_all_agents.sh

# Test local communication
python test_local_interaction.py
```
