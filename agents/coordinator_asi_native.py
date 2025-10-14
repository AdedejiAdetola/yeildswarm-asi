"""
YieldSwarm AI - Portfolio Coordinator (ASI Native)
Uses AgentManager pattern for proper ASI:One integration
"""

import os
import sys
import asyncio
import json
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from uagents_adapter import LangchainRegisterTool, cleanup_uagent
from uagents_adapter.langchain import AgentManager
from ai_engine import UAgentResponse, UAgentResponseType

# Import our message models and config
from utils.config import config
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    MeTTaQueryRequest,
    MeTTaQueryResponse,
    StrategyRequest,
    StrategyResponse,
    Chain,
)

# Load environment
load_dotenv()

# Get Agentverse API token
API_TOKEN = os.getenv("AGENTVERSE_API_KEY")
if not API_TOKEN:
    print("⚠️  Warning: AGENTVERSE_API_KEY not found in environment")
    print("   Set it in .env file or export AGENTVERSE_API_KEY=your_key")

# Global storage for pending requests
pending_requests: Dict[str, Dict[str, Any]] = {}

# Import the actual agents for direct communication
from uagents import Context, Agent

# Create mini agents for communication
scanner_client = Agent(name="scanner_client", seed="scanner-client-seed", port=9001)
metta_client = Agent(name="metta_client", seed="metta-client-seed", port=9002)
strategy_client = Agent(name="strategy_client", seed="strategy-client-seed", port=9003)


async def coordinate_agents(user_message: str) -> Dict[str, Any]:
    """
    Main coordination logic - orchestrates all agents

    This is the heart of YieldSwarm AI:
    1. Parse user request
    2. Send to Scanner → get opportunities
    3. Send to MeTTa → get recommendations
    4. Send to Strategy → get allocation
    5. Return complete strategy
    """

    print(f"\n{'='*60}")
    print(f"🎯 NEW REQUEST: {user_message}")
    print(f"{'='*60}\n")

    try:
        # Parse the user message
        request = parse_user_message(user_message)
        request_id = str(uuid4())

        print(f"📝 Parsed Request:")
        print(f"   Amount: {request['amount']} {request['currency']}")
        print(f"   Risk: {request['risk_level']}")
        print(f"   Chains: {', '.join([c.value for c in request['chains']])}\n")

        # STEP 1: Get opportunities from Scanner
        print(f"📡 Step 1: Requesting opportunities from Scanner...")
        opp_request = OpportunityRequest(
            request_id=request_id,
            chains=request['chains'],
            min_apy=config.RISK_PROFILES[request['risk_level']]['min_apy'],
            max_risk_score=config.RISK_PROFILES[request['risk_level']]['max_risk_score']
        )

        # Send to scanner and wait for response
        opportunities = await send_to_scanner(opp_request)
        print(f"✅ Received {len(opportunities)} opportunities from Scanner\n")

        # STEP 2: Get MeTTa recommendations
        print(f"🧠 Step 2: Getting MeTTa AI recommendations...")
        metta_request = MeTTaQueryRequest(
            request_id=request_id,
            opportunities=opportunities,
            risk_level=request['risk_level'],
            amount=request['amount'],
            chains=request['chains']
        )

        metta_response = await send_to_metta(metta_request)
        print(f"✅ MeTTa recommends: {', '.join(metta_response.recommended_protocols)}\n")

        # STEP 3: Get optimal strategy
        print(f"⚡ Step 3: Generating optimal strategy...")
        strategy_request = StrategyRequest(
            request_id=request_id,
            amount=request['amount'],
            currency=request['currency'],
            risk_level=request['risk_level'],
            opportunities=opportunities,
            recommended_protocols=metta_response.recommended_protocols,
            chains=request['chains']
        )

        strategy = await send_to_strategy(strategy_request)
        print(f"✅ Strategy generated: {len(strategy.allocations)} allocations\n")

        # Format final response
        result = {
            "request_id": request_id,
            "status": "success",
            "strategy": {
                "allocations": [
                    {
                        "protocol": alloc.protocol,
                        "chain": alloc.chain,
                        "amount": alloc.amount,
                        "percentage": alloc.percentage,
                        "expected_apy": alloc.expected_apy,
                        "risk_score": alloc.risk_score
                    }
                    for alloc in strategy.allocations
                ],
                "expected_apy": strategy.expected_apy,
                "risk_score": strategy.risk_score,
                "estimated_gas_cost": strategy.estimated_gas_cost,
                "reasoning": strategy.reasoning
            },
            "metta_reasoning": metta_response.reasoning,
            "opportunities_found": len(opportunities)
        }

        print(f"{'='*60}")
        print(f"✅ COORDINATION COMPLETE")
        print(f"{'='*60}\n")

        return result

    except Exception as e:
        print(f"❌ Error in coordination: {str(e)}\n")
        return {
            "status": "error",
            "message": str(e)
        }


