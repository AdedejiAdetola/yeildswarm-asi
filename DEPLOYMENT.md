# YieldSwarm AI - Deployment Guide

## Prerequisites

- Python 3.10 or higher
- Agentverse account (https://agentverse.ai)
- Git

## Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd yieldswarm-asi
```

### 2. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

Required environment variables:
- `AGENTVERSE_API_KEY`: Your Agentverse API key (get from https://agentverse.ai/profile/api-keys)

Optional environment variables:
- `COORDINATOR_MAILBOX_KEY`: Mailbox key for coordinator (auto-generated if not set)
- `SCANNER_MAILBOX_KEY`: Mailbox key for scanner
- `METTA_MAILBOX_KEY`: Mailbox key for MeTTa agent
- `STRATEGY_MAILBOX_KEY`: Mailbox key for strategy agent
- `EXECUTION_MAILBOX_KEY`: Mailbox key for execution agent
- `TRACKER_MAILBOX_KEY`: Mailbox key for tracker agent

### 4. Test Locally (Optional)

Start all agents locally for testing:
```bash
./start_agents.sh
```

Check agent status:
```bash
# View logs
tail -f logs/coordinator.log
tail -f logs/chain-scanner.log
tail -f logs/metta-knowledge.log
tail -f logs/strategy-engine.log
```

Stop agents:
```bash
./stop_agents.sh
```

### 5. Deploy to Agentverse

#### Option A: Using Agentverse Dashboard (Recommended)

1. Go to https://agentverse.ai
2. Sign in with your account
3. Navigate to "My Agents"
4. Click "Create New Agent"
5. For each agent:
   - Upload the agent file (e.g., `agents/portfolio_coordinator.py`)
   - Enable mailbox (for coordinator only)
   - Configure port (8000 for coordinator, 8001-8005 for others)
   - Click "Deploy"
6. Copy the agent addresses and update README.md

#### Option B: Using CLI (Advanced)

```bash
# Deploy coordinator
python agents/portfolio_coordinator.py &

# Wait for deployment to complete, then copy the agent address

# Deploy other agents
python agents/chain_scanner.py &
python agents/metta_knowledge.py &
python agents/strategy_engine.py &
python agents/execution_agent.py &
python agents/performance_tracker.py &
```

### 6. Update README with Agent Addresses

After deployment, update README.md with your actual agent addresses:

```markdown
| Agent | Address | Port |
|-------|---------|------|
| Portfolio Coordinator | agent1q... | 8000 |
| Chain Scanner | agent1q... | 8001 |
| MeTTa Knowledge | agent1q... | 8002 |
| Strategy Engine | agent1q... | 8003 |
| Execution Agent | agent1q... | 8004 |
| Performance Tracker | agent1q... | 8005 |
```

### 7. Test via ASI:One

1. Go to https://agentverse.ai
2. Find your "yieldswarm-coordinator" agent
3. Click the "Chat" button
4. Send test message: "Invest 10 ETH with moderate risk"
5. Verify you receive a strategy response

## Architecture

```
User (ASI:One)
    ↓
Portfolio Coordinator (Chat Protocol enabled)
    ↓
    ├── Chain Scanner → Scans DeFi opportunities
    ├── MeTTa Knowledge → AI reasoning with symbolic logic
    ├── Strategy Engine → Generates optimal allocation
    ├── Execution Agent → Simulates transactions
    └── Performance Tracker → Tracks performance metrics
```

## Agent Communication Flow

1. **User Request** → Portfolio Coordinator (via Chat Protocol)
2. **Coordinator** → Chain Scanner: "Find opportunities"
3. **Chain Scanner** → Coordinator: Returns opportunities
4. **Coordinator** → MeTTa Knowledge: "Analyze these opportunities"
5. **MeTTa** → Coordinator: Returns recommendations
6. **Coordinator** → Strategy Engine: "Create allocation strategy"
7. **Strategy Engine** → Coordinator: Returns strategy
8. **Coordinator** → User: Formatted strategy response

## Troubleshooting

### Issue: Agents not communicating

**Solution:** Verify agent addresses in `utils/config.py` match deployed addresses

```bash
# Check agent addresses
python -c "from utils.config import config; print(f'Coordinator: {config.COORDINATOR_ADDRESS}')"
```

### Issue: Mailbox not working

**Solution:** Ensure mailbox is enabled in Agentverse dashboard for coordinator

### Issue: MeTTa knowledge base not loading

**Solution:** Verify `metta_kb/defi_protocols.metta` exists and has proper syntax

```bash
# Test MeTTa engine
python utils/metta_engine.py
```

### Issue: Import errors

**Solution:** Ensure all dependencies installed

```bash
pip install -r requirements.txt --upgrade
```

## Monitoring

### View Agent Logs
```bash
# Live tail
tail -f logs/coordinator.log

# Search for errors
grep ERROR logs/*.log

# View agent status
ps aux | grep python
```

### Check Agent Health
```bash
# Verify agents are running
curl http://localhost:8000/status  # Coordinator
curl http://localhost:8001/status  # Scanner
curl http://localhost:8002/status  # MeTTa
```

## Production Deployment

For production deployment:

1. Use production RPC endpoints (update `.env`)
2. Enable proper monitoring and alerting
3. Set up log rotation
4. Configure firewall rules
5. Use HTTPS endpoints
6. Implement rate limiting
7. Set up backup mechanisms

## Support

For issues or questions:
- GitHub Issues: [Your repo URL]/issues
- Documentation: https://docs.fetch.ai
- Discord: https://discord.gg/fetchai

## License

[Your License]
