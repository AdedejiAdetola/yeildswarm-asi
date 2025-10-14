"""
YieldSwarm AI - Chain Scanner Agent (Pure uAgents)
Scans multiple blockchains for DeFi yield opportunities

Following official patterns from winning projects:
- TravelBud: Pure agent-to-agent messaging
- AgentFlow: Clean message handlers with datetime.now(timezone.utc)
- FinWell: mailbox=True for Agentverse compatibility
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from datetime import datetime, timezone
from typing import List
import random

# Import Pydantic message models
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    Opportunity,
    Chain
)
from utils.config import config


# ===== AGENT INITIALIZATION =====
# Pattern from FinWell asi1_wrapper_agent.py and AgentFlow intent_classifier_agent.py

scanner = Agent(
    name="yieldswarm-scanner",
    seed=config.SCANNER_SEED,
    port=config.SCANNER_PORT,
    mailbox=True,  # Enable Agentverse (REQUIRED for hackathon)
    endpoint=[f"http://localhost:{config.SCANNER_PORT}/submit"],
)


# ===== MOCK SCANNING FUNCTIONS =====

async def scan_ethereum() -> List[Opportunity]:
    """Scan Ethereum for yield opportunities"""
    return [
        Opportunity(
            protocol="Aave-V3",
            chain=Chain.ETHEREUM,
            apy=round(random.uniform(3.5, 5.5), 2),
            tvl=5_000_000_000,
            risk_score=2.0,
            pool_address="0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
        ),
        Opportunity(
            protocol="Uniswap-V3",
            chain=Chain.ETHEREUM,
            apy=round(random.uniform(8.0, 15.0), 2),
            tvl=3_200_000_000,
            risk_score=3.5,
            token_pair="ETH-USDC",
            pool_address="0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
        ),
        Opportunity(
            protocol="Curve",
            chain=Chain.ETHEREUM,
            apy=round(random.uniform(4.0, 7.0), 2),
            tvl=2_800_000_000,
            risk_score=2.5,
            token_pair="stETH-ETH"
        ),
    ]


async def scan_solana() -> List[Opportunity]:
    """Scan Solana for yield opportunities"""
    return [
        Opportunity(
            protocol="Raydium",
            chain=Chain.SOLANA,
            apy=round(random.uniform(15.0, 25.0), 2),
            tvl=450_000_000,
            risk_score=6.0,
            token_pair="SOL-USDC"
        ),
        Opportunity(
            protocol="Solend",
            chain=Chain.SOLANA,
            apy=round(random.uniform(6.0, 12.0), 2),
            tvl=280_000_000,
            risk_score=4.5
        ),
    ]


async def scan_bsc() -> List[Opportunity]:
    """Scan BSC for yield opportunities"""
    return [
        Opportunity(
            protocol="PancakeSwap",
            chain=Chain.BSC,
            apy=round(random.uniform(10.0, 20.0), 2),
            tvl=1_200_000_000,
            risk_score=5.0,
            token_pair="BNB-BUSD"
        ),
        Opportunity(
            protocol="Venus",
            chain=Chain.BSC,
            apy=round(random.uniform(5.0, 9.0), 2),
            tvl=680_000_000,
            risk_score=4.0
        ),
    ]


async def scan_polygon() -> List[Opportunity]:
    """Scan Polygon for yield opportunities"""
    return [
        Opportunity(
            protocol="Aave-V3",
            chain=Chain.POLYGON,
            apy=round(random.uniform(4.0, 6.5), 2),
            tvl=620_000_000,
            risk_score=2.5
        ),
        Opportunity(
            protocol="QuickSwap",
            chain=Chain.POLYGON,
            apy=round(random.uniform(7.0, 13.0), 2),
            tvl=380_000_000,
            risk_score=4.0,
            token_pair="MATIC-USDC"
        ),
    ]


async def scan_arbitrum() -> List[Opportunity]:
    """Scan Arbitrum for yield opportunities"""
    return [
        Opportunity(
            protocol="Aave-V3",
            chain=Chain.ARBITRUM,
            apy=round(random.uniform(3.8, 5.8), 2),
            tvl=540_000_000,
            risk_score=2.3
        ),
        Opportunity(
            protocol="GMX",
            chain=Chain.ARBITRUM,
            apy=round(random.uniform(12.0, 18.0), 2),
            tvl=420_000_000,
            risk_score=5.5,
            token_pair="GLP"
        ),
    ]


# ===== MESSAGE HANDLER =====
# Pattern from AgentFlow: @agent.on_message(model=MessageModel)

@scanner.on_message(model=OpportunityRequest)
async def handle_opportunity_request(ctx: Context, sender: str, msg: OpportunityRequest):
    """
    Handle opportunity scanning request from Portfolio Coordinator

    Pattern from winning projects:
    - AgentFlow: Clean message handler with logging
    - TravelBud: Async processing and response
    - FinWell: Simple request-response pattern
    """
    ctx.logger.info(f"📩 Received scan request {msg.request_id} from {sender}")
    ctx.logger.info(f"   Chains: {[c.value for c in msg.chains]}")
    ctx.logger.info(f"   Min APY: {msg.min_apy}%, Max Risk: {msg.max_risk_score}")

    try:
        # Scan requested chains
        all_opportunities = []

        if Chain.ETHEREUM in msg.chains:
            eth_ops = await scan_ethereum()
            all_opportunities.extend(eth_ops)
            ctx.logger.info(f"   ✓ Scanned Ethereum: {len(eth_ops)} opportunities")

        if Chain.SOLANA in msg.chains:
            sol_ops = await scan_solana()
            all_opportunities.extend(sol_ops)
            ctx.logger.info(f"   ✓ Scanned Solana: {len(sol_ops)} opportunities")

        if Chain.BSC in msg.chains:
            bsc_ops = await scan_bsc()
            all_opportunities.extend(bsc_ops)
            ctx.logger.info(f"   ✓ Scanned BSC: {len(bsc_ops)} opportunities")

        if Chain.POLYGON in msg.chains:
            poly_ops = await scan_polygon()
            all_opportunities.extend(poly_ops)
            ctx.logger.info(f"   ✓ Scanned Polygon: {len(poly_ops)} opportunities")

        if Chain.ARBITRUM in msg.chains:
            arb_ops = await scan_arbitrum()
            all_opportunities.extend(arb_ops)
            ctx.logger.info(f"   ✓ Scanned Arbitrum: {len(arb_ops)} opportunities")

        # Filter by criteria
        filtered_opportunities = [
            opp for opp in all_opportunities
            if opp.apy >= msg.min_apy and opp.risk_score <= msg.max_risk_score
        ]

        # Sort by APY (highest first)
        filtered_opportunities.sort(key=lambda x: x.apy, reverse=True)

        ctx.logger.info(f"✅ Found {len(filtered_opportunities)} opportunities matching criteria")

        # Send response back to coordinator
        # Pattern from AgentFlow: datetime.now(timezone.utc) for timestamps
        response = OpportunityResponse(
            request_id=msg.request_id,
            opportunities=filtered_opportunities,
            timestamp=datetime.now(timezone.utc).isoformat(),
            chains_scanned=msg.chains
        )

        await ctx.send(sender, response)
        ctx.logger.info(f"📤 Sent {len(filtered_opportunities)} opportunities to {sender}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing scan request: {str(e)}")
        # Send empty response on error
        error_response = OpportunityResponse(
            request_id=msg.request_id,
            opportunities=[],
            timestamp=datetime.now(timezone.utc).isoformat(),
            chains_scanned=msg.chains
        )
        await ctx.send(sender, error_response)


# ===== STARTUP EVENT HANDLER =====
# Pattern from FinWell: Log agent details on startup

@scanner.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler - runs once when agent starts"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🔍 Chain Scanner Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Name: {scanner.name}")
    ctx.logger.info(f"Agent Address: {scanner.address}")
    ctx.logger.info(f"Port: {config.SCANNER_PORT}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Supported Chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    ctx.logger.info(f"Protocols: 10+ DeFi protocols")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive opportunity scan requests")
    ctx.logger.info(f"👀 Listening for messages from Coordinator: {config.COORDINATOR_ADDRESS}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🐝 YieldSwarm AI - Chain Scanner Agent")
    print("=" * 60)
    print(f"Agent Address: {scanner.address}")
    print(f"Port: {config.SCANNER_PORT}")
    print(f"Mailbox: Enabled (Agentverse Ready)")
    print(f"Chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting pure uAgents mode...\n")

    # Run the agent (this blocks)
    scanner.run()
