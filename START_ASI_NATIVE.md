# Start YieldSwarm AI (ASI Native)

## Quick Start

### 1. Get Your Agentverse API Key

1. Go to https://agentverse.ai
2. Sign in / Create account
3. Go to Profile → API Keys
4. Create new API key
5. Copy the key

### 2. Set Environment Variable

```bash
# Add to .env file
echo "AGENTVERSE_API_KEY=your_key_here" >> .env
```

OR

```bash
# Export directly
export AGENTVERSE_API_KEY=your_key_here
```

### 3. Start the Coordinator

```bash
source venv/bin/activate
python agents/coordinator_asi_native.py
```

You should see:
```
🐝 YieldSwarm AI - ASI Native Coordinator
✅ Successfully registered with ASI:One!

Agent Details:
  Name: YieldSwarmCoordinator
  Port: 8000
  Address: agent1q...
  Mailbox: Enabled

🌐 Access your agent:
  1. Go to https://agentverse.ai
  2. Find 'YieldSwarmCoordinator' in your agents
  3. Chat directly through ASI:One interface

✨ Your agent is now live and ready!
```

### 4. Test via ASI:One Dashboard

1. Go to https://agentverse.ai
2. Click on "My Agents"
3. Find "YieldSwarmCoordinator"
4. Click "Chat"
5. Send a message like:
   ```
   Invest 15 ETH with moderate risk on Ethereum and Solana
   ```

### 5. You'll Get REAL Responses!

The agent will:
- Parse your request
- Coordinate Scanner, MeTTa, and Strategy agents
- Return a complete portfolio strategy with:
  - Recommended allocations
  - Expected APY
  - Risk scores
  - Explainable reasoning from MeTTa AI

---

## What This Does

The ASI-native coordinator:
1. ✅ Registers with Agentverse using `LangchainRegisterTool`
2. ✅ Uses `AgentManager` for proper lifecycle management
3. ✅ Coordinates all 6 agents internally
4. ✅ Returns responses in `UAgentResponse` format
5. ✅ Works with ASI:One dashboard (no custom frontend needed!)

---

## Architecture

```
User
  ↓
ASI:One Dashboard
  ↓
YieldSwarmCoordinator (agent1q...)
  ├─→ Scanner Agent
  ├─→ MeTTa Knowledge Agent
  ├─→ Strategy Engine Agent
  ├─→ Execution Agent
  └─→ Performance Tracker Agent
```

---

## Troubleshooting

### "AGENTVERSE_API_KEY not found"
- Make sure you've set the environment variable
- Check `.env` file has the key
- Or export it: `export AGENTVERSE_API_KEY=your_key`

### "Error registering with ASI:One"
- Check your API key is valid
- Make sure you have internet connection
- The agent will still run locally even if registration fails

### Agent not appearing in dashboard
- Wait a minute and refresh
- Check the agent logs for errors
- Verify API key is correct

---

## Testing Without Agentverse

You can test locally without Agentverse:

```python
# Test the coordination function directly
import asyncio
from agents.coordinator_asi_native import coordinate_agents

async def test():
    result = await coordinate_agents(
        "Invest 10 ETH with aggressive risk on Ethereum"
    )
    print(json.dumps(result, indent=2))

asyncio.run(test())
```

---

## Next Steps

Once working:
1. Test different risk levels (conservative, moderate, aggressive)
2. Try different chains (Ethereum, Solana, BSC, Polygon, Arbitrum)
3. Vary amounts
4. See how MeTTa reasoning changes with different parameters

---

## Advantages of ASI Native

- ✅ **No custom frontend** - Use ASI:One dashboard
- ✅ **No custom backend** - AgentManager handles everything
- ✅ **Proper ASI integration** - Mailbox, Chat Protocol, etc.
- ✅ **Matches winning projects** - Same pattern as TravelBud
- ✅ **Less code to maintain** - Focus on agent logic
- ✅ **Better ecosystem integration** - Works with all ASI tools

---

**Status:** Ready to run! Just add your AGENTVERSE_API_KEY and start the coordinator.
