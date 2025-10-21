"""
YieldSwarm AI - Performance Tracker Agent
AGENTVERSE DEPLOYMENT VERSION - Self-contained
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

# ===== INLINE MESSAGE MODELS =====

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"

class PerformanceQuery(BaseModel):
    request_id: str
    user_id: str
    query_type: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class PositionDetail(BaseModel):
    protocol: str
    chain: Chain
    amount: float
    entry_value: float
    current_value: float
    pnl: float
    pnl_percentage: float
    current_apy: float
    days_held: int

class PerformanceResponse(BaseModel):
    request_id: str
    user_id: str
    total_portfolio_value: float
    total_pnl: float
    total_pnl_percentage: float
    positions: List[PositionDetail]
    realized_apy: float
    total_gas_spent: float
    timestamp: str

# ===== CONFIGURATION =====
TRACKER_SEED = process.env.TRACKER_SEED
TRACKER_PORT = 8005

# ASI:One API Configuration
ASI_ONE_API_KEY = process.env.ASI_ONE_API_KEY

# Simulated portfolio data storage
portfolio_data: Dict[str, List[PositionDetail]] = {}

# ===== AGENT INITIALIZATION =====
try:
    tracker_agent = agent  # type: ignore
except NameError:
    tracker_agent = Agent(
        name="yieldswarm-tracker",
        seed=TRACKER_SEED,
        port=TRACKER_PORT,
        mailbox=True,
        # NOTE: No endpoint for Agentverse - auto-configured
    )

# # Create chat protocol for ASI:One compatibility
# chat_protocol = Protocol(spec=chat_protocol_spec)

# # Include chat protocol with manifest publishing for ASI:One compatibility
# tracker_agent.include(chat_protocol, publish_manifest=True)

# ===== MESSAGE HANDLER =====

@tracker_agent.on_message(model=PerformanceQuery)
async def handle_performance_query(ctx: Context, sender: str, msg: PerformanceQuery):
    """Handle performance query from Portfolio Coordinator"""
    ctx.logger.info(f"📨 Received Performance Query: {msg.request_id}")
    ctx.logger.info(f"   User: {msg.user_id}")
    ctx.logger.info(f"   Query Type: {msg.query_type}")

    try:
        # Generate performance response
        response = _generate_performance_report(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        ctx.logger.info(f"✅ Sent Performance Response: {msg.request_id}")
        ctx.logger.info(f"   Portfolio Value: ${response.total_portfolio_value:,.2f}")
        ctx.logger.info(f"   P&L: {response.total_pnl_percentage:.2f}%")

    except Exception as e:
        ctx.logger.error(f"❌ Error generating performance report: {str(e)}")
        error_response = PerformanceResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            total_portfolio_value=0.0,
            total_pnl=0.0,
            total_pnl_percentage=0.0,
            positions=[],
            realized_apy=0.0,
            total_gas_spent=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        await ctx.send(sender, error_response)

def _generate_performance_report(msg: PerformanceQuery) -> PerformanceResponse:
    """
    Generate performance report (SIMULATED)

    In production, this would:
    - Track real on-chain positions
    - Calculate actual P&L
    - Monitor APY changes
    - Generate tax reports

    For demo: Returns simulated performance data
    """

    # Check if user has portfolio data
    if msg.user_id not in portfolio_data:
        # Generate sample positions for demo
        positions = _generate_sample_positions()
        portfolio_data[msg.user_id] = positions
    else:
        positions = portfolio_data[msg.user_id]

    # Calculate portfolio metrics
    total_value = sum(pos.current_value for pos in positions)
    total_pnl = sum(pos.pnl for pos in positions)
    total_pnl_percentage = (total_pnl / sum(pos.entry_value for pos in positions)) * 100 if positions else 0.0

    # Calculate realized APY (weighted by position size)
    if positions:
        weighted_apy = sum(
            pos.current_apy * (pos.current_value / total_value)
            for pos in positions
        )
    else:
        weighted_apy = 0.0

    # Estimate total gas spent (simulated)
    total_gas = len(positions) * 0.015  # ~0.015 ETH per position

    return PerformanceResponse(
        request_id=msg.request_id,
        user_id=msg.user_id,
        total_portfolio_value=total_value,
        total_pnl=total_pnl,
        total_pnl_percentage=total_pnl_percentage,
        positions=positions,
        realized_apy=weighted_apy,
        total_gas_spent=total_gas,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def _generate_sample_positions() -> List[PositionDetail]:
    """Generate sample portfolio positions for demo"""
    import random

    positions = [
        PositionDetail(
            protocol="Aave-V3",
            chain=Chain.ETHEREUM,
            amount=5.0,
            entry_value=10000.0,
            current_value=10250.0,
            pnl=250.0,
            pnl_percentage=2.5,
            current_apy=4.8,
            days_held=30
        ),
        PositionDetail(
            protocol="Uniswap-V3",
            chain=Chain.ETHEREUM,
            amount=3.0,
            entry_value=6000.0,
            current_value=6420.0,
            pnl=420.0,
            pnl_percentage=7.0,
            current_apy=13.2,
            days_held=30
        ),
        PositionDetail(
            protocol="Raydium",
            chain=Chain.SOLANA,
            amount=2.0,
            entry_value=4000.0,
            current_value=4560.0,
            pnl=560.0,
            pnl_percentage=14.0,
            current_apy=19.5,
            days_held=30
        ),
    ]

    return positions

# ===== STARTUP EVENT HANDLER =====

@tracker_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("📊 Performance Tracker Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Address: {tracker_agent.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Mode: SIMULATION (Demo data)")
    ctx.logger.info(f"Capabilities: P&L Tracking, APY Monitoring, Tax Reports")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive performance queries")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Performance Tracker Agent")
    print(f"Address: {tracker_agent.address}")
    print(f"Mailbox: Enabled\n")
    tracker_agent.run()
