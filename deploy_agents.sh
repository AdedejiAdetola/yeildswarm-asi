#!/bin/bash
# YieldSwarm AI - Deploy All 6 Agents with Mailbox Mode
# This script runs all agents in the background with proper logging

set -e

echo "============================================================"
echo "YieldSwarm AI - Agent Deployment (Mailbox Mode)"
echo "============================================================"
echo ""

# Create logs directory
mkdir -p logs

# Stop any existing agents
echo "🛑 Stopping any existing agents..."
pkill -f "python agents/" 2>/dev/null || true
sleep 2

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "🚀 Starting all 6 agents..."
echo ""

# Start each agent in background
echo "1️⃣  Starting Portfolio Coordinator (Port 8000)..."
nohup python agents/portfolio_coordinator.py > logs/coordinator.log 2>&1 &
COORDINATOR_PID=$!
sleep 2

echo "2️⃣  Starting Chain Scanner (Port 8001)..."
nohup python agents/chain_scanner.py > logs/scanner.log 2>&1 &
SCANNER_PID=$!
sleep 2

echo "3️⃣  Starting MeTTa Knowledge (Port 8002)..."
nohup python agents/metta_knowledge.py > logs/metta.log 2>&1 &
METTA_PID=$!
sleep 2

echo "4️⃣  Starting Strategy Engine (Port 8003)..."
nohup python agents/strategy_engine.py > logs/strategy.log 2>&1 &
STRATEGY_PID=$!
sleep 2

echo "5️⃣  Starting Execution Agent (Port 8004)..."
nohup python agents/execution_agent.py > logs/execution.log 2>&1 &
EXECUTION_PID=$!
sleep 2

echo "6️⃣  Starting Performance Tracker (Port 8005)..."
nohup python agents/performance_tracker.py > logs/tracker.log 2>&1 &
TRACKER_PID=$!
sleep 2

echo ""
echo "⏳ Waiting for agents to initialize..."
sleep 5

# Check if agents are running
echo ""
echo "📊 Checking agent status..."
echo ""

RUNNING_COUNT=0

if ps -p $COORDINATOR_PID > /dev/null 2>&1; then
    echo "✅ Portfolio Coordinator (PID: $COORDINATOR_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ Portfolio Coordinator - Failed to start"
fi

if ps -p $SCANNER_PID > /dev/null 2>&1; then
    echo "✅ Chain Scanner (PID: $SCANNER_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ Chain Scanner - Failed to start"
fi

if ps -p $METTA_PID > /dev/null 2>&1; then
    echo "✅ MeTTa Knowledge (PID: $METTA_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ MeTTa Knowledge - Failed to start"
fi

if ps -p $STRATEGY_PID > /dev/null 2>&1; then
    echo "✅ Strategy Engine (PID: $STRATEGY_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ Strategy Engine - Failed to start"
fi

if ps -p $EXECUTION_PID > /dev/null 2>&1; then
    echo "✅ Execution Agent (PID: $EXECUTION_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ Execution Agent - Failed to start"
fi

if ps -p $TRACKER_PID > /dev/null 2>&1; then
    echo "✅ Performance Tracker (PID: $TRACKER_PID) - Running"
    ((RUNNING_COUNT++))
else
    echo "❌ Performance Tracker - Failed to start"
fi

echo ""
echo "============================================================"
echo "Deployment Summary: $RUNNING_COUNT/6 agents running"
echo "============================================================"
echo ""

if [ $RUNNING_COUNT -eq 6 ]; then
    echo "🎉 SUCCESS! All agents deployed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Check logs in ./logs/ directory"
    echo "2. Verify agents on Agentverse: https://agentverse.ai/agents"
    echo "3. Test on ASI:One: https://asi1.ai"
    echo ""
    echo "📝 Useful Commands:"
    echo "  View coordinator logs: tail -f logs/coordinator.log"
    echo "  View all logs: tail -f logs/*.log"
    echo "  Check agent processes: ps aux | grep 'python agents'"
    echo "  Stop all agents: pkill -f 'python agents/'"
    echo ""
else
    echo "⚠️  WARNING: Not all agents started successfully"
    echo ""
    echo "Check logs for errors:"
    echo "  ls -lh logs/"
    echo "  cat logs/*.log"
    echo ""
fi

echo "Agent PIDs saved to: logs/agent_pids.txt"
echo "$COORDINATOR_PID $SCANNER_PID $METTA_PID $STRATEGY_PID $EXECUTION_PID $TRACKER_PID" > logs/agent_pids.txt