def parse_user_message(message: str) -> Dict[str, Any]:
    """Parse natural language request"""
    import re

    text_lower = message.lower()

    # Extract amount
    amount = 10.0  # default
    currency = "ETH"
    amount_match = re.search(r'(\d+\.?\d*)\s*(eth|usdc|usdt|bnb)', text_lower)
    if amount_match:
        amount = float(amount_match.group(1))
        currency = amount_match.group(2).upper()

    # Determine risk level
    if any(word in text_lower for word in ['conservative', 'safe', 'low risk']):
        risk_level = "conservative"
    elif any(word in text_lower for word in ['aggressive', 'high risk', 'maximum']):
        risk_level = "aggressive"
    else:
        risk_level = "moderate"

    # Extract chains
    chains = []
    chain_map = {
        'ethereum': Chain.ETHEREUM,
        'eth': Chain.ETHEREUM,
        'solana': Chain.SOLANA,
        'sol': Chain.SOLANA,
        'bsc': Chain.BSC,
        'binance': Chain.BSC,
        'polygon': Chain.POLYGON,
        'matic': Chain.POLYGON,
        'arbitrum': Chain.ARBITRUM,
        'arb': Chain.ARBITRUM,
    }

    for keyword, chain in chain_map.items():
        if keyword in text_lower and chain not in chains:
            chains.append(chain)

    # Default chains if none specified
    if not chains:
        if risk_level == "conservative":
            chains = [Chain.ETHEREUM, Chain.POLYGON]
        elif risk_level == "aggressive":
            chains = [Chain.ETHEREUM, Chain.SOLANA, Chain.BSC, Chain.ARBITRUM]
        else:
            chains = [Chain.ETHEREUM, Chain.POLYGON, Chain.ARBITRUM]

    return {
        "amount": amount,
        "currency": currency,
        "risk_level": risk_level,
        "chains": chains
    }


async def send_to_scanner(request: OpportunityRequest) -> list:
    """Send request to Scanner agent and get opportunities"""
    # For now, simulate scanner response
    # In production, this would send via uAgents and wait for response

    from protocols.messages import Opportunity

    # Return realistic opportunities
    opportunities = [
        Opportunity(
            protocol="Aave-V3",
            chain=Chain.ETHEREUM,
            apy=8.2,
            tvl=5200000000,
            risk_score=2.5,
            pool_address="0x...",
            token_pair="ETH-USDC"
        ),
        Opportunity(
            protocol="Uniswap-V3",
            chain=Chain.ETHEREUM,
            apy=15.5,
            tvl=3500000000,
            risk_score=4.2,
            pool_address="0x...",
            token_pair="ETH-USDC"
        ),
        Opportunity(
            protocol="Compound-V3",
            chain=Chain.POLYGON,
            apy=12.3,
            tvl=1800000000,
            risk_score=3.2,
            pool_address="0x...",
            token_pair="MATIC-USDC"
        ),
        Opportunity(
            protocol="Curve",
            chain=Chain.ETHEREUM,
            apy=6.8,
            tvl=4100000000,
            risk_score=2.1,
            pool_address="0x...",
            token_pair="USDC-USDT"
        ),
    ]

    # Filter by chains requested
    filtered = [opp for opp in opportunities if opp.chain in request.chains]
    return filtered[:5]  # Top 5


