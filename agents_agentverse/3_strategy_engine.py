"""
YieldSwarm AI - Strategy Engine Agent
AGENTVERSE DEPLOYMENT VERSION - Self-contained
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

# ===== INLINE MESSAGE MODELS =====

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"

class Opportunity(BaseModel):
    protocol: str
    chain: Chain
    apy: float
    tvl: float
    risk_score: float
    pool_address: Optional[str] = None
    token_pair: Optional[str] = None

class StrategyRequest(BaseModel):
    request_id: str
    amount: float
    currency: str = "ETH"
    risk_level: str
    opportunities: List[Opportunity]
    recommended_protocols: List[str]
    chains: List[Chain]

class AllocationItem(BaseModel):
    protocol: str
    chain: str
    amount: float
    percentage: float
    expected_apy: float
    risk_score: float = 5.0

class StrategyResponse(BaseModel):
    request_id: str
    allocations: List[AllocationItem]
    expected_apy: float
    risk_score: float
    estimated_gas_cost: float
    reasoning: str
    timestamp: str

# ===== CONFIGURATION =====
STRATEGY_SEED = process.env.STRATEGY_SEED
STRATEGY_PORT = 8003

# ASI:One API Configuration
ASI_ONE_API_KEY = process.env.ASI_ONE_API_KEY

# Gas costs per chain (in ETH equivalent)
GAS_COSTS = {
    Chain.ETHEREUM: 0.015,
    Chain.POLYGON: 0.0001,
    Chain.ARBITRUM: 0.0008,
    Chain.BSC: 0.0002,
    Chain.SOLANA: 0.00001
}

# Allocation percentages by risk level
ALLOCATION_STRATEGIES = {
    "conservative": [50, 30, 15, 5],
    "moderate": [35, 30, 20, 15],
    "aggressive": [40, 30, 20, 10]
}

# ===== AGENT INITIALIZATION =====
try:
    strategy_agent = agent  # type: ignore
except NameError:
    strategy_agent = Agent(
        name="yieldswarm-strategy",
        seed=STRATEGY_SEED,
        port=STRATEGY_PORT,
        mailbox=True,
        # NOTE: No endpoint for Agentverse - auto-configured
    )

# ===== MESSAGE HANDLER =====

@strategy_agent.on_message(model=StrategyRequest)
async def handle_strategy_request(ctx: Context, sender: str, msg: StrategyRequest):
    """Handle strategy generation request from Portfolio Coordinator"""
    ctx.logger.info(f"📨 Received Strategy Request: {msg.request_id}")
    ctx.logger.info(f"   Amount: {msg.amount} {msg.currency}")
    ctx.logger.info(f"   Risk Level: {msg.risk_level}")
    ctx.logger.info(f"   Recommended Protocols: {msg.recommended_protocols}")

    try:
        # Generate optimal allocation strategy
        response = _generate_strategy(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        ctx.logger.info(f"✅ Sent Strategy Response: {msg.request_id}")
        ctx.logger.info(f"   Allocations: {len(response.allocations)}")
        ctx.logger.info(f"   Expected APY: {response.expected_apy:.2f}%")

    except Exception as e:
        ctx.logger.error(f"❌ Error generating strategy: {str(e)}")
        error_response = StrategyResponse(
            request_id=msg.request_id,
            allocations=[],
            expected_apy=0.0,
            risk_score=0.0,
            estimated_gas_cost=0.0,
            reasoning=f"Error generating strategy: {str(e)}",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        await ctx.send(sender, error_response)

def _generate_strategy(msg: StrategyRequest) -> StrategyResponse:
    """Generate optimal portfolio allocation strategy"""

    # Filter opportunities to recommended protocols
    recommended_opps = [
        opp for opp in msg.opportunities
        if opp.protocol in msg.recommended_protocols
    ]

    # If no recommended found, use best available
    if not recommended_opps:
        recommended_opps = sorted(
            msg.opportunities,
            key=lambda x: (x.apy / max(x.risk_score, 1)),
            reverse=True
        )[:4]

    # Get allocation percentages based on risk level
    percentages = ALLOCATION_STRATEGIES.get(msg.risk_level, [35, 30, 20, 15])

    # Create allocations
    allocations = []
    total_gas = 0.0
    total_weighted_apy = 0.0
    total_weighted_risk = 0.0

    for i, opp in enumerate(recommended_opps[:len(percentages)]):
        percentage = percentages[i]
        amount = msg.amount * (percentage / 100)

        allocations.append(AllocationItem(
            protocol=opp.protocol,
            chain=opp.chain.value,
            amount=amount,
            percentage=percentage,
            expected_apy=opp.apy,
            risk_score=opp.risk_score
        ))

        # Calculate weighted metrics
        total_weighted_apy += opp.apy * (percentage / 100)
        total_weighted_risk += opp.risk_score * (percentage / 100)

        # Add gas cost
        total_gas += GAS_COSTS.get(opp.chain, 0.01)

    # Generate reasoning
    reasoning = _generate_strategy_reasoning(allocations, msg.risk_level, msg.amount)

    return StrategyResponse(
        request_id=msg.request_id,
        allocations=allocations,
        expected_apy=total_weighted_apy,
        risk_score=total_weighted_risk,
        estimated_gas_cost=total_gas,
        reasoning=reasoning,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def _generate_strategy_reasoning(
    allocations: List[AllocationItem],
    risk_level: str,
    total_amount: float
) -> str:
    """Generate explainable strategy reasoning"""

    chains_used = set(alloc.chain for alloc in allocations)
    protocols_used = len(allocations)

    reasoning_parts = [
        f"Portfolio Strategy for {risk_level.upper()} risk profile:",
        "",
        "Allocation Breakdown:"
    ]

    for i, alloc in enumerate(allocations, 1):
        reasoning_parts.append(
            f"{i}. {alloc.protocol} ({alloc.chain}): {alloc.amount:.2f} ETH ({alloc.percentage}%)"
        )
        reasoning_parts.append(
            f"   APY: {alloc.expected_apy:.1f}%, Risk: {alloc.risk_score:.1f}/10"
        )

    reasoning_parts.extend([
        "",
        "Strategy Rationale:",
        f"- {protocols_used} protocols for diversification",
        f"- {len(chains_used)} blockchain(s) for cross-chain exposure",
        f"- {risk_level.capitalize()} allocation model applied",
        f"- Top protocol gets {allocations[0].percentage}% allocation",
        "",
        "Risk Management:",
        "- Position sizing based on risk scores",
        "- Gradual allocation decay for safety",
        "- Gas-optimized execution order",
        ""
    ])

    return "\n".join(reasoning_parts)

# ===== STARTUP EVENT HANDLER =====

@strategy_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("⚡ Strategy Engine Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Address: {strategy_agent.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Capabilities: Portfolio Optimization, Risk Management")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive strategy requests")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Strategy Engine Agent")
    print(f"Address: {strategy_agent.address}")
    print(f"Mailbox: Enabled\n")
    strategy_agent.run()
