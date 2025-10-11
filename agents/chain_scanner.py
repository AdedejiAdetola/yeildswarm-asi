"""
YieldSwarm AI - Chain Scanner Agent
Scans multiple blockchains for DeFi yield opportunities

Follows official uAgents documentation patterns:
- https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- https://innovationlab.fetch.ai/resources/docs/agent-communication/uagent-uagent-communication
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context, Model
from datetime import datetime, timezone
from typing import List
import asyncio
import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import uvicorn

# Import our Pydantic message models (following official doc patterns)
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    Opportunity,
    Chain
)
from utils.config import config


# ===== AGENT INITIALIZATION (Official Pattern) =====
# Following: https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation

scanner = Agent(
    name="yieldswarm-scanner",
    seed=config.SCANNER_SEED,  # Deterministic address generation (REQUIRED)
    port=config.SCANNER_PORT,
    mailbox=True,  # Enable Agentverse mailbox (REQUIRED for hackathon)
    endpoint=[f"http://localhost:{config.SCANNER_PORT}/submit"],  # Best practice
)


# ===== MOCK DATA FUNCTIONS (Phase 4 will replace with real APIs) =====

async def scan_ethereum() -> List[Opportunity]:
    """Scan Ethereum for yield opportunities"""
    opportunities = []

    # Mock Aave V3 data
    opportunities.append(Opportunity(
        protocol="Aave-V3",
        chain=Chain.ETHEREUM,
        apy=round(random.uniform(3.5, 5.5), 2),
        tvl=5_000_000_000,
        risk_score=2.0,
        pool_address="0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"  # Real Aave V3 Pool
    ))

    # Mock Uniswap V3 data
    opportunities.append(Opportunity(
        protocol="Uniswap-V3",
        chain=Chain.ETHEREUM,
        apy=round(random.uniform(8.0, 15.0), 2),
        tvl=3_200_000_000,
        risk_score=3.5,
        token_pair="ETH-USDC",
        pool_address="0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
    ))

    # Mock Curve data
    opportunities.append(Opportunity(
        protocol="Curve",
        chain=Chain.ETHEREUM,
        apy=round(random.uniform(4.0, 7.0), 2),
        tvl=2_800_000_000,
        risk_score=2.5,
        token_pair="stETH-ETH"
    ))

    return opportunities


async def scan_solana() -> List[Opportunity]:
    """Scan Solana for yield opportunities"""
    opportunities = []

    # Mock Raydium data
    opportunities.append(Opportunity(
        protocol="Raydium",
        chain=Chain.SOLANA,
        apy=round(random.uniform(15.0, 25.0), 2),
        tvl=450_000_000,
        risk_score=6.0,
        token_pair="SOL-USDC"
    ))

    # Mock Solend data
    opportunities.append(Opportunity(
        protocol="Solend",
        chain=Chain.SOLANA,
        apy=round(random.uniform(6.0, 12.0), 2),
        tvl=280_000_000,
        risk_score=4.5
    ))

    return opportunities


async def scan_bsc() -> List[Opportunity]:
    """Scan BSC for yield opportunities"""
    opportunities = []

    # Mock PancakeSwap data
    opportunities.append(Opportunity(
        protocol="PancakeSwap",
        chain=Chain.BSC,
        apy=round(random.uniform(10.0, 20.0), 2),
        tvl=1_200_000_000,
        risk_score=5.0,
        token_pair="BNB-BUSD"
    ))

    # Mock Venus data
    opportunities.append(Opportunity(
        protocol="Venus",
        chain=Chain.BSC,
        apy=round(random.uniform(5.0, 9.0), 2),
        tvl=680_000_000,
        risk_score=4.0
    ))

    return opportunities


async def scan_polygon() -> List[Opportunity]:
    """Scan Polygon for yield opportunities"""
    opportunities = []

    # Mock Aave Polygon data
    opportunities.append(Opportunity(
        protocol="Aave-V3",
        chain=Chain.POLYGON,
        apy=round(random.uniform(4.0, 6.5), 2),
        tvl=620_000_000,
        risk_score=2.5
    ))

    # Mock QuickSwap data
    opportunities.append(Opportunity(
        protocol="QuickSwap",
        chain=Chain.POLYGON,
        apy=round(random.uniform(7.0, 13.0), 2),
        tvl=380_000_000,
        risk_score=4.0,
        token_pair="MATIC-USDC"
    ))

    return opportunities


async def scan_arbitrum() -> List[Opportunity]:
    """Scan Arbitrum for yield opportunities"""
    opportunities = []

    # Mock Aave Arbitrum data
    opportunities.append(Opportunity(
        protocol="Aave-V3",
        chain=Chain.ARBITRUM,
        apy=round(random.uniform(3.8, 5.8), 2),
        tvl=540_000_000,
        risk_score=2.3
    ))

    # Mock GMX data
    opportunities.append(Opportunity(
        protocol="GMX",
        chain=Chain.ARBITRUM,
        apy=round(random.uniform(12.0, 18.0), 2),
        tvl=420_000_000,
        risk_score=5.5,
        token_pair="GLP"
    ))

    return opportunities


# ===== MESSAGE HANDLER (Official Pattern) =====
# Following: https://innovationlab.fetch.ai/resources/docs/agent-communication/uagent-uagent-communication

@scanner.on_message(model=OpportunityRequest)
async def handle_opportunity_request(ctx: Context, sender: str, msg: OpportunityRequest):
    """
    Handle opportunity scanning request from Portfolio Coordinator

    Pattern: @agent.on_message(model=MessageModel)
    Args: ctx (Context), sender (str), msg (MessageModel)
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

        if Chain.SOLANA in msg.chains:
            sol_ops = await scan_solana()
            all_opportunities.extend(sol_ops)

        if Chain.BSC in msg.chains:
            bsc_ops = await scan_bsc()
            all_opportunities.extend(bsc_ops)

        if Chain.POLYGON in msg.chains:
            poly_ops = await scan_polygon()
            all_opportunities.extend(poly_ops)

        if Chain.ARBITRUM in msg.chains:
            arb_ops = await scan_arbitrum()
            all_opportunities.extend(arb_ops)

        # Filter by criteria
        filtered_opportunities = [
            opp for opp in all_opportunities
            if opp.apy >= msg.min_apy and opp.risk_score <= msg.max_risk_score
        ]

        # Sort by APY (highest first)
        filtered_opportunities.sort(key=lambda x: x.apy, reverse=True)

        ctx.logger.info(f"✅ Found {len(filtered_opportunities)} opportunities matching criteria")

        # Send response back to coordinator (Official ctx.send pattern)
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


