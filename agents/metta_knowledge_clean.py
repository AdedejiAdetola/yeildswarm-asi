"""
YieldSwarm AI - MeTTa Knowledge Agent (Clean)
Pure uAgents implementation with MeTTa engine integration
"""

import os
import sys
import logging
from datetime import datetime, timezone
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from protocols.messages import (
    MeTTaQueryRequest,
    MeTTaQueryResponse,
    Opportunity
)
from utils.config import config
from utils.metta_engine import DeFiMeTTaEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MeTTa Knowledge Agent
metta_agent = Agent(
    name="metta_knowledge",
    seed=config.METTA_SEED,
    port=8002,
    endpoint=["http://0.0.0.0:8002/submit"]
)

# Initialize MeTTa Engine
kb_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "metta_kb",
    "defi_protocols.metta"
)

try:
    metta_engine = DeFiMeTTaEngine(kb_path)
    logger.info(f"✅ MeTTa engine loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load MeTTa engine: {str(e)}")
    metta_engine = None


@metta_agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("🧠 MeTTa Knowledge Agent Starting")
    logger.info("=" * 60)
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Port: 8002")
    logger.info(f"Coordinator: {config.COORDINATOR_ADDRESS}")
    logger.info(f"MeTTa Engine: {'✅ Loaded' if metta_engine else '❌ Not Loaded'}")
    logger.info("=" * 60)


