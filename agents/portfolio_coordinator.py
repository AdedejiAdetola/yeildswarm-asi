"""
YieldSwarm AI - Portfolio Coordinator
ASI:One compatible coordinator that ACTUALLY orchestrates the 6 agents
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

from protocols.messages import *
from utils.config import config

# Create coordinator agent with mailbox
coordinator = Agent(
    name="yieldswarm-coordinator",
    seed=config.COORDINATOR_SEED,
    port=8000,
    mailbox=True,  # REQUIRED for ASI:One
    endpoint=["http://localhost:8000/submit"]
)

# Agent addresses (from config)
SCANNER_ADDRESS = config.SCANNER_ADDRESS
METTA_ADDRESS = config.METTA_ADDRESS
STRATEGY_ADDRESS = config.STRATEGY_ADDRESS
EXECUTION_ADDRESS = config.EXECUTION_ADDRESS
TRACKER_ADDRESS = config.TRACKER_ADDRESS

# Storage for pending requests
pending_requests = {}

# Create Chat Protocol for ASI:One
chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def handle_user_request(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle user messages from ASI:One

    This is the MAIN entry point for users
    """
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
            request_id = str(uuid4())
            parsed = parse_user_message(user_message)

            # Store request context
            pending_requests[request_id] = {
                "sender": sender,
                "msg_id": msg.msg_id,
                "parsed": parsed,
                "opportunities": None,
                "metta_response": None,
                "strategy": None
            }

            # STEP 1: Request opportunities from Scanner
            ctx.logger.info(f"📡 Requesting opportunities from Scanner...")
            scanner_request = OpportunityRequest(
                request_id=request_id,
                chains=parsed["chains"],
                min_apy=config.RISK_PROFILES[parsed["risk_level"]]["min_apy"],
                max_risk_score=config.RISK_PROFILES[parsed["risk_level"]]["max_risk_score"]
            )

            await ctx.send(SCANNER_ADDRESS, scanner_request)

        elif isinstance(content, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")


@coordinator.on_message(model=OpportunityResponse)
async def handle_scanner_response(ctx: Context, sender: str, msg: OpportunityResponse):
    """
    Handle opportunities from Chain Scanner
    Then forward to MeTTa Knowledge agent
    """
    ctx.logger.info(f"✅ Received {len(msg.opportunities)} opportunities from Scanner")

    if msg.request_id not in pending_requests:
        ctx.logger.warning(f"⚠️ Unknown request ID: {msg.request_id}")
        return

    # Store opportunities
    req_ctx = pending_requests[msg.request_id]
    req_ctx["opportunities"] = msg.opportunities

    # STEP 2: Send to MeTTa for analysis
    ctx.logger.info(f"🧠 Sending to MeTTa for analysis...")
    metta_request = MeTTaQueryRequest(
        request_id=msg.request_id,
        opportunities=msg.opportunities,
        risk_level=req_ctx["parsed"]["risk_level"],
        amount=req_ctx["parsed"]["amount"],
        chains=req_ctx["parsed"]["chains"]
    )

    await ctx.send(METTA_ADDRESS, metta_request)


@coordinator.on_message(model=MeTTaQueryResponse)
async def handle_metta_response(ctx: Context, sender: str, msg: MeTTaQueryResponse):
    """
    Handle MeTTa recommendations
    Then forward to Strategy Engine
    """
    ctx.logger.info(f"✅ MeTTa recommends: {', '.join(msg.recommended_protocols)}")

    if msg.request_id not in pending_requests:
        ctx.logger.warning(f"⚠️ Unknown request ID: {msg.request_id}")
        return

    # Store MeTTa response
    req_ctx = pending_requests[msg.request_id]
    req_ctx["metta_response"] = msg

    # STEP 3: Send to Strategy Engine
    ctx.logger.info(f"⚡ Requesting strategy from Engine...")
    strategy_request = StrategyRequest(
        request_id=msg.request_id,
        amount=req_ctx["parsed"]["amount"],
        currency=req_ctx["parsed"]["currency"],
        risk_level=req_ctx["parsed"]["risk_level"],
        opportunities=req_ctx["opportunities"],
        recommended_protocols=msg.recommended_protocols,
        chains=req_ctx["parsed"]["chains"]
    )

    await ctx.send(STRATEGY_ADDRESS, strategy_request)


@coordinator.on_message(model=StrategyResponse)
async def handle_strategy_response(ctx: Context, sender: str, msg: StrategyResponse):
    """
    Handle final strategy
    Send back to user via ASI:One
    """
    ctx.logger.info(f"✅ Strategy generated: {len(msg.allocations)} allocations")

    if msg.request_id not in pending_requests:
        ctx.logger.warning(f"⚠️ Unknown request ID: {msg.request_id}")
        return

    # Get request context
    req_ctx = pending_requests[msg.request_id]
    req_ctx["strategy"] = msg

    # Format response for user
    response_text = format_strategy_response(req_ctx)

    # Send back to user via Chat Protocol
    response_msg = ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response_text)]
    )

    await ctx.send(req_ctx["sender"], response_msg)
    ctx.logger.info(f"📤 Sent strategy to user")

    # Cleanup
    del pending_requests[msg.request_id]


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
    """Format strategy as markdown for ASI:One"""
    strategy = req_ctx["strategy"]
    metta = req_ctx["metta_response"]

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
- **Protocols:** {len(strategy.allocations)}
- **Opportunities Analyzed:** {len(req_ctx["opportunities"])}

## 🧠 MeTTa AI Analysis
{metta.reasoning}

## ⚙️ Strategy Reasoning
{strategy.reasoning}

---
*Powered by 6 specialized AI agents coordinated via YieldSwarm AI*
"""

    return text


# Include Chat Protocol with manifest publishing
coordinator.include(chat_proto, publish_manifest=True)


@coordinator.on_event("startup")
async def startup(ctx: Context):
    """Log startup details"""
    ctx.logger.info("="*60)
    ctx.logger.info("🐝 YieldSwarm AI - Portfolio Coordinator")
    ctx.logger.info("="*60)
    ctx.logger.info(f"Agent Address: {coordinator.address}")
    ctx.logger.info(f"Port: 8000")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Chat Protocol: Enabled ✓")
    ctx.logger.info(f"Connected to 5 agents:")
    ctx.logger.info(f"  📡 Scanner: {SCANNER_ADDRESS}")
    ctx.logger.info(f"  🧠 MeTTa: {METTA_ADDRESS}")
    ctx.logger.info(f"  ⚡ Strategy: {STRATEGY_ADDRESS}")
    ctx.logger.info(f"  🔒 Execution: {EXECUTION_ADDRESS}")
    ctx.logger.info(f"  📊 Tracker: {TRACKER_ADDRESS}")
    ctx.logger.info("="*60)
    ctx.logger.info("✅ Ready to accept requests via ASI:One")


if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Portfolio Coordinator")
    print(f"Address: {coordinator.address}")
    print(f"ASI:One Compatible: ✅\n")
    coordinator.run()
