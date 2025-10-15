
"""
YieldSwarm AI - Portfolio Coordinator
ASI:One compatible coordinator - AGENTVERSE VERSION
IMPORTANT: Deploy OTHER AGENTS FIRST, then update their addresses below!
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    StartSessionContent,
    TextContent,
    EndSessionContent,
    chat_protocol_spec
)
from datetime import datetime, timezone
from uuid import uuid4
import re
import json
import base64
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from enum import Enum
from openai import OpenAI

# ===== INLINE MESSAGE MODELS =====
class RiskLevel(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

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
COORDINATOR_SEED = "coordinator-dev-seed-yieldswarm"

# ASI:One API Configuration
# NOTE: In Agentverse, add this as environment variable: ASI_ONE_API_KEY
ASI_ONE_API_KEY = "sk_784c488384e043f38c0ae5c0e69b12d689b15089c11347b38384a1a8d5934d0c"

# Configure OpenAI client with ASI:One endpoint
asi_client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key=ASI_ONE_API_KEY,
)

# TODO: REPLACE THESE WITH YOUR ACTUAL DEPLOYED AGENT ADDRESSES!
SCANNER_ADDRESS = "agent1qtn2hgpdfl0he2h88xncvrdvyk5vd9xtsruw9vzua8tgnejtxxpzy8suu8r"  # Chain Scanner
METTA_ADDRESS = "agent1qflfh899d98vw3337neylwjkfvc4exx6frsj6vqnaeq0ujwjf6ggcczc5y0"  # MeTTa Knowledge
STRATEGY_ADDRESS = "agent1qwqr4489ww7kplx456w5tpj4548s743wvp7ly3qjd6aurgp04cf4zswgyal"  # Strategy Engine

RISK_PROFILES = {
    "conservative": {"max_risk_score": 2.0, "min_apy": 2.0},
    "moderate": {"max_risk_score": 5.0, "min_apy": 4.0},
    "aggressive": {"max_risk_score": 8.0, "min_apy": 8.0},
}

# ===== AGENT INITIALIZATION =====
try:
    coordinator = agent  # type: ignore
except NameError:
    coordinator = Agent(
        name="yieldswarm-coordinator",
        seed=COORDINATOR_SEED,
        port=8000,
        mailbox=True
        # NOTE: No endpoint for Agentverse deployment
        # Agentverse will automatically configure the endpoint
    )

# NOTE: Agentverse is STATELESS - agent instances are recreated for each handler
# Solution: Encode all context in request_id as base64 JSON

# Create chat protocol for ASI:One compatibility
chat_protocol = Protocol(spec=chat_protocol_spec)

@chat_protocol.on_message(ChatMessage)
async def handle_user_request(ctx: Context, sender: str, msg: ChatMessage):
    """Handle user messages from ASI:One"""
    ctx.logger.info(f"📩 Received message from {sender}")

    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Process message content
    for content in msg.content:
        if isinstance(content, StartSessionContent):
            ctx.logger.info(f"🟢 Session started with {sender}")

        elif isinstance(content, TextContent):
            user_message = content.text
            ctx.logger.info(f"💬 User message: {user_message}")

            # Parse the request
            parsed = parse_user_message(user_message)

            # STATELESS APPROACH: Encode context in request_id as base64 JSON
            context = {
                "uid": str(uuid4())[:8],
                "sender": sender,
                "msg_id": str(msg.msg_id),
                "amount": parsed["amount"],
                "currency": parsed["currency"],
                "risk_level": parsed["risk_level"],
                "chains": [c.value for c in parsed["chains"]]
            }
            request_id = base64.b64encode(json.dumps(context).encode()).decode()

            ctx.logger.info(f"📝 Request with context encoded")
            ctx.logger.info(f"   Sender: {sender}")
            ctx.logger.info(f"   Amount: {parsed['amount']} {parsed['currency']}")
            ctx.logger.info(f"   Risk: {parsed['risk_level']}")

            # STEP 1: Request opportunities from Scanner
            ctx.logger.info(f"📡 Requesting opportunities from Scanner...")
            scanner_request = OpportunityRequest(
                request_id=request_id,
                chains=parsed["chains"],
                min_apy=RISK_PROFILES[parsed["risk_level"]]["min_apy"],
                max_risk_score=RISK_PROFILES[parsed["risk_level"]]["max_risk_score"]
            )

            await ctx.send(SCANNER_ADDRESS, scanner_request)

        elif isinstance(content, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements from users"""
    ctx.logger.info(f"✅ Message acknowledged by {sender}")

