"""
YieldSwarm AI - Portfolio Coordinator Agent
ASI:One compatible agent with Chat Protocol
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
import re


# Create Portfolio Coordinator Agent (Local Mode with Endpoint)
coordinator = Agent(
    name="yieldswarm-coordinator",
    seed=config.COORDINATOR_SEED,
    port=config.COORDINATOR_PORT,
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Initialize chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# Store user sessions
user_sessions = {}


def create_text_chat(text: str) -> ChatMessage:
    """Create a chat message with text content"""
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
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


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages"""
    ctx.logger.info(f"Received message from {sender}")

    # Send acknowledgement
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
            ctx.logger.info(f"Session started with {sender}")
            user_sessions[sender] = {
                "started_at": datetime.now(timezone.utc),
                "requests": []
            }

            welcome_msg = create_text_chat(
                "👋 Welcome to YieldSwarm AI!\n\n"
                "I'm your autonomous DeFi yield optimizer. I coordinate a swarm of 6 specialized AI agents "
                "to maximize your returns across Ethereum, Solana, BSC, Polygon, and Arbitrum.\n\n"
                "Tell me:\n"
                "• How much you want to invest (e.g., '10 ETH')\n"
                "• Your risk tolerance (conservative/moderate/aggressive)\n"
                "• Preferred chains (optional)\n\n"
                "Example: 'I want to invest 5 ETH with moderate risk on Ethereum and Polygon'"
            )
            await ctx.send(sender, welcome_msg)

        elif isinstance(item, TextContent):
            ctx.logger.info(f"Processing request: {item.text}")

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
                    "This is a demo - connecting to Performance Tracker Agent...\n\n"
                    "Once deployed, I'll show:\n"
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

                # Create response message
                response_text = (
                    f"✅ Investment Request Parsed:\n\n"
                    f"Amount: {investment_req.amount} {investment_req.currency}\n"
                    f"Risk Level: {investment_req.risk_level.value}\n"
                    f"Chains: {', '.join([c.value for c in investment_req.preferred_chains])}\n\n"
                    f"🔄 Coordinating agents:\n"
                    f"1. ✓ Chain Scanner - Scanning for opportunities...\n"
                    f"2. ✓ MeTTa Knowledge - Analyzing protocol data...\n"
                    f"3. ⏳ Strategy Engine - Calculating optimal allocation...\n\n"
                    f"💡 In production, I would:\n"
                    f"• Query {len(investment_req.preferred_chains)} chains across 20+ protocols\n"
                    f"• Use MeTTa knowledge graphs for intelligent decisions\n"
                    f"• Generate optimized strategy in seconds\n"
                    f"• Execute with MEV protection\n\n"
                    f"Expected APY range: {config.RISK_PROFILES[investment_req.risk_level.value]['min_apy']}%+"
                )

                response_msg = create_text_chat(response_text)
                await ctx.send(sender, response_msg)

                # In production, would now send to other agents:
                # await ctx.send(config.SCANNER_ADDRESS, {...})
                # await ctx.send(config.METTA_ADDRESS, {...})
                # await ctx.send(config.STRATEGY_ADDRESS, {...})

            except Exception as e:
                error_msg = create_text_chat(
                    f"❌ Error processing request: {str(e)}\n\n"
                    f"Please try: 'Invest 10 ETH with moderate risk'"
                )
                await ctx.send(sender, error_msg)

        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            if sender in user_sessions:
                del user_sessions[sender]

            goodbye_msg = create_text_chat(
                "👋 Thanks for using YieldSwarm AI!\n\n"
                "Your autonomous DeFi yield optimizer is always monitoring opportunities."
            )
            await ctx.send(sender, goodbye_msg)

        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle message acknowledgements"""
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")


# Include chat protocol and publish manifest
coordinator.include(chat_proto, publish_manifest=True)


@coordinator.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info(f"Portfolio Coordinator Agent started")
    ctx.logger.info(f"Agent address: {coordinator.address}")
    ctx.logger.info(f"ASI:One compatible: YES")
    ctx.logger.info(f"Chat Protocol: ENABLED")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Portfolio Coordinator Agent")
    print("=" * 60)
    print(f"Agent Address: {coordinator.address}")
    print(f"Port: {config.COORDINATOR_PORT}")
    print(f"ASI:One Compatible: YES ✓")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting agent...\n")

    coordinator.run()
