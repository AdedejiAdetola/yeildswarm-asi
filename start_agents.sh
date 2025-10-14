#!/bin/bash
# YieldSwarm AI - Start All Agents
# Starts all 6 agents for local testing or deployment

echo "🐝 Starting YieldSwarm AI Agents..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Function to start an agent
start_agent() {
    local name=$1
    local port=$2
    local script=$3

    echo "Starting $name on port $port..."
    nohup python $script > logs/${name}.log 2>&1 &
    echo $! > logs/${name}.pid
    sleep 2
}

# Start all agents
start_agent "chain-scanner" 8001 "agents/chain_scanner.py"
start_agent "metta-knowledge" 8002 "agents/metta_knowledge.py"
start_agent "strategy-engine" 8003 "agents/strategy_engine.py"
start_agent "execution-agent" 8004 "agents/execution_agent.py"
start_agent "performance-tracker" 8005 "agents/performance_tracker.py"
start_agent "coordinator" 8000 "agents/portfolio_coordinator.py"

echo ""
echo "✅ All agents started!"
echo ""
echo "📊 Status:"
echo "  • Chain Scanner:        http://localhost:8001"
echo "  • MeTTa Knowledge:      http://localhost:8002"
echo "  • Strategy Engine:      http://localhost:8003"
echo "  • Execution Agent:      http://localhost:8004"
echo "  • Performance Tracker:  http://localhost:8005"
echo "  • Portfolio Coordinator: http://localhost:8000 (ASI:One compatible)"
echo ""
echo "📝 Logs are in ./logs/"
echo ""
echo "To stop all agents, run: ./stop_agents.sh"