@coordinator.on_message(model=OpportunityResponse)
async def handle_scanner_response(ctx: Context, sender: str, msg: OpportunityResponse):
    """Handle opportunities from Chain Scanner - STATELESS"""
    ctx.logger.info(f"✅ Received {len(msg.opportunities)} opportunities from Scanner")

    # Decode context from request_id
    try:
        context = json.loads(base64.b64decode(msg.request_id).decode())
        ctx.logger.info(f"📖 Decoded context: sender={context['sender'][:20]}..., risk={context['risk_level']}")
    except:
        ctx.logger.error(f"❌ Failed to decode context from request_id")
        return

    # STEP 2: Send to MeTTa for analysis
    ctx.logger.info(f"🧠 Sending to MeTTa for analysis...")
    metta_request = MeTTaQueryRequest(
        request_id=msg.request_id,
        opportunities=msg.opportunities,
        risk_level=context["risk_level"],
        amount=context["amount"],
        chains=[Chain(c) for c in context["chains"]]
    )

    await ctx.send(METTA_ADDRESS, metta_request)
    ctx.logger.info(f"✅ MeTTa request sent successfully")

@coordinator.on_message(model=MeTTaQueryResponse)
async def handle_metta_response(ctx: Context, sender: str, msg: MeTTaQueryResponse):
    """Handle MeTTa recommendations - STATELESS"""
    try:
        ctx.logger.info(f"✅ MeTTa recommends: {', '.join(msg.recommended_protocols)}")

        # Decode context from request_id
        try:
            context = json.loads(base64.b64decode(msg.request_id).decode())
            ctx.logger.info(f"📖 Decoded context from MeTTa response")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to decode context: {str(e)}")
            return

        # STEP 3: Send to Strategy Engine
        ctx.logger.info(f"⚡ Requesting strategy from Engine...")

        # Need to get opportunities from somewhere - they're in the MeTTaQueryRequest that was sent
        # For now, use empty list and let Strategy work with recommended protocols
        strategy_request = StrategyRequest(
            request_id=msg.request_id,
            amount=context["amount"],
            currency=context["currency"],
            risk_level=context["risk_level"],
            opportunities=[],  # Strategy will need to handle this
            recommended_protocols=msg.recommended_protocols,
            chains=[Chain(c) for c in context["chains"]]
        )

        await ctx.send(STRATEGY_ADDRESS, strategy_request)
        ctx.logger.info(f"✅ Strategy request sent")
    except Exception as e:
        ctx.logger.error(f"❌ Error in handle_metta_response: {str(e)}")

@coordinator.on_message(model=StrategyResponse)
async def handle_strategy_response(ctx: Context, sender: str, msg: StrategyResponse):
    """Handle final strategy and send back to user - STATELESS"""
    ctx.logger.info(f"✅ Strategy generated: {len(msg.allocations)} allocations")

    # Decode context from request_id
    try:
        context = json.loads(base64.b64decode(msg.request_id).decode())
        user_sender = context["sender"]
        ctx.logger.info(f"📖 Decoded sender: {user_sender[:20]}...")
    except:
        ctx.logger.error(f"❌ Failed to decode context from request_id")
        return

    # Create simple response text
    text = f"""# 🎯 YieldSwarm AI Portfolio Strategy

## 📊 Recommended Allocation

"""
    for i, alloc in enumerate(msg.allocations, 1):
        text += f"""### {i}. {alloc.protocol} ({alloc.chain})
- Amount: **{alloc.amount:.2f} ETH** ({alloc.percentage}%)
- Expected APY: **{alloc.expected_apy:.2f}%**
- Risk Score: {alloc.risk_score:.1f}/10

"""

    text += f"""## 📈 Portfolio Metrics
- **Expected APY:** {msg.expected_apy:.2f}%
- **Portfolio Risk:** {msg.risk_score:.1f}/10
- **Estimated Gas:** {msg.estimated_gas_cost:.4f} ETH

## ⚙️ Strategy Reasoning
{msg.reasoning}

---
*Powered by 6 specialized AI agents via YieldSwarm AI 🐝*"""

    # Send back to user via Chat Protocol
    response_msg = ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)]
    )

    await ctx.send(user_sender, response_msg)
    ctx.logger.info(f"📤 Sent strategy to user")

def parse_user_message(text: str) -> dict:
    """Parse natural language investment request"""
    text_lower = text.lower()

    # Extract amount
    amount = 10.0
    currency = "ETH"
    amount_match = re.search(r'(\d+\.?\d*)\s*(eth|usdc|usdt|bnb)', text_lower)
    if amount_match:
        amount = float(amount_match.group(1))
        currency = amount_match.group(2).upper()

    # Extract risk level
    if any(w in text_lower for w in ['conservative', 'safe', 'low risk']):
        risk_level = "conservative"
    elif any(w in text_lower for w in ['aggressive', 'high risk', 'maximum']):
        risk_level = "aggressive"
    else:
        risk_level = "moderate"

    # Extract chains
    chains = []
    chain_map = {
        'ethereum': Chain.ETHEREUM, 'eth': Chain.ETHEREUM,
        'solana': Chain.SOLANA, 'sol': Chain.SOLANA,
        'bsc': Chain.BSC, 'binance': Chain.BSC,
        'polygon': Chain.POLYGON, 'matic': Chain.POLYGON,
        'arbitrum': Chain.ARBITRUM, 'arb': Chain.ARBITRUM,
    }

    for keyword, chain in chain_map.items():
        if keyword in text_lower and chain not in chains:
            chains.append(chain)

    if not chains:
        chains = [Chain.ETHEREUM, Chain.POLYGON]

    return {
        "amount": amount,
        "currency": currency,
        "risk_level": risk_level,
        "chains": chains
    }

