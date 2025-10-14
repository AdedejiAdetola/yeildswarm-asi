#!/bin/bash

# YieldSwarm AI - Start All Agents
# Starts all 5 agents in the background with proper logging

echo "============================================================"
echo "🚀 YieldSwarm AI - Starting All Agents"
echo "============================================================"

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Kill any existing agents
echo "🛑 Stopping existing agents..."
pkill -f "chain_scanner_clean.py" || true
pkill -f "portfolio_coordinator_clean.py" || true
pkill -f "metta_knowledge_clean.py" || true
pkill -f "strategy_engine_clean.py" || true
pkill -f "execution_agent_clean.py" || true
pkill -f "performance_tracker_clean.py" || true

sleep 2

# Start Scanner Agent (port 8001)
echo ""
echo "📡 Starting Chain Scanner Agent (port 8001)..."
nohup python agents/chain_scanner_clean.py > logs/scanner.log 2>&1 &
SCANNER_PID=$!
echo "   PID: $SCANNER_PID"
sleep 3

# Start Coordinator Agent (port 8000)
echo ""
echo "🎯 Starting Portfolio Coordinator Agent (port 8000)..."
nohup python agents/portfolio_coordinator_clean.py > logs/coordinator.log 2>&1 &
COORDINATOR_PID=$!
echo "   PID: $COORDINATOR_PID"
sleep 3

# Start MeTTa Knowledge Agent (port 8002)
echo ""
echo "🧠 Starting MeTTa Knowledge Agent (port 8002)..."
nohup python agents/metta_knowledge_clean.py > logs/metta.log 2>&1 &
METTA_PID=$!
echo "   PID: $METTA_PID"
sleep 3

# Start Strategy Engine Agent (port 8003)
echo ""
echo "⚡ Starting Strategy Engine Agent (port 8003)..."
nohup python agents/strategy_engine_clean.py > logs/strategy.log 2>&1 &
STRATEGY_PID=$!
echo "   PID: $STRATEGY_PID"
sleep 3

# Start Execution Agent (port 8004)
echo ""
echo "🚀 Starting Execution Agent (port 8004)..."
nohup python agents/execution_agent_clean.py > logs/execution.log 2>&1 &
EXECUTION_PID=$!
echo "   PID: $EXECUTION_PID"
sleep 3

# Start Performance Tracker Agent (port 8005)
echo ""
echo "📊 Starting Performance Tracker Agent (port 8005)..."
nohup python agents/performance_tracker_clean.py > logs/tracker.log 2>&1 &
TRACKER_PID=$!
echo "   PID: $TRACKER_PID"
sleep 3

# Check status
echo ""
echo "============================================================"
echo "📊 Agent Status Check"
echo "============================================================"
echo ""

# Check ports
for port in 8000 8001 8002 8003 8004 8005; do
    if lsof -i :$port 2>/dev/null | grep -q LISTEN; then
        echo "✅ Port $port: ACTIVE"
    else
        echo "❌ Port $port: INACTIVE"
    fi
done

echo ""
echo "============================================================"
echo "🎉 Agent System Started!"
echo "============================================================"
echo ""
echo "Agent Endpoints:"
echo "  • Coordinator:   http://0.0.0.0:8000"
echo "  • Scanner:       http://0.0.0.0:8001"
echo "  • MeTTa:         http://0.0.0.0:8002"
echo "  • Strategy:      http://0.0.0.0:8003"
echo "  • Execution:     http://0.0.0.0:8004"
echo "  • Tracker:       http://0.0.0.0:8005"
echo ""
echo "Logs available in: ./logs/"
echo ""
echo "To stop all agents:"
echo "  ./stop_all_agents.sh"
echo ""
echo "To view logs:"
echo "  tail -f logs/coordinator.log"
echo "  tail -f logs/scanner.log"
echo "  tail -f logs/metta.log"
echo "  tail -f logs/strategy.log"
echo "  tail -f logs/execution.log"
echo "  tail -f logs/tracker.log"
echo ""
echo "============================================================"