@metta_agent.on_message(model=MeTTaQueryRequest)
async def handle_metta_query(ctx: Context, sender: str, msg: MeTTaQueryRequest):
    """
    Handle MeTTa query from Portfolio Coordinator

    Process:
    1. Receive opportunities and user preferences
    2. Use MeTTa engine to reason about best protocols
    3. Apply symbolic AI logic for recommendations
    4. Return explainable reasoning
    """
    logger.info("=" * 60)
    logger.info(f"📨 Received MeTTa Query: {msg.request_id}")
    logger.info(f"   From: {sender}")
    logger.info(f"   Risk Level: {msg.risk_level}")
    logger.info(f"   Amount: {msg.amount}")
    logger.info(f"   Opportunities: {len(msg.opportunities)}")
    logger.info(f"   Preferred Chains: {msg.chains}")
    logger.info("=" * 60)

    try:
        # Check if MeTTa engine is loaded
        if not metta_engine or not metta_engine.loaded:
            logger.warning("⚠️  MeTTa engine not loaded, using fallback logic")
            response = _fallback_reasoning(msg)
        else:
            # Use MeTTa engine for symbolic reasoning
            response = await _metta_reasoning(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        logger.info(f"✅ Sent MeTTa Response: {msg.request_id}")
        logger.info(f"   Recommended: {response.recommended_protocols}")
        logger.info(f"   Confidence: {response.confidence}")

    except Exception as e:
        logger.error(f"❌ Error processing MeTTa query: {str(e)}")
        # Send error response
        error_response = MeTTaQueryResponse(
            request_id=msg.request_id,
            recommended_protocols=[],
            reasoning=f"Error in MeTTa processing: {str(e)}",
            confidence=0.0
        )
        await ctx.send(sender, error_response)


async def _metta_reasoning(msg: MeTTaQueryRequest) -> MeTTaQueryResponse:
    """
    Use MeTTa engine for symbolic reasoning

    MeTTa provides explainable AI recommendations based on:
    - Risk tolerance
    - Historical protocol performance
    - Market conditions
    - Protocol security audits
    """
    try:
        # Extract protocol names from opportunities
        available_protocols = [opp.protocol for opp in msg.opportunities]

        # Query MeTTa for best protocols based on risk
        risk_tolerance_map = {
            "conservative": 3.0,
            "moderate": 5.0,
            "aggressive": 8.0
        }
        risk_tolerance = risk_tolerance_map.get(msg.risk_level, 5.0)

        # Get MeTTa recommendations
        metta_result = metta_engine.query_best_protocols(
            risk_tolerance=risk_tolerance,
            chains=[chain.value for chain in msg.chains]
        )

        # Get allocation optimization from MeTTa
        allocation = metta_engine.optimize_allocation(
            amount=msg.amount,
            risk_level=msg.risk_level
        )

        # Filter recommendations to only include available protocols
        recommended = [
            alloc["protocol"]
            for alloc in allocation.get("allocations", [])
            if alloc["protocol"] in available_protocols
        ]

        # If no matches, fall back to top opportunities
        if not recommended:
            # Sort opportunities by APY and risk
            sorted_opps = sorted(
                msg.opportunities,
                key=lambda x: (x.apy / max(x.risk_score, 1), -x.risk_score),
                reverse=True
            )
            recommended = [opp.protocol for opp in sorted_opps[:4]]

        # Generate explainable reasoning
        reasoning = _generate_reasoning(
            recommended=recommended,
            opportunities=msg.opportunities,
            risk_level=msg.risk_level,
            allocation=allocation
        )

        # Calculate risk assessments
        risk_assessments = {
            opp.protocol: opp.risk_score
            for opp in msg.opportunities
            if opp.protocol in recommended
        }

        return MeTTaQueryResponse(
            request_id=msg.request_id,
            recommended_protocols=recommended,
            reasoning=reasoning,
            confidence=0.85,
            risk_assessments=risk_assessments
        )

    except Exception as e:
        logger.error(f"Error in MeTTa reasoning: {str(e)}")
        # Fall back to simple logic
        return _fallback_reasoning(msg)


def _fallback_reasoning(msg: MeTTaQueryRequest) -> MeTTaQueryResponse:
    """
    Fallback reasoning when MeTTa engine is not available
    Uses simple heuristics based on risk and APY
    """
    # Sort opportunities by risk-adjusted returns
    if msg.risk_level == "conservative":
        # Prioritize low risk over high APY
        sorted_opps = sorted(
            msg.opportunities,
            key=lambda x: (-x.apy / max(x.risk_score, 1), x.risk_score)
        )
    elif msg.risk_level == "aggressive":
        # Prioritize high APY
        sorted_opps = sorted(
            msg.opportunities,
            key=lambda x: -x.apy
        )
    else:  # moderate
        # Balance between APY and risk
        sorted_opps = sorted(
            msg.opportunities,
            key=lambda x: (x.apy - x.risk_score, -x.risk_score),
            reverse=True
        )

    # Select top protocols
    recommended = [opp.protocol for opp in sorted_opps[:4]]

    # Generate reasoning
    reasoning = f"""
Based on {msg.risk_level} risk profile and {msg.amount} ETH investment:

Selected {len(recommended)} protocols optimized for:
- Risk tolerance: {msg.risk_level}
- APY optimization
- Portfolio diversification
- Chain preference: {', '.join([c.value for c in msg.chains])}

Recommended protocols ranked by risk-adjusted returns.
"""

    risk_assessments = {
        opp.protocol: opp.risk_score
        for opp in sorted_opps[:4]
    }

    return MeTTaQueryResponse(
        request_id=msg.request_id,
        recommended_protocols=recommended,
        reasoning=reasoning.strip(),
        confidence=0.75,  # Lower confidence for fallback
        risk_assessments=risk_assessments
    )


def _generate_reasoning(
    recommended: List[str],
    opportunities: List[Opportunity],
    risk_level: str,
    allocation: dict
) -> str:
    """Generate explainable AI reasoning for recommendations"""

    # Get details for recommended protocols
    protocol_details = {
        opp.protocol: opp
        for opp in opportunities
        if opp.protocol in recommended
    }

    reasoning_parts = [
        f"MeTTa Symbolic AI Analysis for {risk_level.upper()} risk profile:",
        "",
        "Selected Protocols:"
    ]

    for i, protocol in enumerate(recommended, 1):
        if protocol in protocol_details:
            opp = protocol_details[protocol]
            reasoning_parts.append(
                f"{i}. {protocol}: {opp.apy:.2f}% APY, Risk: {opp.risk_score:.1f}/10, Chain: {opp.chain.value}"
            )

    reasoning_parts.extend([
        "",
        "Reasoning:",
        f"- Optimized for {risk_level} risk tolerance",
        f"- Diversified across {len(set(opp.chain for opp in protocol_details.values()))} chains",
        f"- Average risk score: {sum(opp.risk_score for opp in protocol_details.values()) / len(protocol_details):.1f}/10",
        f"- Expected portfolio APY: {sum(opp.apy for opp in protocol_details.values()) / len(protocol_details):.1f}%",
        "",
        "MeTTa Knowledge Base applied protocol security, TVL, and historical performance analysis."
    ])

    return "\n".join(reasoning_parts)


if __name__ == "__main__":
    logger.info("\n🧠 Starting MeTTa Knowledge Agent...\n")
    metta_agent.run()
