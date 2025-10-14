"""
YieldSwarm AI - Portfolio Coordinator Agent (Clean Implementation)
Orchestrates multi-agent swarm for DeFi yield optimization

Following winning project patterns:
- AgentFlow: Chat Protocol with datetime.now(timezone.utc)
- TravelBud: Async agent coordination
- FinWell: Multiple message handlers for orchestration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    StartSessionContent,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)
from datetime import datetime, timezone
from uuid import uuid4
from utils.config import config
from utils.models import InvestmentRequest, RiskLevel, Chain
from protocols.messages import (
    OpportunityRequest,
    OpportunityResponse,
    MeTTaQueryRequest,
    MeTTaQueryResponse,
    StrategyRequest,
    StrategyResponse,
)
import re
from typing import Dict, Any

# ===== AGENT INITIALIZATION =====
# Pattern from FinWell and AgentFlow

coordinator = Agent(
    name="yieldswarm-coordinator",
    seed=config.COORDINATOR_SEED,
    port=config.COORDINATOR_PORT,
    mailbox=True,  # Enable Agentverse (REQUIRED)
    endpoint=[f"http://localhost:{config.COORDINATOR_PORT}/submit"],
)

# Initialize chat protocol for ASI:One compatibility
chat_proto = Protocol(spec=chat_protocol_spec)

# Store user sessions and pending requests
user_sessions: Dict[str, Dict[str, Any]] = {}
pending_requests: Dict[str, Dict[str, Any]] = {}


# ===== HELPER FUNCTIONS =====

def create_text_chat(text: str) -> ChatMessage:
    """Create a chat message with text content"""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),  # Correct pattern from AgentFlow
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )


def parse_investment_request(text: str, user_id: str) -> InvestmentRequest:
    """Parse natural language investment request"""
    text_lower = text.lower()

    # Extract amount
    amount = 10.0  # default
    amount_match = re.search(r'(\d+\.?\d*)\s*(eth|usdc|usdt|bnb)', text_lower)
    if amount_match:
        amount = float(amount_match.group(1))
        currency = amount_match.group(2).upper()
    else:
        currency = "ETH"

    # Determine risk level
    if any(word in text_lower for word in ['conservative', 'safe', 'low risk']):
        risk_level = RiskLevel.CONSERVATIVE
    elif any(word in text_lower for word in ['aggressive', 'high risk', 'maximum']):
        risk_level = RiskLevel.AGGRESSIVE
    else:
        risk_level = RiskLevel.MODERATE

    # Extract preferred chains
    preferred_chains = []
    chain_keywords = {
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

    for keyword, chain in chain_keywords.items():
        if keyword in text_lower and chain not in preferred_chains:
            preferred_chains.append(chain)

    # If no chains specified, use defaults based on risk
    if not preferred_chains:
        if risk_level == RiskLevel.CONSERVATIVE:
            preferred_chains = [Chain.ETHEREUM, Chain.POLYGON]
        elif risk_level == RiskLevel.AGGRESSIVE:
            preferred_chains = [Chain.ETHEREUM, Chain.SOLANA, Chain.BSC, Chain.ARBITRUM]
        else:
            preferred_chains = [Chain.ETHEREUM, Chain.POLYGON, Chain.ARBITRUM]

    return InvestmentRequest(
        user_id=user_id,
        amount=amount,
        currency=currency,
        risk_level=risk_level,
        preferred_chains=preferred_chains,
    )


# ===== CHAT PROTOCOL HANDLERS (ASI:One) =====
# Pattern from official Chat Protocol documentation

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle incoming chat messages from ASI:One or other users
    Pattern from AgentFlow intent_classifier_agent.py
    """
    ctx.logger.info(f"📩 Received chat message from {sender}")

    # REQUIRED: Always acknowledge (from official docs)
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Process message content
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"🟢 Session started with {sender}")
            user_sessions[sender] = {
                "started_at": datetime.now(timezone.utc),
                "requests": []
            }

            welcome_msg = create_text_chat(
                "👋 Welcome to YieldSwarm AI!\n\n"
                "I'm your autonomous DeFi yield optimizer powered by a swarm of 6 specialized AI agents.\n\n"
                "Tell me:\n"
                "• How much you want to invest (e.g., '10 ETH')\n"
                "• Your risk tolerance (conservative/moderate/aggressive)\n"
                "• Preferred chains (optional)\n\n"
                "Example: 'Invest 5 ETH with moderate risk on Ethereum and Polygon'"
            )
            await ctx.send(sender, welcome_msg)

        elif isinstance(item, TextContent):
            ctx.logger.info(f"💬 Processing request: {item.text}")

            # Check for help requests
            if any(word in item.text.lower() for word in ['help', 'how', 'what can']):
                help_msg = create_text_chat(
                    "🤖 YieldSwarm AI Commands:\n\n"
                    "Investment: 'Invest [amount] [currency] with [risk] risk'\n"
                    "Portfolio: 'Show my portfolio' or 'Check performance'\n"
                    "Strategy: 'What's the best strategy for...'\n\n"
                    "Risk Levels: conservative, moderate, aggressive\n"
                    "Chains: Ethereum, Solana, BSC, Polygon, Arbitrum\n\n"
                    "My 6 agents:\n"
                    "• Chain Scanner: 24/7 multi-chain monitoring\n"
                    "• MeTTa Knowledge: DeFi protocol intelligence\n"
                    "• Strategy Engine: Optimal allocation calculator\n"
                    "• Execution Agent: Safe transaction execution\n"
                    "• Performance Tracker: Real-time analytics"
                )
                await ctx.send(sender, help_msg)
                continue

            # Check for portfolio status requests
            if any(word in item.text.lower() for word in ['portfolio', 'performance', 'status', 'balance']):
                status_msg = create_text_chat(
                    "📊 Portfolio Status:\n\n"
                    "Connecting to Performance Tracker Agent...\n\n"
                    "Once fully deployed, I'll show:\n"
                    "• Total Value\n"
                    "• Active Positions\n"
                    "• Realized APY\n"
                    "• P&L (24h, 7d, 30d)\n"
                    "• Gas Costs"
                )
                await ctx.send(sender, status_msg)
                continue

            # Parse investment request
            try:
                investment_req = parse_investment_request(item.text, sender)

                # Store in session
                if sender in user_sessions:
                    user_sessions[sender]["requests"].append(investment_req)

                # Create unique request ID
                request_id = str(uuid4())

                # Store pending request for tracking responses
                pending_requests[request_id] = {
                    "user": sender,
                    "investment_req": investment_req,
                    "scanner_response": None,
                    "metta_response": None,
                    "strategy_response": None,
                    "timestamp": datetime.now(timezone.utc)
                }

                # Send initial acknowledgment
                initial_response = create_text_chat(
                    f"✅ Investment Request Received!\n\n"
                    f"Amount: {investment_req.amount} {investment_req.currency}\n"
                    f"Risk Level: {investment_req.risk_level.value}\n"
                    f"Chains: {', '.join([c.value for c in investment_req.preferred_chains])}\n\n"
                    f"🔄 Coordinating my agent swarm:\n"
                    f"1. 📡 Chain Scanner - Scanning {len(investment_req.preferred_chains)} chains...\n"
                    f"2. 🧠 MeTTa Knowledge - Will analyze protocols...\n"
                    f"3. ⚙️  Strategy Engine - Will optimize allocation...\n\n"
                    f"Request ID: {request_id[:8]}..."
                )
                await ctx.send(sender, initial_response)

                # === STEP 1: Request opportunities from Chain Scanner ===
                opp_request = OpportunityRequest(
                    request_id=request_id,
                    chains=investment_req.preferred_chains,
                    min_apy=config.RISK_PROFILES[investment_req.risk_level.value]['min_apy'],
                    max_risk_score=config.RISK_PROFILES[investment_req.risk_level.value]['max_risk_score']
                )

                ctx.logger.info(f"📤 Sending opportunity request to Scanner: {config.SCANNER_ADDRESS}")
                await ctx.send(config.SCANNER_ADDRESS, opp_request)

                # Send progress update
                progress_msg = create_text_chat(
                    f"✓ Request sent to Chain Scanner\n"
                    f"  Scanning {len(investment_req.preferred_chains)} chains for opportunities...\n"
                    f"  Looking for APY ≥ {config.RISK_PROFILES[investment_req.risk_level.value]['min_apy']}%\n\n"
                    f"⏳ Waiting for Scanner response..."
                )
                await ctx.send(sender, progress_msg)

                ctx.logger.info(f"✅ Investment request {request_id} initiated for user {sender}")

            except Exception as e:
                ctx.logger.error(f"❌ Error processing investment request: {str(e)}")
                error_msg = create_text_chat(
                    f"❌ Error processing request: {str(e)}\n\n"
                    f"Please try: 'Invest 10 ETH with moderate risk'"
                )
                await ctx.send(sender, error_msg)

        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")
            if sender in user_sessions:
                del user_sessions[sender]

            goodbye_msg = create_text_chat(
                "👋 Thanks for using YieldSwarm AI!\n\n"
                "Your autonomous DeFi yield optimizer is always here when you need it."
            )
            await ctx.send(sender, goodbye_msg)

        else:
            ctx.logger.info(f"⚠️  Received unexpected content type from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"✓ ACK from {sender} for message {msg.acknowledged_msg_id}")


# ===== AGENT MESSAGE HANDLERS (Inter-agent Communication) =====

@coordinator.on_message(model=OpportunityResponse)
async def handle_scanner_response(ctx: Context, sender: str, msg: OpportunityResponse):
    """
    Handle response from Chain Scanner Agent
    Pattern from TravelBud: Sequential agent coordination
    """
    ctx.logger.info(f"📩 Received OpportunityResponse from Scanner")
    ctx.logger.info(f"   Request ID: {msg.request_id}")
    ctx.logger.info(f"   Opportunities: {len(msg.opportunities)}")
    ctx.logger.info(f"   Chains Scanned: {[c.value for c in msg.chains_scanned]}")

    # Find the pending request
    if msg.request_id not in pending_requests:
        ctx.logger.error(f"❌ Unknown request ID: {msg.request_id}")
        return

    pending_req = pending_requests[msg.request_id]
    pending_req["scanner_response"] = msg

    user = pending_req["user"]
    investment_req = pending_req["investment_req"]

    # Send update to user
    update_msg = create_text_chat(
        f"✅ Chain Scanner Complete!\n\n"
        f"Found {len(msg.opportunities)} opportunities across {len(msg.chains_scanned)} chains\n\n"
        f"Top 3 Opportunities:\n"
        + "\n".join([
            f"• {opp.protocol} ({opp.chain.value}): {opp.apy}% APY, Risk: {opp.risk_score}/10"
            for opp in msg.opportunities[:3]
        ])
        + f"\n\n🧠 Sending to MeTTa Knowledge Agent for analysis..."
    )
    await ctx.send(user, update_msg)

    # === STEP 2: Send to MeTTa Knowledge Agent ===
    metta_request = MeTTaQueryRequest(
        request_id=msg.request_id,
        opportunities=msg.opportunities,
        risk_level=investment_req.risk_level.value,
        amount=investment_req.amount,
        chains=investment_req.preferred_chains
    )

    ctx.logger.info(f"📤 Sending MeTTa query for request {msg.request_id}")
    await ctx.send(config.METTA_ADDRESS, metta_request)


@coordinator.on_message(model=MeTTaQueryResponse)
async def handle_metta_response(ctx: Context, sender: str, msg: MeTTaQueryResponse):
    """
    Handle response from MeTTa Knowledge Agent
    Pattern from AgentFlow: Sequential routing
    """
    ctx.logger.info(f"📩 Received MeTTaQueryResponse")
    ctx.logger.info(f"   Request ID: {msg.request_id}")
    ctx.logger.info(f"   Recommended Protocols: {len(msg.recommended_protocols)}")

    # Find the pending request
    if msg.request_id not in pending_requests:
        ctx.logger.error(f"❌ Unknown request ID: {msg.request_id}")
        return

    pending_req = pending_requests[msg.request_id]
    pending_req["metta_response"] = msg

    user = pending_req["user"]
    investment_req = pending_req["investment_req"]
    scanner_resp = pending_req["scanner_response"]

    # Send update to user
    update_msg = create_text_chat(
        f"✅ MeTTa Knowledge Analysis Complete!\n\n"
        f"Recommended: {', '.join(msg.recommended_protocols)}\n"
        f"Reasoning: {msg.reasoning}\n\n"
        f"⚙️  Sending to Strategy Engine for optimization..."
    )
    await ctx.send(user, update_msg)

    # === STEP 3: Send to Strategy Engine ===
    strategy_request = StrategyRequest(
        request_id=msg.request_id,
        amount=investment_req.amount,
        currency=investment_req.currency,
        risk_level=investment_req.risk_level.value,
        opportunities=scanner_resp.opportunities,
        recommended_protocols=msg.recommended_protocols,
        chains=investment_req.preferred_chains
    )

    ctx.logger.info(f"📤 Sending Strategy request for {msg.request_id}")
    await ctx.send(config.STRATEGY_ADDRESS, strategy_request)


@coordinator.on_message(model=StrategyResponse)
async def handle_strategy_response(ctx: Context, sender: str, msg: StrategyResponse):
    """
    Handle response from Strategy Engine Agent
    Final step - send results to user
    """
    ctx.logger.info(f"📩 Received StrategyResponse")
    ctx.logger.info(f"   Request ID: {msg.request_id}")
    ctx.logger.info(f"   Allocations: {len(msg.allocations)}")
    ctx.logger.info(f"   Expected APY: {msg.expected_apy}%")

    # Find the pending request
    if msg.request_id not in pending_requests:
        ctx.logger.error(f"❌ Unknown request ID: {msg.request_id}")
        return

    pending_req = pending_requests[msg.request_id]
    pending_req["strategy_response"] = msg

    user = pending_req["user"]

    # Format final response
    allocation_text = "\n".join([
        f"• {alloc.protocol} ({alloc.chain}): {alloc.percentage}% ({alloc.amount} ETH) @ {alloc.expected_apy}% APY"
        for alloc in msg.allocations
    ])

    final_msg = create_text_chat(
        f"✅ Optimal Strategy Generated!\n\n"
        f"📊 Portfolio Allocation:\n{allocation_text}\n\n"
        f"Expected APY: {msg.expected_apy}%\n"
        f"Risk Score: {msg.risk_score}/10\n"
        f"Estimated Gas: {msg.estimated_gas_cost} ETH\n\n"
        f"Reasoning:\n{msg.reasoning}\n\n"
        f"💡 This strategy was optimized by coordinating 3 specialized agents:\n"
        f"• Chain Scanner: Scanned opportunities\n"
        f"• MeTTa Knowledge: Analyzed protocols\n"
        f"• Strategy Engine: Optimized allocation\n\n"
        f"Ready to execute? (In production, Execution Agent would handle this)"
    )

    await ctx.send(user, final_msg)

    # Clean up pending request
    ctx.logger.info(f"✅ Request {msg.request_id} completed successfully!")
    del pending_requests[msg.request_id]


# ===== STARTUP EVENT HANDLER =====

@coordinator.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🎯 Portfolio Coordinator Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Name: {coordinator.name}")
    ctx.logger.info(f"Agent Address: {coordinator.address}")
    ctx.logger.info(f"Port: {config.COORDINATOR_PORT}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"ASI:One Compatible: YES ✓")
    ctx.logger.info(f"Chat Protocol: ENABLED ✓")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)
    ctx.logger.info("Registered Agents:")
    ctx.logger.info(f"  • Scanner: {config.SCANNER_ADDRESS}")
    ctx.logger.info(f"  • MeTTa: {config.METTA_ADDRESS}")
    ctx.logger.info(f"  • Strategy: {config.STRATEGY_ADDRESS}")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to coordinate agent swarm!")


# Include chat protocol and publish manifest
coordinator.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🐝 YieldSwarm AI - Portfolio Coordinator Agent")
    print("=" * 60)
    print(f"Agent Address: {coordinator.address}")
    print(f"Port: {config.COORDINATOR_PORT}")
    print(f"ASI:One Compatible: YES ✓")
    print(f"Chat Protocol: ENABLED ✓")
    print(f"Mailbox: Enabled (Agentverse Ready)")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting coordinator with full agent orchestration...\n")

    # Run the agent (this blocks)
    coordinator.run()
