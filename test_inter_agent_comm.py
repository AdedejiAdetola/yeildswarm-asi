"""
Test script for inter-agent communication
Tests message flow: Coordinator -> Scanner -> Strategy Engine
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from uagents import Agent, Context
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    StrategyRequest,
    Chain
)
from utils.models import InvestmentRequest, RiskLevel
from utils.config import config
from datetime import datetime, timezone
from uuid import uuid4


# Create a test agent to simulate the coordinator
test_agent = Agent(
    name="test-coordinator",
    seed="test-seed-123",
    port=9000
)


@test_agent.on_event("startup")
async def test_startup(ctx: Context):
    """Test inter-agent communication on startup"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🧪 TESTING INTER-AGENT COMMUNICATION")
    ctx.logger.info("=" * 60)

    # Wait a moment for agents to be ready
    await asyncio.sleep(2)

    ctx.logger.info("\n📋 Test 1: Coordinator -> Scanner")
    ctx.logger.info("-" * 60)

    # Create test opportunity request
    request_id = str(uuid4())
    opp_request = OpportunityRequest(
        request_id=request_id,
        user_id="test-user-123",
        chains=[Chain.ETHEREUM, Chain.POLYGON],
        min_apy=4.0,
        max_risk_score=5.0
    )

    ctx.logger.info(f"📤 Sending OpportunityRequest to Scanner...")
    ctx.logger.info(f"   Request ID: {request_id}")
    ctx.logger.info(f"   Chains: {[c.value for c in opp_request.chains]}")
    ctx.logger.info(f"   Min APY: {opp_request.min_apy}%")
    ctx.logger.info(f"   Max Risk: {opp_request.max_risk_score}")

    try:
        await ctx.send(config.SCANNER_ADDRESS, opp_request)
        ctx.logger.info("✅ Message sent successfully!")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send message: {str(e)}")

    ctx.logger.info("\n" + "=" * 60)
    ctx.logger.info("Test complete! Check Scanner agent logs for response.")
    ctx.logger.info("=" * 60)


# Handle response from Scanner
@test_agent.on_message(model=OpportunityResponse)
async def handle_opportunities(ctx: Context, sender: str, msg: OpportunityResponse):
    """Handle opportunity response from Scanner"""
    ctx.logger.info("\n" + "=" * 60)
    ctx.logger.info("📥 RECEIVED RESPONSE FROM SCANNER")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Request ID: {msg.request_id}")
    ctx.logger.info(f"Opportunities: {len(msg.opportunities)}")
    ctx.logger.info(f"Chains Scanned: {[c.value for c in msg.chains_scanned]}")

    if msg.opportunities:
        ctx.logger.info("\nTop 3 Opportunities:")
        for i, opp in enumerate(msg.opportunities[:3], 1):
            ctx.logger.info(f"{i}. {opp.protocol} on {opp.chain.value}")
            ctx.logger.info(f"   APY: {opp.apy}%, Risk: {opp.risk_score}, TVL: ${opp.tvl:,}")

        # Now test Strategy Engine
        ctx.logger.info("\n📋 Test 2: Coordinator -> Strategy Engine")
        ctx.logger.info("-" * 60)

        # Create test investment request
        investment_req = InvestmentRequest(
            user_id="test-user-123",
            amount=10.0,
            currency="ETH",
            risk_level=RiskLevel.MODERATE,
            preferred_chains=[Chain.ETHEREUM, Chain.POLYGON]
        )

        strategy_req = StrategyRequest(
            request_id=str(uuid4()),
            investment_request=investment_req,
            opportunities=msg.opportunities,
            metta_knowledge={}
        )

        ctx.logger.info(f"📤 Sending StrategyRequest to Strategy Engine...")
        ctx.logger.info(f"   Amount: {investment_req.amount} {investment_req.currency}")
        ctx.logger.info(f"   Risk Level: {investment_req.risk_level.value}")
        ctx.logger.info(f"   Opportunities: {len(msg.opportunities)}")

        try:
            await ctx.send(config.STRATEGY_ADDRESS, strategy_req)
            ctx.logger.info("✅ Message sent successfully!")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send message: {str(e)}")

    else:
        ctx.logger.warning("⚠️  No opportunities received")


# Handle strategy response
from utils.models import Strategy

@test_agent.on_message(model=Strategy)
async def handle_strategy(ctx: Context, sender: str, msg: Strategy):
    """Handle strategy response from Strategy Engine"""
    ctx.logger.info("\n" + "=" * 60)
    ctx.logger.info("📥 RECEIVED STRATEGY FROM STRATEGY ENGINE")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Strategy ID: {msg.strategy_id}")
    ctx.logger.info(f"User ID: {msg.user_id}")
    ctx.logger.info(f"Total Amount: {msg.total_amount}")
    ctx.logger.info(f"Actions: {len(msg.actions)}")
    ctx.logger.info(f"Expected APY: {msg.expected_apy}%")
    ctx.logger.info(f"Risk Score: {msg.risk_score}")
    ctx.logger.info("\n✅ INTER-AGENT COMMUNICATION TEST SUCCESSFUL!")
    ctx.logger.info("=" * 60)


if __name__ == "__main__":
    print("\n🧪 YieldSwarm AI - Inter-Agent Communication Test")
    print("=" * 60)
    print("\nThis script will test the following message flows:")
    print("1. Test Agent -> Chain Scanner (OpportunityRequest)")
    print("2. Chain Scanner -> Test Agent (OpportunityResponse)")
    print("3. Test Agent -> Strategy Engine (StrategyRequest)")
    print("\nMake sure the following agents are running:")
    print("  - agents/chain_scanner.py (port 8001)")
    print("  - agents/strategy_engine.py (port 8003)")
    print("\nStarting test...\n")

    test_agent.run()
