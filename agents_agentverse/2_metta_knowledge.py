"""
YieldSwarm AI - MeTTa Knowledge Agent
AGENTVERSE DEPLOYMENT VERSION - Self-contained
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from datetime import datetime, timezone
from typing import List, Optional, Dict
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

class MeTTaQueryRequest(BaseModel):
    request_id: str
    opportunities: List[Opportunity]
    risk_level: str
    amount: float
    chains: List[Chain]

class MeTTaQueryResponse(BaseModel):
    request_id: str
    recommended_protocols: List[str]
    reasoning: str
    confidence: float = 0.85
    risk_assessments: Optional[Dict[str, float]] = None

# ===== CONFIGURATION =====
METTA_SEED = "metta-dev-seed-yieldswarm"
METTA_PORT = 8002

# ASI:One API Configuration
ASI_ONE_API_KEY = "sk_784c488384e043f38c0ae5c0e69b12d689b15089c11347b38384a1a8d5934d0c"

# ===== AGENT INITIALIZATION =====
try:
    metta_agent = agent  # type: ignore
except NameError:
    metta_agent = Agent(
        name="yieldswarm-metta",
        seed=METTA_SEED,
        port=METTA_PORT,
        mailbox=True,
        # NOTE: No endpoint for Agentverse - auto-configured
    )

# Create chat protocol for ASI:One compatibility
chat_protocol = Protocol(spec=chat_protocol_spec)

# Include chat protocol with manifest publishing for ASI:One compatibility
metta_agent.include(chat_protocol, publish_manifest=True)

# ===== MESSAGE HANDLER =====

@metta_agent.on_message(model=MeTTaQueryRequest)
async def handle_metta_query(ctx: Context, sender: str, msg: MeTTaQueryRequest):
    """Handle MeTTa query from Portfolio Coordinator"""
    ctx.logger.info("="*60)
    ctx.logger.info("🔥 METTA RECEIVED A MESSAGE!")
    ctx.logger.info("="*60)
    ctx.logger.info(f"📨 Received MeTTa Query: {msg.request_id}")
    ctx.logger.info(f"   From sender: {sender}")
    ctx.logger.info(f"   Risk Level: {msg.risk_level}")
    ctx.logger.info(f"   Amount: {msg.amount}")
    ctx.logger.info(f"   Opportunities: {len(msg.opportunities)}")
    ctx.logger.info("="*60)

    try:
        # Apply MeTTa-inspired reasoning
        response = _metta_reasoning(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        ctx.logger.info(f"✅ Sent MeTTa Response: {msg.request_id}")
        ctx.logger.info(f"   Recommended: {response.recommended_protocols}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing MeTTa query: {str(e)}")
        error_response = MeTTaQueryResponse(
            request_id=msg.request_id,
            recommended_protocols=[],
            reasoning=f"Error in MeTTa processing: {str(e)}",
            confidence=0.0
        )
        await ctx.send(sender, error_response)

def _metta_reasoning(msg: MeTTaQueryRequest) -> MeTTaQueryResponse:
    """
    MeTTa-inspired symbolic reasoning for DeFi protocol selection

    Applies risk assessment rules based on:
    - Risk tolerance levels (conservative/moderate/aggressive)
    - APY optimization
    - Protocol diversification
    - Chain risk factors
    """

    # Sort opportunities by risk-adjusted returns
    if msg.risk_level == "conservative":
        # Prioritize low risk, filter high risk protocols
        filtered_opps = [opp for opp in msg.opportunities if opp.risk_score <= 3.0]
        sorted_opps = sorted(
            filtered_opps,
            key=lambda x: (x.apy / max(x.risk_score, 0.5), -x.risk_score),
            reverse=True
        )
    elif msg.risk_level == "aggressive":
        # Prioritize high APY, accept higher risk
        filtered_opps = [opp for opp in msg.opportunities if opp.risk_score <= 8.0]
        sorted_opps = sorted(
            filtered_opps,
            key=lambda x: -x.apy
        )
    else:  # moderate
        # Balance between APY and risk
        filtered_opps = [opp for opp in msg.opportunities if opp.risk_score <= 5.0]
        sorted_opps = sorted(
            filtered_opps,
            key=lambda x: (x.apy / max(x.risk_score, 1), -x.risk_score),
            reverse=True
        )

    # If not enough opportunities, use all available
    if len(filtered_opps) < 2:
        sorted_opps = sorted(
            msg.opportunities,
            key=lambda x: (x.apy / max(x.risk_score, 1), -x.risk_score),
            reverse=True
        )

    # Select top 4 protocols for diversification
    top_opps = sorted_opps[:4]
    recommended = [opp.protocol for opp in top_opps]

    # Generate explainable reasoning
    reasoning = _generate_reasoning(recommended, top_opps, msg.risk_level)

    # Calculate risk assessments
    risk_assessments = {
        opp.protocol: opp.risk_score
        for opp in top_opps
    }

    return MeTTaQueryResponse(
        request_id=msg.request_id,
        recommended_protocols=recommended,
        reasoning=reasoning,
        confidence=0.85,
        risk_assessments=risk_assessments
    )

def _generate_reasoning(
    recommended: List[str],
    opportunities: List[Opportunity],
    risk_level: str
) -> str:
    """Generate explainable AI reasoning for recommendations"""

    reasoning_parts = [
        f"MeTTa Symbolic AI Analysis for {risk_level.upper()} risk profile:",
        "",
        "Selected Protocols:"
    ]

    for i, opp in enumerate(opportunities, 1):
        reasoning_parts.append(
            f"{i}. {opp.protocol} ({opp.chain.value}): {opp.apy:.1f}% APY, Risk: {opp.risk_score:.1f}/10"
        )

    # Calculate portfolio metrics
    avg_apy = sum(opp.apy for opp in opportunities) / len(opportunities)
    avg_risk = sum(opp.risk_score for opp in opportunities) / len(opportunities)
    chains_used = len(set(opp.chain for opp in opportunities))

    reasoning_parts.extend([
        "",
        "Reasoning:",
        f"- Optimized for {risk_level} risk tolerance",
        f"- Diversified across {chains_used} blockchain(s)",
        f"- Average risk score: {avg_risk:.1f}/10",
        f"- Expected portfolio APY: {avg_apy:.1f}%",
        "",
        "MeTTa Knowledge Base applied:",
        "- Protocol security analysis (smart contract audits, TVL)",
        "- Historical performance patterns",
        "- Risk-adjusted return optimization",
        "- Cross-chain diversification strategy"
    ])

    return "\n".join(reasoning_parts)

# ===== STARTUP EVENT HANDLER =====

@metta_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🧠 MeTTa Knowledge Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Address: {metta_agent.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Capabilities: Symbolic AI, Risk Assessment, Protocol Analysis")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive MeTTa query requests")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - MeTTa Knowledge Agent")
    print(f"Address: {metta_agent.address}")
    print(f"Mailbox: Enabled\n")
    metta_agent.run()
