# YieldSwarm AI - Setup Guide

## Prerequisites

- Python 3.10+ (3.12 recommended)
- pip or pip3
- Git

## Installation Steps

### 1. Install System Dependencies (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your actual values
```

### 5. Verify Installation

```bash
python3 -c "import uagents; print('uAgents version:', uagents.__version__)"
python3 -c "from hyperon import MeTTa; print('MeTTa imported successfully')"
```

## Quick Start

### Run All Agents Locally

```bash
# Terminal 1 - Portfolio Coordinator
python agents/portfolio_coordinator.py

# Terminal 2 - Chain Scanner
python agents/chain_scanner.py

# Terminal 3 - MeTTa Knowledge
python agents/metta_knowledge.py

# Terminal 4 - Strategy Engine
python agents/strategy_engine.py

# Terminal 5 - Execution Agent
python agents/execution_agent.py

# Terminal 6 - Performance Tracker
python agents/performance_tracker.py
```

### Run Tests

```bash
pytest tests/
```

## Deployment to Agentverse

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

## Troubleshooting

### Issue: `No module named pip`
**Solution**: Install python3-venv and python3-pip as shown in step 1

### Issue: `externally-managed-environment`
**Solution**: Use a virtual environment (step 2)

### Issue: Agent connection errors
**Solution**: Check that all agents are running and mailbox keys are configured

## Next Steps

1. Read [WINNING_PROJECT_PLAN.md](WINNING_PROJECT_PLAN.md) for full architecture
2. Check [README.md](README.md) for agent addresses and usage
3. Watch demo video for walkthrough
