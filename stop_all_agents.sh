#!/bin/bash

# YieldSwarm AI - Stop All Agents

echo "============================================================"
echo "🛑 YieldSwarm AI - Stopping All Agents"
echo "============================================================"

# Stop all agent processes
pkill -f "chain_scanner_clean.py" && echo "✅ Stopped Scanner Agent" || echo "  Scanner not running"
pkill -f "portfolio_coordinator_clean.py" && echo "✅ Stopped Coordinator Agent" || echo "  Coordinator not running"
pkill -f "metta_knowledge_clean.py" && echo "✅ Stopped MeTTa Agent" || echo "  MeTTa not running"
pkill -f "strategy_engine_clean.py" && echo "✅ Stopped Strategy Agent" || echo "  Strategy not running"
pkill -f "execution_agent_clean.py" && echo "✅ Stopped Execution Agent" || echo "  Execution not running"
pkill -f "performance_tracker_clean.py" && echo "✅ Stopped Tracker Agent" || echo "  Tracker not running"

echo ""
echo "============================================================"
echo "✅ All agents stopped"
echo "============================================================"
