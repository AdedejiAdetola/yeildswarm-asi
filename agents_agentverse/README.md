# YieldSwarm AI - Agentverse Deployment Files

## 🚀 Deployment Order

Deploy agents in this order:

1. **Chain Scanner** (`1_chain_scanner.py`)
2. **MeTTa Knowledge** (`2_metta_knowledge.py`)
3. **Strategy Engine** (`3_strategy_engine.py`)
4. **Execution Agent** (`4_execution_agent.py`) - Optional for demo
5. **Performance Tracker** (`5_performance_tracker.py`) - Optional for demo
6. **Portfolio Coordinator** (`0_COORDINATOR.py`) - DEPLOY LAST!

## 📝 Deployment Instructions

### For Each Agent:

1. Go to https://agentverse.ai
2. Click "Create New Agent"
3. In the code editor, **delete all existing code**
4. **Copy the entire content** of the agent file
5. **Paste** into the Agentverse editor
6. Click **"Save"** or **"Deploy"**
7. Wait for "Successfully started agent" in logs
8. **Copy the agent address** from the logs

### Example Agent Addresses to Save:

```
Chain Scanner:       agent1qtn2hgpdfl0he2h88xncvrdvyk5vd9xtsruw9vzua8tgnejtxxpzy8suu8r
MeTTa Knowledge:     agent1q... (copy from logs)
Strategy Engine:     agent1q... (copy from logs)
Execution Agent:     agent1q... (copy from logs) - Optional
Performance Tracker: agent1q... (copy from logs) - Optional
Coordinator:         agent1q... (copy from logs)
```

**Note:** Execution and Performance Tracker are optional for the basic demo. The core flow only requires Chain Scanner → MeTTa → Strategy → Coordinator.

## ⚠️ IMPORTANT: Update Coordinator

Before deploying the **Coordinator** (`0_COORDINATOR.py`):

1. Open `0_COORDINATOR.py`
2. Find this section (around line 120):

```python
# TODO: REPLACE THESE WITH YOUR ACTUAL DEPLOYED AGENT ADDRESSES!
SCANNER_ADDRESS = "agent1qtn2hgpdfl0he2h88xncvrdvyk5vd9xtsruw9vzua8tgnejtxxpzy8suu8r"
METTA_ADDRESS = "agent1q0nwxnu6dhws86gxqd7sv5ywv57nnsncfhxcgnxkxkh5mshgze9kuvztx0t"
STRATEGY_ADDRESS = "agent1q0v38te45h3ns2nas9pluajdzguww6t99t37x9lp7an5e3pcckpxkgreypz"
```

3. **Replace** with your actual deployed agent addresses
4. **Save** and deploy

## ✅ Testing

After deploying the Coordinator:

1. Go to https://agentverse.ai
2. Find your "yieldswarm-coordinator" agent
3. Click **"Chat"** button
4. Send test message: **"Invest 10 ETH with moderate risk"**
5. Wait for response with portfolio strategy

## 📊 Expected Flow

```
User (ASI:One)
    ↓
Portfolio Coordinator
    ↓
Chain Scanner → finds opportunities
    ↓
MeTTa Knowledge → analyzes & recommends
    ↓
Strategy Engine → creates allocation
    ↓
Portfolio Coordinator → formats response
    ↓
User (receives strategy)
```

## 🐛 Troubleshooting

### Agent won't start:
- Check logs for errors
- Ensure no `__file__` references
- Verify all imports are standard libraries

### Coordinator not responding:
- Verify agent addresses are correct
- Check that other agents are running
- Look at coordinator logs for message flow

### Messages not being received:
- Ensure mailbox is enabled
- Verify agent addresses are correct
- Check Almanac registration status

## 📁 Files in This Directory

- `1_chain_scanner.py` - Chain Scanner (deploy first)
- `2_metta_knowledge.py` - MeTTa Knowledge Agent
- `3_strategy_engine.py` - Strategy Engine
- `4_execution_agent.py` - Execution Agent (optional)
- `5_performance_tracker.py` - Performance Tracker (optional)
- `0_COORDINATOR.py` - Portfolio Coordinator (deploy LAST)
- `README.md` - This file
- `DEPLOYMENT_SUMMARY.md` - Detailed instructions

## 🎯 Success Criteria

✅ All agents show "Successfully started agent"
✅ All agents registered on Almanac
✅ Coordinator receives test message
✅ Full agent chain executes
✅ User receives formatted strategy response

---

**Need help?** Check the main project README or Agentverse documentation.
