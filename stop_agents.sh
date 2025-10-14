#!/bin/bash
# YieldSwarm AI - Stop All Agents

echo "🛑 Stopping YieldSwarm AI Agents..."
echo "======================================"

# Function to stop an agent
stop_agent() {
    local name=$1
    local pidfile="logs/${name}.pid"

    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping $name (PID: $pid)..."
            kill $pid
            rm "$pidfile"
        else
            echo "$name was not running"
            rm "$pidfile"
        fi
    else
        echo "$name PID file not found"
    fi
}

# Stop all agents
stop_agent "chain-scanner"
stop_agent "metta-knowledge"
stop_agent "strategy-engine"
stop_agent "execution-agent"
stop_agent "performance-tracker"
stop_agent "coordinator"

echo ""
echo "✅ All agents stopped!"
