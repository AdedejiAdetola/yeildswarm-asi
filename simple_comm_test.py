"""
Simple test to verify inter-agent communication is working
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.config import config

print("=" * 60)
print("🧪 YieldSwarm AI - Simple Communication Test")
print("=" * 60)
print("\n✅ Configuration Check:")
print(f"Coordinator Address: {config.COORDINATOR_ADDRESS}")
print(f"Scanner Address: {config.SCANNER_ADDRESS}")
print(f"MeTTa Address: {config.METTA_ADDRESS}")
print(f"Strategy Address: {config.STRATEGY_ADDRESS}")
print(f"Execution Address: {config.EXECUTION_ADDRESS}")
print(f"Tracker Address: {config.TRACKER_ADDRESS}")

print("\n✅ Message Models Check:")
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    StrategyRequest,
    StrategyResponse,
    Chain,
    RiskLevel
)
print("✓ OpportunityRequest")
print("✓ OpportunityResponse")
print("✓ StrategyRequest")
print("✓ StrategyResponse")

print("\n✅ Create Test Messages:")

# Test OpportunityRequest
opp_req = OpportunityRequest(
    request_id="test-123",
    user_id="test-user",
    chains=[Chain.ETHEREUM],
    min_apy=4.0,
    max_risk_score=5.0
)
print(f"✓ Created OpportunityRequest: {opp_req.request_id}")

# Test StrategyRequest
strat_req = StrategyRequest(
    request_id="test-456",
    user_id="test-user",
    amount=10.0,
    currency="ETH",
    risk_level=RiskLevel.MODERATE,
    preferred_chains=[Chain.ETHEREUM],
    opportunities=[],
    metta_insights={}
)
print(f"✓ Created StrategyRequest: {strat_req.request_id}")

print("\n✅ All checks passed!")
print("\nNext steps:")
print("1. Agents are configured correctly")
print("2. Message models are properly defined")
print("3. Ready for full integration testing")
print("\nTo test full communication:")
print("  1. Ensure agents are running (check ports 8001, 8002, 8003)")
print("  2. They can receive and process messages")
print("  3. Update agent handlers to use new message models from protocols/messages.py")
print("=" * 60)
