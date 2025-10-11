"""
YieldSwarm AI - Portfolio Coordinator Agent
ASI:One compatible agent with Chat Protocol + HTTP REST API
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
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from threading import Thread


# Create Portfolio Coordinator Agent (Mailbox Mode for Agentverse)
coordinator = Agent(
    name="yieldswarm-coordinator",
    seed=config.COORDINATOR_SEED,
    port=config.COORDINATOR_PORT,
    mailbox=f"{config.COORDINATOR_MAILBOX_KEY}@https://agentverse.ai",
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

                # Send initial acknowledgment
                initial_response = create_text_chat(
                    f"✅ Investment Request Received:\n\n"
                    f"Amount: {investment_req.amount} {investment_req.currency}\n"
                    f"Risk Level: {investment_req.risk_level.value}\n"
                    f"Chains: {', '.join([c.value for c in investment_req.preferred_chains])}\n\n"
                    f"🔄 Coordinating agents:\n"
                    f"1. 📡 Scanning chains for opportunities...\n"
                    f"2. 🧠 Querying knowledge base...\n"
                    f"3. ⚙️  Generating optimal strategy...\n\n"
                    f"Please wait while I coordinate with my agent swarm..."
                )
                await ctx.send(sender, initial_response)

                # === STEP 1: Request opportunities from Chain Scanner ===
                from protocols.messages import OpportunityRequest
                request_id = str(uuid4())

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
                    f"✓ Chain Scanner activated\n"
                    f"  Scanning {len(investment_req.preferred_chains)} chains...\n"
                    f"  Looking for APY ≥ {config.RISK_PROFILES[investment_req.risk_level.value]['min_apy']}%"
                )
                await ctx.send(sender, progress_msg)

                # Note: In a real implementation, we would wait for responses
                # from Scanner, MeTTa, and Strategy agents before responding.
                # For now, we're demonstrating the message sending pattern.
                # Full async orchestration will be implemented in next phase.

                ctx.logger.info(f"✅ Investment request {request_id} initiated for user {sender}")

            except Exception as e:
                ctx.logger.error(f"Error processing investment request: {str(e)}")
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


# ===== HTTP REST API FOR BACKEND INTEGRATION =====
# Store pending responses
pending_responses = {}

# Create FastAPI app for HTTP endpoints
http_app = FastAPI(title="Portfolio Coordinator HTTP API")

# Add CORS
http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_app.get("/")
async def http_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Portfolio Coordinator",
        "agent_address": str(coordinator.address),
        "http_api": "enabled",
        "chat_protocol": "enabled"
    }


@http_app.post("/chat")
async def http_chat(request: Request):
    """
    HTTP endpoint for chat messages from backend
    This bridges HTTP REST API → uAgents internal processing
    """
    try:
        data = await request.json()
        user_message = data.get("text", "")
        user_id = data.get("user_id", "http-user")

        # Process the message using the same logic as chat protocol
        response_text = await process_user_message(user_message, user_id)

        return JSONResponse({
            "success": True,
            "response": response_text,
            "user_id": user_id
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


async def process_user_message(text: str, user_id: str) -> str:
    """
    Process user message and return response
    This is the core logic that both HTTP and Chat Protocol use
    """
    text_lower = text.lower()

    # Check for help requests
    if any(word in text_lower for word in ['help', 'how', 'what can']):
        return (
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

    # Check for portfolio status requests
    if any(word in text_lower for word in ['portfolio', 'performance', 'status', 'balance']):
        return (
            "📊 Portfolio Status:\n\n"
            "This is a demo - connecting to Performance Tracker Agent...\n\n"
            "Once deployed, I'll show:\n"
            "• Total Value\n"
            "• Active Positions\n"
            "• Realized APY\n"
            "• P&L (24h, 7d, 30d)\n"
            "• Gas Costs"
        )

    # Parse investment request
    try:
        investment_req = parse_investment_request(text, user_id)

        response = (
            f"✅ Investment Request Received!\n\n"
            f"Amount: {investment_req.amount} {investment_req.currency}\n"
            f"Risk Level: {investment_req.risk_level.value}\n"
            f"Chains: {', '.join([c.value for c in investment_req.preferred_chains])}\n\n"
            f"🔄 Coordinating agents:\n"
            f"1. 📡 Scanning chains for opportunities...\n"
            f"2. 🧠 Querying knowledge base...\n"
            f"3. ⚙️  Generating optimal strategy...\n\n"
            f"Expected APY: {config.RISK_PROFILES[investment_req.risk_level.value]['min_apy']}-12%\n"
            f"Risk Score: {investment_req.risk_level.value.title()}\n\n"
            f"💡 In production, I coordinate with 6 specialized agents across {len(investment_req.preferred_chains)} chains!"
        )

        return response

    except Exception as e:
        return (
            "❌ Error processing request. Please try:\n\n"
            "'Invest 10 ETH with moderate risk'\n"
            "'Show my portfolio'\n"
            "'Help'"
        )


def run_http_server():
    """Run the HTTP server in a separate thread"""
    uvicorn.run(http_app, host="0.0.0.0", port=config.COORDINATOR_PORT, log_level="info")


@coordinator.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info(f"Portfolio Coordinator Agent started")
    ctx.logger.info(f"Agent address: {coordinator.address}")
    ctx.logger.info(f"ASI:One compatible: YES")
    ctx.logger.info(f"Chat Protocol: ENABLED")
    ctx.logger.info(f"HTTP API: ENABLED on port {config.COORDINATOR_PORT}")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Portfolio Coordinator Agent")
    print("=" * 60)
    print(f"Agent Address: {coordinator.address}")
    print(f"HTTP API Port: {config.COORDINATOR_PORT}")
    print(f"ASI:One Compatible: YES ✓")
    print(f"Chat Protocol: ENABLED ✓")
    print(f"HTTP REST API: ENABLED ✓")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting dual-mode agent (uAgents + HTTP)...\n")

    # Start HTTP server in a background thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run the uAgent (this blocks)
    coordinator.run()
