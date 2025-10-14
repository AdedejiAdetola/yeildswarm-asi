"""
YieldSwarm AI - Agent Communication Test
Tests the full agent orchestration flow
"""

import asyncio
from datetime import datetime, timezone
from uuid import uuid4
from uagents import Agent, Context
from protocols.messages import (
    OpportunityRequest,
    Chain
)
from utils.config import config

# Create a test client agent
test_client = Agent(
    name="test_client",
    seed="test-client-seed-12345",
    port=9000,
    endpoint=["http://0.0.0.0:9000/submit"]
)


@test_client.on_event("startup")
async def startup(ctx: Context):
    """Send test request to coordinator on startup"""
    print("\n" + "=" * 60)
    print("🧪 Test Client Starting")
    print("=" * 60)
    print(f"Test Client Address: {ctx.agent.address}")
    print(f"Coordinator Address: {config.COORDINATOR_ADDRESS}")
    print("=" * 60)

    # Wait for startup
    await asyncio.sleep(3)

    print("\n📤 Sending test OpportunityRequest to Scanner...")

    # Create test request
    request = OpportunityRequest(
        request_id=str(uuid4()),
        chains=[Chain.ETHEREUM, Chain.SOLANA, Chain.BSC],
        min_apy=3.0,
        max_risk_score=7.0
    )

    print(f"   Request ID: {request.request_id}")
    print(f"   Chains: {[c.value for c in request.chains]}")
    print(f"   Min APY: {request.min_apy}%")
    print(f"   Max Risk: {request.max_risk_score}/10")

    # Send to Scanner
    scanner_address = config.SCANNER_ADDRESS
    await ctx.send(scanner_address, request)

    print(f"✅ Request sent to Scanner: {scanner_address}")
    print(f"\nCheck logs/scanner.log and logs/coordinator.log to see the response!")
    print("\nTo monitor logs:")
    print("  tail -f logs/scanner.log")
    print("  tail -f logs/coordinator.log")
    print("=" * 60)


async def test_direct_message():
    """
    Alternative: Direct test via Python
    This demonstrates how to programmatically test agent communication
    """
    print("\n" + "=" * 60)
    print("🧪 Direct Message Test")
    print("=" * 60)

    # Import the scanner and coordinator for direct testing
    from agents.chain_scanner_clean import scanner_agent
    from agents.portfolio_coordinator_clean import coordinator_agent

    print("✅ Agents imported successfully")
    print(f"   Scanner: {scanner_agent.address}")
    print(f"   Coordinator: {coordinator_agent.address}")
    print("=" * 60)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 YieldSwarm AI - Agent Flow Test")
    print("=" * 60)
    print("\nThis test will:")
    print("  1. Start a test client agent")
    print("  2. Send OpportunityRequest to Scanner")
    print("  3. Scanner should respond with OpportunityResponse")
    print("  4. Check logs to verify communication")
    print("\nMake sure all agents are running first:")
    print("  ./start_all_agents.sh")
    print("\n" + "=" * 60)

    # Run test client
    test_client.run()
