"""
YieldSwarm AI - Chain Scanner Agent
Scans multiple blockchains for DeFi yield opportunities
AGENTVERSE DEPLOYMENT VERSION - Self-contained
"""
from uagents import Agent, Context
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import random

# ===== INLINE MESSAGE MODELS =====

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"

class OpportunityRequest(BaseModel):
    request_id: str
    chains: List[Chain]
    min_apy: float = 0.0
    max_risk_score: float = 10.0

class Opportunity(BaseModel):
    protocol: str
    chain: Chain
    apy: float
    tvl: float
    risk_score: float
    pool_address: Optional[str] = None
    token_pair: Optional[str] = None

class OpportunityResponse(BaseModel):
    request_id: str
    opportunities: List[Opportunity]
    timestamp: str
    chains_scanned: List[Chain]

# ===== CONFIGURATION =====
SCANNER_SEED = "scanner-dev-seed-yieldswarm"
SCANNER_PORT = 8001

# ===== AGENT INITIALIZATION =====
# Note: In Agentverse, use the preloaded 'agent' instance
# For local: scanner = Agent(name="yieldswarm-scanner", seed=SCANNER_SEED, port=SCANNER_PORT, mailbox=True)
try:
    # Try to use the preloaded agent (Agentverse)
    scanner = agent  # type: ignore
except NameError:
    # Fall back to creating new agent (local development)
    scanner = Agent(
        name="yieldswarm-scanner",
        seed=SCANNER_SEED,
        port=SCANNER_PORT,
        mailbox=True,
        endpoint=[f"http://localhost:{SCANNER_PORT}/submit"],
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

@scanner.on_message(model=OpportunityRequest)
async def handle_opportunity_request(ctx: Context, sender: str, msg: OpportunityRequest):
    """Handle opportunity scanning request from Portfolio Coordinator"""
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

@scanner.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler - runs once when agent starts"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🔍 Chain Scanner Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Address: {scanner.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Supported Chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    ctx.logger.info(f"Protocols: 10+ DeFi protocols")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive opportunity scan requests")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Chain Scanner Agent")
    print(f"Address: {scanner.address}")
    print(f"Mailbox: Enabled\n")
    scanner.run()
