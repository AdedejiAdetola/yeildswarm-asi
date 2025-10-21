
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
from typing import List, Optional, Any, Dict
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
    risk_assessments: Optional[Dict[str, float]] = None

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
COORDINATOR_SEED = process.env.COORDINATOR_SEED

# ASI:One API Configuration
# NOTE: In Agentverse, add this as environment variable: ASI_ONE_API_KEY
ASI_ONE_API_KEY = process.env.ASI_ONE_API_KEY

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

            # Validate input first
            validation_result = validate_user_input(user_message)
            if not validation_result["valid"]:
                # Send helpful guidance message
                guidance_msg = ChatMessage(
                    timestamp=datetime.now(timezone.utc),
                    msg_id=uuid4(),
                    content=[TextContent(type="text", text=validation_result["message"])]
                )
                await ctx.send(sender, guidance_msg)
                ctx.logger.info(f"⚠️ Invalid input detected, sent guidance")
                return

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

    # Store opportunities in context for later use
    context["opportunities"] = [opp.model_dump() for opp in msg.opportunities]

    # Re-encode context with opportunities
    updated_request_id = base64.b64encode(json.dumps(context).encode()).decode()

    # STEP 2: Send to MeTTa for analysis
    ctx.logger.info(f"🧠 Sending to MeTTa for analysis...")
    metta_request = MeTTaQueryRequest(
        request_id=updated_request_id,
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

        # Reconstruct opportunities from context
        opportunities = []
        if "opportunities" in context:
            for opp_dict in context["opportunities"]:
                opportunities.append(Opportunity(**opp_dict))

        ctx.logger.info(f"📊 Sending {len(opportunities)} opportunities to Strategy Engine")

        strategy_request = StrategyRequest(
            request_id=msg.request_id,
            amount=context["amount"],
            currency=context["currency"],
            risk_level=context["risk_level"],
            opportunities=opportunities,
            recommended_protocols=msg.recommended_protocols,
            chains=[Chain(c) for c in context["chains"]]
        )

        await ctx.send(STRATEGY_ADDRESS, strategy_request)
        ctx.logger.info(f"✅ Strategy request sent to {STRATEGY_ADDRESS}")
    except Exception as e:
        ctx.logger.error(f"❌ Error in handle_metta_response: {str(e)}")
        import traceback
        ctx.logger.error(f"Traceback: {traceback.format_exc()}")

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

def validate_user_input(text: str) -> dict:
    """
    Validate user input before processing

    Returns:
        dict with 'valid' (bool) and 'message' (str) keys
    """
    text_lower = text.lower().strip()

    # Empty or too short
    if len(text_lower) < 3:
        return {
            "valid": False,
            "message": """👋 Hello! I'm YieldSwarm AI, your DeFi portfolio optimizer.

I can help you create optimized yield strategies across multiple chains.

**How to use me:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH on Ethereum with conservative risk"
• "Invest 20 ETH with aggressive risk on Polygon"

**Risk levels:** conservative, moderate, aggressive
**Supported chains:** Ethereum, Polygon, Solana, BSC, Arbitrum

What would you like to invest?"""
        }

    # Common greetings and casual inputs
    greetings = ['hi', 'hello', 'hey', 'greetings', 'howdy', 'sup', 'yo']
    if any(text_lower.startswith(g) for g in greetings) or text_lower in greetings:
        return {
            "valid": False,
            "message": """👋 Hello! Great to meet you!

I'm YieldSwarm AI - I help optimize DeFi portfolios using 6 specialized AI agents.

**Try these commands:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH with conservative risk on Ethereum"
• "Invest 50 ETH with aggressive risk"

Ready to optimize your yield? Tell me how much you'd like to invest!"""
        }

    # Help requests
    help_keywords = ['help', 'how', 'what can you', 'guide', 'instructions', 'commands', '?']
    if any(keyword in text_lower for keyword in help_keywords) and 'invest' not in text_lower:
        return {
            "valid": False,
            "message": """📚 **YieldSwarm AI - Usage Guide**

I analyze 50+ DeFi protocols across 5 chains and create optimized portfolio strategies.

**Basic Format:**
"Invest [AMOUNT] [CURRENCY] with [RISK LEVEL]"

**Examples:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH with conservative risk on Ethereum"
• "Invest 20 USDC with aggressive risk"
• "Invest 15 ETH on Polygon with low risk"

**Parameters:**
• **Amount:** Any number (e.g., 1, 10, 50)
• **Currency:** ETH, USDC, USDT, BNB
• **Risk Level:**
  - Conservative: Low risk, stable yields (2-6% APY)
  - Moderate: Balanced risk/reward (4-12% APY)
  - Aggressive: High risk, maximum yields (8-20% APY)
• **Chains (optional):** Ethereum, Polygon, Solana, BSC, Arbitrum

**What I do:**
1. Scan opportunities across all chains
2. Use MeTTa AI for symbolic reasoning
3. Generate optimized allocation strategy
4. Provide gas-efficient execution plan

Ready to start? Tell me your investment parameters!"""
        }

    # Random gibberish (no investment-related keywords)
    investment_keywords = ['invest', 'eth', 'usdc', 'usdt', 'bnb', 'defi', 'yield', 'apy',
                          'stake', 'farm', 'pool', 'protocol', 'risk', 'portfolio',
                          'strategy', 'allocat', 'ethereum', 'polygon', 'solana', 'bsc', 'arbitrum']

    has_investment_keyword = any(keyword in text_lower for keyword in investment_keywords)

    # Check if text has numbers (amount indication)
    has_number = any(char.isdigit() for char in text)

    if not has_investment_keyword and not has_number:
        return {
            "valid": False,
            "message": """🤔 I didn't quite understand that.

I'm specialized in DeFi portfolio optimization. Here's how to use me:

**Example requests:**
• "Invest 10 ETH with moderate risk"
• "Invest 5 ETH with conservative risk"
• "Invest 20 ETH with aggressive risk on Polygon"

**Need help?** Just ask: "How do I use this?" or "Show me examples"

What would you like to invest?"""
        }

    # Looks like a valid investment request
    return {"valid": True, "message": ""}


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
        footer = "\n\n---\n*Powered by 4 specialized AI agents coordinated via YieldSwarm AI 🐝*"

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
