#!/bin/bash
# YieldSwarm AI - Run All Agents
# This script helps you run all 6 agents in separate terminals

echo "============================================================"
echo "YieldSwarm AI - Multi-Agent Launcher"
echo "============================================================"
echo ""
echo "This will open 6 terminal windows, each running one agent."
echo ""
echo "Agents:"
echo "  1. Portfolio Coordinator (Port 8000) - ASI:One compatible"
echo "  2. Chain Scanner (Port 8001) - Multi-chain monitoring"
echo "  3. MeTTa Knowledge (Port 8002) - DeFi intelligence"
echo "  4. Strategy Engine (Port 8003) - Optimization"
echo "  5. Execution Agent (Port 8004) - Transaction handling"
echo "  6. Performance Tracker (Port 8005) - Analytics"
echo ""
echo "Press ENTER to continue..."
read

# Check if gnome-terminal is available (Ubuntu/Debian)
if command -v gnome-terminal &> /dev/null; then
    TERMINAL="gnome-terminal"
elif command -v xterm &> /dev/null; then
    TERMINAL="xterm"
elif command -v konsole &> /dev/null; then
    TERMINAL="konsole"
else
    echo "❌ No supported terminal emulator found."
    echo "Please run each agent manually in separate terminals:"
    echo ""
    echo "Terminal 1: python3 agents/portfolio_coordinator.py"
    echo "Terminal 2: python3 agents/chain_scanner.py"
    echo "Terminal 3: python3 agents/metta_knowledge.py"
    echo "Terminal 4: python3 agents/strategy_engine.py"
    echo "Terminal 5: python3 agents/execution_agent.py"
    echo "Terminal 6: python3 agents/performance_tracker.py"
    exit 1
fi

echo "🚀 Launching agents..."

# Launch each agent in a new terminal
$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/portfolio_coordinator.py; exec bash" &
sleep 1

$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/chain_scanner.py; exec bash" &
sleep 1

$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/metta_knowledge.py; exec bash" &
sleep 1

$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/strategy_engine.py; exec bash" &
sleep 1

$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/execution_agent.py; exec bash" &
sleep 1

$TERMINAL -- bash -c "source venv/bin/activate; python3 agents/performance_tracker.py; exec bash" &

echo ""
echo "✅ All agents launched!"
echo ""
echo "Check each terminal window to verify agents are running."
echo "Look for 'Starting agent...' messages."
echo ""
echo "To stop all agents: Close each terminal window or press CTRL+C in each."
echo ""
echo "============================================================"
