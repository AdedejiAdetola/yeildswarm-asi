#!/bin/bash

# YieldSwarm AI - System Status Checker

echo "============================================================"
echo "🔍 YieldSwarm AI - System Status Check"
echo "============================================================"
echo ""

# Check all ports
echo "📊 Port Status:"
echo ""

declare -A ports=(
    [8000]="Coordinator"
    [8001]="Scanner"
    [8002]="MeTTa"
    [8003]="Strategy"
    [8004]="Execution"
    [8005]="Tracker"
    [8080]="Backend"
    [3000]="Frontend"
)

for port in 8000 8001 8002 8003 8004 8005 8080 3000; do
    name="${ports[$port]}"
    if lsof -i :$port 2>/dev/null | grep -q LISTEN; then
        echo "  ✅ $name (port $port): RUNNING"
    else
        echo "  ❌ $name (port $port): NOT RUNNING"
    fi
done

echo ""
echo "============================================================"
echo "🤖 Agent Processes:"
echo ""

# Check agent processes
if ps aux | grep -E "chain_scanner_clean|portfolio_coordinator_clean|metta_knowledge_clean|strategy_engine_clean|execution_agent_clean|performance_tracker_clean" | grep -v grep > /dev/null; then
    count=$(ps aux | grep -E "chain_scanner_clean|portfolio_coordinator_clean|metta_knowledge_clean|strategy_engine_clean|execution_agent_clean|performance_tracker_clean" | grep -v grep | wc -l)
    echo "  ✅ $count agents running"
else
    echo "  ❌ No agents running"
    echo "     Run: ./start_all_agents.sh"
fi

echo ""
echo "============================================================"
echo "📝 Recent Log Activity:"
echo ""

# Check for recent log activity
if [ -d "logs" ]; then
    echo "  Last 5 log entries from coordinator:"
    tail -5 logs/coordinator.log 2>/dev/null | sed 's/^/    /'
else
    echo "  ⚠️  No logs directory found"
fi

echo ""
echo "============================================================"
echo "🌐 Access Points:"
echo ""
echo "  • Frontend:    http://localhost:3000"
echo "  • Backend:     http://localhost:8080"
echo "  • Coordinator: http://localhost:8000"
echo ""
echo "============================================================"
echo "📚 Useful Commands:"
echo ""
echo "  View agent logs:"
echo "    tail -f logs/coordinator.log"
echo "    tail -f logs/scanner.log"
echo "    tail -f logs/metta.log"
echo ""
echo "  Stop all agents:"
echo "    ./stop_all_agents.sh"
echo ""
echo "  Test HTTP integration:"
echo "    python test_http_chat.py"
echo ""
echo "============================================================"