def format_strategy_response(req_ctx: dict) -> str:
    """Generate intelligent, conversational response using ASI:One LLM"""
    strategy = req_ctx["strategy"]
    metta = req_ctx["metta_response"]
    parsed = req_ctx["parsed"]

    # Prepare structured data for LLM
    strategy_data = {
        "user_request": {
            "amount": parsed["amount"],
            "currency": parsed["currency"],
            "risk_level": parsed["risk_level"],
            "chains": [c.value for c in parsed["chains"]]
        },
        "allocations": [
            {
                "protocol": alloc.protocol,
                "chain": alloc.chain,
                "amount": alloc.amount,
                "percentage": alloc.percentage,
                "apy": alloc.expected_apy,
                "risk_score": alloc.risk_score
            }
            for alloc in strategy.allocations
        ],
        "portfolio_metrics": {
            "expected_apy": strategy.expected_apy,
            "risk_score": strategy.risk_score,
            "gas_cost": strategy.estimated_gas_cost,
            "opportunities_analyzed": len(req_ctx["opportunities"])
        },
        "metta_analysis": {
            "recommended_protocols": metta.recommended_protocols,
            "reasoning": metta.reasoning,
            "confidence": metta.confidence
        },
        "strategy_reasoning": strategy.reasoning
    }

    # System prompt defines agent's personality and expertise
    system_prompt = """You are YieldSwarm AI, an expert DeFi portfolio advisor powered by 6 specialized AI agents.

Your expertise:
- Deep knowledge of 50+ DeFi protocols across Ethereum, Polygon, Solana, BSC, Arbitrum
- Risk assessment and portfolio optimization
- Real-time yield analysis and market conditions
- MeTTa symbolic reasoning for protocol safety

Your communication style:
- Professional yet conversational and friendly
- Explain complex DeFi concepts simply
- Provide clear reasoning for recommendations
- Highlight both opportunities and risks
- Use markdown formatting for readability
- Always invite follow-up questions

Task: Present the portfolio strategy in a natural, engaging way that helps the user understand WHY these choices were made, not just WHAT the choices are."""

    user_prompt = f"""Generate a conversational response presenting this DeFi portfolio strategy. Make it engaging, educational, and actionable.

Strategy Data:
{json.dumps(strategy_data, indent=2)}"""

    try:
        # Call ASI:One LLM
        response = asi_client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2048,
        )

        llm_response = response.choices[0].message.content

        # Add attribution footer
        footer = "\n\n---\n*Powered by 6 specialized AI agents coordinated via YieldSwarm AI 🐝*"

        return llm_response + footer

    except Exception as e:
        # Fallback to template if LLM fails
        text = f"""# 🎯 YieldSwarm AI Portfolio Strategy

## 📊 Recommended Allocation

"""
        for i, alloc in enumerate(strategy.allocations, 1):
            text += f"""### {i}. {alloc.protocol} ({alloc.chain})
- Amount: **{alloc.amount:.2f} ETH** ({alloc.percentage}%)
- Expected APY: **{alloc.expected_apy:.2f}%**
- Risk Score: {alloc.risk_score:.1f}/10

"""

        text += f"""## 📈 Portfolio Metrics
- **Expected APY:** {strategy.expected_apy:.2f}%
- **Portfolio Risk:** {strategy.risk_score:.1f}/10
- **Estimated Gas:** {strategy.estimated_gas_cost:.4f} ETH

## 🧠 MeTTa AI Analysis
{metta.reasoning}

## ⚙️ Strategy Reasoning
{strategy.reasoning}

---
*Powered by 6 specialized AI agents via YieldSwarm AI*
*(Note: LLM enhancement temporarily unavailable)*"""

        return text

# Include chat protocol with manifest publishing for ASI:One compatibility
coordinator.include(chat_protocol, publish_manifest=True)

@coordinator.on_event("startup")
async def startup(ctx: Context):
    """Log startup details"""
    ctx.logger.info("="*60)
    ctx.logger.info("🐝 YieldSwarm AI - Portfolio Coordinator")
    ctx.logger.info("="*60)
    ctx.logger.info(f"Agent Address: {coordinator.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Chat Protocol: Enabled ✓")
    ctx.logger.info(f"Connected agents:")
    ctx.logger.info(f"  📡 Scanner: {SCANNER_ADDRESS}")
    ctx.logger.info(f"  🧠 MeTTa: {METTA_ADDRESS}")
    ctx.logger.info(f"  ⚡ Strategy: {STRATEGY_ADDRESS}")
    ctx.logger.info("="*60)
    ctx.logger.info("✅ Ready for ASI:One requests")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Portfolio Coordinator")
    print(f"Address: {coordinator.address}")
    print(f"ASI:One Compatible: ✅\n")
    coordinator.run()