# ===== STARTUP EVENT HANDLER (Official Pattern) =====
# Following: https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation

@scanner.on_event("startup")
async def startup(ctx: Context):
    """
    Startup event handler - runs once when agent starts

    Pattern: @agent.on_event("startup")
    """
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


# ===== HTTP API ENDPOINTS (for Coordinator integration) =====

http_app = FastAPI(title="Chain Scanner HTTP API")

http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_app.get("/")
async def http_root():
    """Health check"""
    return {
        "status": "online",
        "service": "Chain Scanner",
        "agent_address": str(scanner.address),
        "chains": ["ethereum", "solana", "bsc", "polygon", "arbitrum"]
    }


@http_app.post("/query_opportunities")
async def http_query_opportunities(request: Request):
    """HTTP endpoint to query opportunities (called by Coordinator)"""
    try:
        data = await request.json()
        opp_request = OpportunityRequest(**data)

        # Scan chains (reuse the logic from message handler)
        all_opportunities = []

        if Chain.ETHEREUM in opp_request.chains:
            all_opportunities.extend(await scan_ethereum())

        if Chain.SOLANA in opp_request.chains:
            all_opportunities.extend(await scan_solana())

        if Chain.BSC in opp_request.chains:
            all_opportunities.extend(await scan_bsc())

        if Chain.POLYGON in opp_request.chains:
            all_opportunities.extend(await scan_polygon())

        if Chain.ARBITRUM in opp_request.chains:
            all_opportunities.extend(await scan_arbitrum())

        # Filter by criteria
        filtered_opportunities = [
            opp for opp in all_opportunities
            if opp.apy >= opp_request.min_apy and opp.risk_score <= opp_request.max_risk_score
        ]

        # Sort by APY (highest first)
        filtered_opportunities.sort(key=lambda x: x.apy, reverse=True)

        # Build response
        response = OpportunityResponse(
            request_id=opp_request.request_id,
            opportunities=filtered_opportunities,
            timestamp=datetime.now(timezone.utc).isoformat(),
            chains_scanned=opp_request.chains
        )

        return JSONResponse(response.dict())

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


def run_http_server():
    """Run HTTP server in background thread"""
    uvicorn.run(http_app, host="0.0.0.0", port=8001, log_level="warning")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🐝 YieldSwarm AI - Chain Scanner Agent")
    print("=" * 60)
    print(f"Agent Address: {scanner.address}")
    print(f"Port: {config.SCANNER_PORT}")
    print(f"HTTP API: http://localhost:8001")
    print(f"Mailbox: Enabled (Agentverse Ready)")
    print(f"Chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting dual-mode agent (uAgents + HTTP)...\n")

    # Start HTTP server in background thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run the agent (this blocks)
    scanner.run()