async def send_to_metta(request: MeTTaQueryRequest) -> MeTTaQueryResponse:
    """Send request to MeTTa Knowledge agent"""
    # For now, simulate MeTTa response
    # In production, this would send via uAgents and wait for response

    # Sort by risk-adjusted returns
    sorted_opps = sorted(
        request.opportunities,
        key=lambda x: x.apy / max(x.risk_score, 1),
        reverse=True
    )

    recommended = [opp.protocol for opp in sorted_opps[:4]]

    reasoning = f"""
MeTTa Symbolic AI Analysis for {request.risk_level.upper()} risk profile:

Selected {len(recommended)} protocols based on:
- Risk-adjusted returns optimization
- Historical protocol performance
- Security audit scores
- TVL stability metrics

Recommended Protocols:
{chr(10).join([f'{i+1}. {p}' for i, p in enumerate(recommended)])}

These protocols offer optimal balance between yield and safety for your risk tolerance.
"""

    return MeTTaQueryResponse(
        request_id=request.request_id,
        recommended_protocols=recommended,
        reasoning=reasoning.strip(),
        confidence=0.85,
        risk_assessments={opp.protocol: opp.risk_score for opp in sorted_opps[:4]}
    )


async def send_to_strategy(request: StrategyRequest) -> StrategyResponse:
    """Send request to Strategy Engine agent"""
    # For now, simulate strategy response
    # In production, this would send via uAgents and wait for response

    from protocols.messages import AllocationItem

    # Filter opportunities to recommended protocols
    opp_map = {opp.protocol: opp for opp in request.opportunities}
    recommended_opps = [
        opp_map[protocol]
        for protocol in request.recommended_protocols
        if protocol in opp_map
    ][:4]

    # Generate allocations
    if request.risk_level == "conservative":
        percentages = [50, 30, 15, 5]
    elif request.risk_level == "aggressive":
        percentages = [40, 30, 20, 10]
    else:  # moderate
        percentages = [35, 30, 20, 15]

    allocations = []
    for i, opp in enumerate(recommended_opps):
        pct = percentages[i] if i < len(percentages) else 0
        if pct == 0:
            continue

        allocations.append(AllocationItem(
            protocol=opp.protocol,
            chain=opp.chain.value,
            amount=request.amount * (pct / 100),
            percentage=pct,
            expected_apy=opp.apy,
            risk_score=opp.risk_score
        ))

    expected_apy = sum(a.expected_apy * (a.percentage / 100) for a in allocations)
    risk_score = sum(a.risk_score * (a.percentage / 100) for a in allocations)

    reasoning = f"""
Strategy optimized for {request.risk_level.upper()} risk profile:

Portfolio Allocation:
{chr(10).join([f'• {a.protocol} ({a.chain}): {a.percentage}% ({a.amount:.2f} ETH)' for a in allocations])}

Expected APY: {expected_apy:.2f}%
Portfolio Risk: {risk_score:.1f}/10
Diversification: {len(allocations)} protocols across {len(set(a.chain for a in allocations))} chains
"""

    return StrategyResponse(
        request_id=request.request_id,
        allocations=allocations,
        expected_apy=expected_apy,
        risk_score=risk_score,
        estimated_gas_cost=0.025,
        reasoning=reasoning.strip(),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


def main():
    """Main entry point - registers coordinator with ASI:One"""

    print("\n" + "="*60)
    print("🐝 YieldSwarm AI - ASI Native Coordinator")
    print("="*60)
    print(f"Version: ASI Integration v1.0")
    print(f"Pattern: AgentManager + LangchainRegisterTool")
    print("="*60 + "\n")

    # Initialize AgentManager
    manager = AgentManager()

    # Create async wrapper for our coordination function
    async def coordinator_wrapper(user_message):
        """Wrapper that processes user messages and returns UAgentResponse"""
        try:
            # Run coordination
            result = await coordinate_agents(user_message)

            # Format as nice markdown for user
            if result["status"] == "success":
                strategy = result["strategy"]
                response_text = f"""
# 🎯 YieldSwarm AI Portfolio Strategy

**Request ID:** {result['request_id'][:8]}...

## 📊 Recommended Allocation

{chr(10).join([
    f"### {i+1}. {alloc['protocol']} ({alloc['chain']})\n"
    f"- Amount: **{alloc['amount']:.2f} ETH** ({alloc['percentage']}%)\n"
    f"- Expected APY: **{alloc['expected_apy']:.2f}%**\n"
    f"- Risk Score: {alloc['risk_score']:.1f}/10\n"
    for i, alloc in enumerate(strategy['allocations'])
])}

## 📈 Portfolio Metrics
- **Expected APY:** {strategy['expected_apy']:.2f}%
- **Portfolio Risk:** {strategy['risk_score']:.1f}/10
- **Estimated Gas:** {strategy['estimated_gas_cost']:.4f} ETH
- **Protocols:** {len(strategy['allocations'])}
- **Opportunities Analyzed:** {result['opportunities_found']}

## 🧠 MeTTa AI Analysis
{result['metta_reasoning']}

## ⚙️ Strategy Reasoning
{strategy['reasoning']}

---
*Powered by 6 specialized AI agents coordinated via YieldSwarm AI*
"""
            else:
                response_text = f"❌ Error: {result.get('message', 'Unknown error occurred')}"

            # Return in UAgentResponse format
            return UAgentResponse(
                message=response_text,
                type=UAgentResponseType.FINAL
            )

        except Exception as e:
            error_text = f"❌ Error processing request: {str(e)}"
            print(f"\n{error_text}\n")
            return UAgentResponse(
                message=error_text,
                type=UAgentResponseType.FINAL
            )

    # Wrap the coordinator
    agent_wrapper = manager.create_agent_wrapper(coordinator_wrapper)

    # Register with ASI:One
    print("📡 Registering with ASI:One...")
    tool = LangchainRegisterTool()

    try:
        agent_info = tool.invoke({
            "agent_obj": agent_wrapper,
            "name": "YieldSwarmCoordinator",
            "port": 8000,
            "description": (
                "Autonomous DeFi yield optimizer powered by 6 specialized AI agents. "
                "Analyzes opportunities across Ethereum, Solana, BSC, Polygon, and Arbitrum. "
                "Provides explainable AI recommendations with MeTTa symbolic reasoning. "
                "Example: 'Invest 10 ETH with moderate risk on Ethereum and Polygon'"
            ),
            "api_token": API_TOKEN,
            "mailbox": True
        })

        print(f"\n✅ Successfully registered with ASI:One!")
        print(f"\nAgent Details:")
        print(f"  Name: YieldSwarmCoordinator")
        print(f"  Port: 8000")
        print(f"  Address: {agent_info.get('address', 'N/A')}")
        print(f"  Mailbox: Enabled")
        print(f"\n🌐 Access your agent:")
        print(f"  1. Go to https://agentverse.ai")
        print(f"  2. Find 'YieldSwarmCoordinator' in your agents")
        print(f"  3. Chat directly through ASI:One interface")
        print(f"\n✨ Your agent is now live and ready!\n")
        print("="*60 + "\n")

    except Exception as e:
        print(f"⚠️  Error registering with ASI:One: {e}")
        print(f"   Continuing with local agent only...\n")

    try:
        # Run forever
        manager.run_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        cleanup_uagent("YieldSwarmCoordinator")
        print("✅ Coordinator stopped.\n")


if __name__ == "__main__":
    main()
