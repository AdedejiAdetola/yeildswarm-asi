"""
YieldSwarm AI - Chain Scanner Agent
Monitors multiple chains for yield opportunities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from datetime import datetime, timezone
from utils.config import config
from utils.models import YieldOpportunity, Chain, ProtocolType, OpportunityData
import asyncio
import random


# Create Chain Scanner Agent (Local Mode with Endpoint)
scanner = Agent(
    name="yieldswarm-scanner",
    seed=config.SCANNER_SEED,
    port=config.SCANNER_PORT,
    endpoint=["http://127.0.0.1:8001/submit"],
)


async def scan_ethereum(ctx: Context) -> list[YieldOpportunity]:
    """Scan Ethereum for yield opportunities"""
    opportunities = []

    # Simulate Aave monitoring
    opportunities.append(YieldOpportunity(
        protocol="Aave-V3",
        chain=Chain.ETHEREUM,
        protocol_type=ProtocolType.LENDING,
        apy=random.uniform(3.5, 5.5),
        tvl=1_500_000_000,
        risk_score=2.0,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate Uniswap V3 monitoring
    opportunities.append(YieldOpportunity(
        protocol="Uniswap-V3",
        chain=Chain.ETHEREUM,
        protocol_type=ProtocolType.DEX,
        apy=random.uniform(8.0, 15.0),
        tvl=3_200_000_000,
        risk_score=4.5,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate Curve monitoring
    opportunities.append(YieldOpportunity(
        protocol="Curve",
        chain=Chain.ETHEREUM,
        protocol_type=ProtocolType.YIELD,
        apy=random.uniform(4.0, 7.0),
        tvl=2_800_000_000,
        risk_score=2.5,
        timestamp=datetime.now(timezone.utc)
    ))

    return opportunities


async def scan_solana(ctx: Context) -> list[YieldOpportunity]:
    """Scan Solana for yield opportunities"""
    opportunities = []

    # Simulate Raydium monitoring
    opportunities.append(YieldOpportunity(
        protocol="Raydium",
        chain=Chain.SOLANA,
        protocol_type=ProtocolType.DEX,
        apy=random.uniform(15.0, 25.0),
        tvl=450_000_000,
        risk_score=6.0,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate Solend monitoring
    opportunities.append(YieldOpportunity(
        protocol="Solend",
        chain=Chain.SOLANA,
        protocol_type=ProtocolType.LENDING,
        apy=random.uniform(6.0, 12.0),
        tvl=280_000_000,
        risk_score=4.5,
        timestamp=datetime.now(timezone.utc)
    ))

    return opportunities


async def scan_bsc(ctx: Context) -> list[YieldOpportunity]:
    """Scan BSC for yield opportunities"""
    opportunities = []

    # Simulate PancakeSwap monitoring
    opportunities.append(YieldOpportunity(
        protocol="PancakeSwap",
        chain=Chain.BSC,
        protocol_type=ProtocolType.DEX,
        apy=random.uniform(10.0, 20.0),
        tvl=1_200_000_000,
        risk_score=5.0,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate Venus monitoring
    opportunities.append(YieldOpportunity(
        protocol="Venus",
        chain=Chain.BSC,
        protocol_type=ProtocolType.LENDING,
        apy=random.uniform(5.0, 9.0),
        tvl=680_000_000,
        risk_score=4.0,
        timestamp=datetime.now(timezone.utc)
    ))

    return opportunities


async def scan_polygon(ctx: Context) -> list[YieldOpportunity]:
    """Scan Polygon for yield opportunities"""
    opportunities = []

    # Simulate Aave Polygon monitoring
    opportunities.append(YieldOpportunity(
        protocol="Aave-V3",
        chain=Chain.POLYGON,
        protocol_type=ProtocolType.LENDING,
        apy=random.uniform(4.0, 6.5),
        tvl=620_000_000,
        risk_score=2.5,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate QuickSwap monitoring
    opportunities.append(YieldOpportunity(
        protocol="QuickSwap",
        chain=Chain.POLYGON,
        protocol_type=ProtocolType.DEX,
        apy=random.uniform(7.0, 13.0),
        tvl=380_000_000,
        risk_score=4.0,
        timestamp=datetime.now(timezone.utc)
    ))

    return opportunities


async def scan_arbitrum(ctx: Context) -> list[YieldOpportunity]:
    """Scan Arbitrum for yield opportunities"""
    opportunities = []

    # Simulate Aave Arbitrum monitoring
    opportunities.append(YieldOpportunity(
        protocol="Aave-V3",
        chain=Chain.ARBITRUM,
        protocol_type=ProtocolType.LENDING,
        apy=random.uniform(3.8, 5.8),
        tvl=540_000_000,
        risk_score=2.3,
        timestamp=datetime.now(timezone.utc)
    ))

    # Simulate GMX monitoring
    opportunities.append(YieldOpportunity(
        protocol="GMX",
        chain=Chain.ARBITRUM,
        protocol_type=ProtocolType.YIELD,
        apy=random.uniform(12.0, 18.0),
        tvl=420_000_000,
        risk_score=5.5,
        timestamp=datetime.now(timezone.utc)
    ))

    return opportunities


@scanner.on_interval(period=30.0)  # Scan every 30 seconds
async def scan_all_chains(ctx: Context):
    """Continuously scan all chains for opportunities"""
    ctx.logger.info("🔍 Scanning all chains for yield opportunities...")

    all_opportunities = []

    # Scan all chains in parallel
    try:
        eth_ops, sol_ops, bsc_ops, poly_ops, arb_ops = await asyncio.gather(
            scan_ethereum(ctx),
            scan_solana(ctx),
            scan_bsc(ctx),
            scan_polygon(ctx),
            scan_arbitrum(ctx),
        )

        all_opportunities.extend(eth_ops)
        all_opportunities.extend(sol_ops)
        all_opportunities.extend(bsc_ops)
        all_opportunities.extend(poly_ops)
        all_opportunities.extend(arb_ops)

        # Sort by APY
        all_opportunities.sort(key=lambda x: x.apy, reverse=True)

        ctx.logger.info(f"✅ Found {len(all_opportunities)} opportunities")

        # Log top 3
        for i, opp in enumerate(all_opportunities[:3], 1):
            ctx.logger.info(
                f"  {i}. {opp.protocol} on {opp.chain.value}: "
                f"{opp.apy:.2f}% APY (Risk: {opp.risk_score})"
            )

        # In production, broadcast to Strategy Engine
        # opportunity_data = OpportunityData(
        #     opportunities=all_opportunities,
        #     timestamp=datetime.now(timezone.utc)
        # )
        # await ctx.send(config.STRATEGY_ADDRESS, opportunity_data)

    except Exception as e:
        ctx.logger.error(f"Error scanning chains: {str(e)}")


@scanner.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("Chain Scanner Agent started")
    ctx.logger.info(f"Agent address: {scanner.address}")
    ctx.logger.info("Monitoring chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    ctx.logger.info(f"Scan interval: 30 seconds")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Chain Scanner Agent")
    print("=" * 60)
    print(f"Agent Address: {scanner.address}")
    print(f"Port: {config.SCANNER_PORT}")
    print(f"Chains: Ethereum, Solana, BSC, Polygon, Arbitrum")
    print(f"Protocols: 20+ DeFi protocols")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting 24/7 monitoring...\n")

    scanner.run()
