"""
YieldSwarm AI - Strategy Engine Agent (Clean)
Pure uAgents implementation for portfolio allocation optimization
"""

import os
import sys
import logging
from datetime import datetime, timezone
from typing import List, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from protocols.messages import (
    StrategyRequest,
    StrategyResponse,
    AllocationItem,
    Opportunity,
    Chain
)
from utils.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Strategy Engine Agent
strategy_agent = Agent(
    name="strategy_engine",
    seed=config.STRATEGY_SEED,
    port=8003,
    endpoint=["http://0.0.0.0:8003/submit"]
)


@strategy_agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("⚡ Strategy Engine Agent Starting")
    logger.info("=" * 60)
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Port: 8003")
    logger.info(f"Coordinator: {config.COORDINATOR_ADDRESS}")
    logger.info("=" * 60)


@strategy_agent.on_message(model=StrategyRequest)
async def handle_strategy_request(ctx: Context, sender: str, msg: StrategyRequest):
    """
    Handle strategy request from Portfolio Coordinator

    Process:
    1. Receive available opportunities and MeTTa recommendations
    2. Calculate optimal allocation across protocols
    3. Balance risk, returns, and diversification
    4. Estimate gas costs
    5. Return detailed allocation strategy
    """
    logger.info("=" * 60)
    logger.info(f"📨 Received Strategy Request: {msg.request_id}")
    logger.info(f"   From: {sender}")
    logger.info(f"   Amount: {msg.amount} {msg.currency}")
    logger.info(f"   Risk Level: {msg.risk_level}")
    logger.info(f"   Opportunities: {len(msg.opportunities)}")
    logger.info(f"   Recommended: {msg.recommended_protocols}")
    logger.info("=" * 60)

    try:
        # Generate optimal allocation strategy
        strategy = _generate_strategy(msg)

        # Send response back to coordinator
        await ctx.send(sender, strategy)

        logger.info(f"✅ Sent Strategy Response: {msg.request_id}")
        logger.info(f"   Allocations: {len(strategy.allocations)}")
        logger.info(f"   Expected APY: {strategy.expected_apy:.2f}%")
        logger.info(f"   Risk Score: {strategy.risk_score:.1f}/10")

    except Exception as e:
        logger.error(f"❌ Error generating strategy: {str(e)}")
        # Send error response with empty strategy
        error_strategy = StrategyResponse(
            request_id=msg.request_id,
            allocations=[],
            expected_apy=0.0,
            risk_score=0.0,
            estimated_gas_cost=0.0,
            reasoning=f"Error generating strategy: {str(e)}",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        await ctx.send(sender, error_strategy)


def _generate_strategy(msg: StrategyRequest) -> StrategyResponse:
    """
    Generate optimal allocation strategy

    Algorithm:
    1. Filter opportunities to recommended protocols
    2. Apply risk-level specific allocation logic
    3. Optimize for diversification
    4. Calculate expected returns and risk
    """

    # Create lookup for opportunities
    opp_map: Dict[str, Opportunity] = {
        opp.protocol: opp for opp in msg.opportunities
    }

    # Filter to recommended protocols that have opportunities
    recommended_opps = [
        opp_map[protocol]
        for protocol in msg.recommended_protocols
        if protocol in opp_map
    ]

    if not recommended_opps:
        # Fall back to top opportunities by APY
        recommended_opps = sorted(
            msg.opportunities,
            key=lambda x: -x.apy
        )[:4]

    # Generate allocations based on risk level
    if msg.risk_level == "conservative":
        allocations = _conservative_allocation(msg.amount, recommended_opps)
    elif msg.risk_level == "aggressive":
        allocations = _aggressive_allocation(msg.amount, recommended_opps)
    else:  # moderate
        allocations = _moderate_allocation(msg.amount, recommended_opps)

    # Calculate portfolio metrics
    expected_apy = _calculate_weighted_apy(allocations)
    risk_score = _calculate_portfolio_risk(allocations)
    estimated_gas_cost = _estimate_gas_cost(allocations, msg.chains)

    # Generate reasoning
    reasoning = _generate_reasoning(
        allocations=allocations,
        risk_level=msg.risk_level,
        expected_apy=expected_apy,
        risk_score=risk_score
    )

    return StrategyResponse(
        request_id=msg.request_id,
        allocations=allocations,
        expected_apy=expected_apy,
        risk_score=risk_score,
        estimated_gas_cost=estimated_gas_cost,
        reasoning=reasoning,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


def _conservative_allocation(amount: float, opportunities: List[Opportunity]) -> List[AllocationItem]:
    """
    Conservative strategy: Prioritize low risk, stable returns

    Allocation rules:
    - 50% to lowest risk protocol
    - 30% to second lowest risk
    - 20% to third lowest risk
    - Diversification across chains
    """
    # Sort by risk score (lowest first)
    sorted_opps = sorted(opportunities, key=lambda x: x.risk_score)[:3]

    percentages = [50, 30, 20]
    allocations = []

    for i, opp in enumerate(sorted_opps):
        pct = percentages[i] if i < len(percentages) else 0
        if pct == 0:
            continue

        allocations.append(AllocationItem(
            protocol=opp.protocol,
            chain=opp.chain.value,
            amount=amount * (pct / 100),
            percentage=pct,
            expected_apy=opp.apy,
            risk_score=opp.risk_score
        ))

    return allocations


def _moderate_allocation(amount: float, opportunities: List[Opportunity]) -> List[AllocationItem]:
    """
    Moderate strategy: Balance risk and returns

    Allocation rules:
    - Equal weight across top 4 protocols
    - Sorted by risk-adjusted returns (APY / risk_score)
    - Diversified across chains
    """
    # Sort by risk-adjusted returns
    sorted_opps = sorted(
        opportunities,
        key=lambda x: x.apy / max(x.risk_score, 1),
        reverse=True
    )[:4]

    pct = 100 / len(sorted_opps)
    allocations = []

    for opp in sorted_opps:
        allocations.append(AllocationItem(
            protocol=opp.protocol,
            chain=opp.chain.value,
            amount=amount * (pct / 100),
            percentage=pct,
            expected_apy=opp.apy,
            risk_score=opp.risk_score
        ))

    return allocations


def _aggressive_allocation(amount: float, opportunities: List[Opportunity]) -> List[AllocationItem]:
    """
    Aggressive strategy: Prioritize high returns

    Allocation rules:
    - 40% to highest APY
    - 30% to second highest APY
    - 20% to third highest APY
    - 10% to fourth highest APY
    """
    # Sort by APY (highest first)
    sorted_opps = sorted(opportunities, key=lambda x: -x.apy)[:4]

    percentages = [40, 30, 20, 10]
    allocations = []

    for i, opp in enumerate(sorted_opps):
        pct = percentages[i] if i < len(percentages) else 0
        if pct == 0:
            continue

        allocations.append(AllocationItem(
            protocol=opp.protocol,
            chain=opp.chain.value,
            amount=amount * (pct / 100),
            percentage=pct,
            expected_apy=opp.apy,
            risk_score=opp.risk_score
        ))

    return allocations


def _calculate_weighted_apy(allocations: List[AllocationItem]) -> float:
    """Calculate weighted average APY across allocations"""
    if not allocations:
        return 0.0

    weighted_sum = sum(
        alloc.expected_apy * (alloc.percentage / 100)
        for alloc in allocations
    )
    return weighted_sum


def _calculate_portfolio_risk(allocations: List[AllocationItem]) -> float:
    """Calculate weighted portfolio risk score"""
    if not allocations:
        return 0.0

    weighted_risk = sum(
        alloc.risk_score * (alloc.percentage / 100)
        for alloc in allocations
    )
    return weighted_risk


def _estimate_gas_cost(allocations: List[AllocationItem], chains: List[Chain]) -> float:
    """
    Estimate total gas cost for executing strategy

    Rough estimates per chain:
    - Ethereum: 0.01 ETH per transaction
    - BSC: 0.001 ETH per transaction
    - Polygon: 0.0005 ETH per transaction
    - Arbitrum: 0.002 ETH per transaction
    - Solana: 0.0001 ETH per transaction
    """
    gas_costs = {
        "ethereum": 0.01,
        "bsc": 0.001,
        "polygon": 0.0005,
        "arbitrum": 0.002,
        "solana": 0.0001
    }

    total_gas = 0.0
    for alloc in allocations:
        chain = alloc.chain.lower()
        total_gas += gas_costs.get(chain, 0.005)

    return total_gas


def _generate_reasoning(
    allocations: List[AllocationItem],
    risk_level: str,
    expected_apy: float,
    risk_score: float
) -> str:
    """Generate human-readable reasoning for strategy"""

    chains_used = set(alloc.chain for alloc in allocations)
    protocol_count = len(allocations)

    reasoning_parts = [
        f"Strategy optimized for {risk_level.upper()} risk profile:",
        "",
        "Allocation Breakdown:"
    ]

    for alloc in allocations:
        reasoning_parts.append(
            f"• {alloc.protocol} ({alloc.chain}): {alloc.percentage:.1f}% "
            f"({alloc.amount:.4f} ETH) - APY: {alloc.expected_apy:.2f}%, Risk: {alloc.risk_score:.1f}/10"
        )

    reasoning_parts.extend([
        "",
        "Portfolio Metrics:",
        f"• Expected APY: {expected_apy:.2f}%",
        f"• Portfolio Risk Score: {risk_score:.1f}/10",
        f"• Protocols: {protocol_count}",
        f"• Chains: {len(chains_used)} ({', '.join(chains_used)})",
        "",
        f"Strategy emphasizes {'low risk and stable returns' if risk_level == 'conservative' else 'high returns' if risk_level == 'aggressive' else 'balanced risk/return'}."
    ])

    return "\n".join(reasoning_parts)


if __name__ == "__main__":
    logger.info("\n⚡ Starting Strategy Engine Agent...\n")
    strategy_agent.run()
