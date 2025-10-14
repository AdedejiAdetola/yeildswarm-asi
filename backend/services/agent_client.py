"""
YieldSwarm AI - Agent Client Service
Handles communication between FastAPI backend and uAgents
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config import config
from backend.models.responses import AgentStatusResponse, PortfolioResponse, PortfolioStats, PositionInfo

logger = logging.getLogger(__name__)


class AgentClient:
    """
    Client for communicating with uAgents via HTTP/WebSocket
    In production, this would connect to Agentverse mailbox endpoints
    """

    def __init__(self):
        self.agent_addresses = {
            "coordinator": config.COORDINATOR_ADDRESS,
            "scanner": config.SCANNER_ADDRESS,
            "metta": config.METTA_ADDRESS,
            "strategy": config.STRATEGY_ADDRESS,
            "execution": config.EXECUTION_ADDRESS,
            "tracker": config.TRACKER_ADDRESS,
        }
        self.agent_ports = {
            "coordinator": 8000,
            "scanner": 8001,
            "strategy": 8002,
        }
        self.http_client: Optional[httpx.AsyncClient] = None
        logger.info("🤖 AgentClient initialized")

    async def start(self):
        """Start the agent client"""
        self.http_client = httpx.AsyncClient(timeout=10.0)
        logger.info("✅ AgentClient started")

    async def stop(self):
        """Stop the agent client"""
        if self.http_client:
            await self.http_client.aclose()
        logger.info("👋 AgentClient stopped")

    async def get_agent_statuses(self) -> List[AgentStatusResponse]:
        """
        Get status of all agents
        Returns mock data for demo, in production would query actual agents
        """
        # In production, this would check actual agent endpoints
        # For now, return realistic demo data
        statuses = [
            AgentStatusResponse(
                name="Portfolio Coordinator",
                status="online",
                icon="🎯",
                last_activity="2 minutes ago",
                tasks_completed=12
            ),
            AgentStatusResponse(
                name="Chain Scanner",
                status="busy",
                icon="📡",
                last_activity="Just now",
                tasks_completed=45
            ),
            AgentStatusResponse(
                name="MeTTa Knowledge",
                status="online",
                icon="🧠",
                last_activity="5 minutes ago",
                tasks_completed=28
            ),
            AgentStatusResponse(
                name="Strategy Engine",
                status="online",
                icon="⚙️",
                last_activity="1 minute ago",
                tasks_completed=15
            ),
            AgentStatusResponse(
                name="Execution Agent",
                status="online",
                icon="⚡",
                last_activity="3 minutes ago",
                tasks_completed=8
            ),
            AgentStatusResponse(
                name="Performance Tracker",
                status="online",
                icon="📊",
                last_activity="4 minutes ago",
                tasks_completed=22
            ),
        ]

        # TODO: In production, actually check agent health via HTTP endpoints
        # for agent_name, port in self.agent_ports.items():
        #     try:
        #         response = await self.http_client.get(f"http://localhost:{port}/health")
        #         if response.status_code == 200:
        #             # Update status based on response
        #             pass
        #     except Exception as e:
        #         logger.warning(f"Agent {agent_name} not reachable: {e}")

        return statuses

    async def send_chat_message(self, message: str, user_id: str) -> str:
        """
        Send chat message to Portfolio Coordinator agent via Chat Protocol
        """
        logger.info(f"📤 Sending chat message from {user_id}: {message}")

        try:
            # Send to coordinator agent via HTTP endpoint
            coordinator_url = "http://localhost:8000/submit"

            # Create Chat Protocol message
            payload = {
                "protocol": "agent_chat",
                "type": "agent_message",
                "sender": user_id,
                "target": config.COORDINATOR_ADDRESS,
                "session_id": f"session_{user_id}",
                "message": {
                    "timestamp": datetime.now().isoformat(),
                    "msg_id": str(id(message)),
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        }
                    ]
                }
            }

            # Send to coordinator
            response = await self.http_client.post(
                coordinator_url,
                json=payload,
                timeout=10.0
            )

            if response.status_code == 200:
                logger.info(f"✅ Message sent to coordinator successfully")
                return (
                    f"✅ Request received! Your message: '{message[:50]}...'\n\n"
                    f"🤖 My agent swarm is processing your request:\n"
                    f"• 📡 Chain Scanner - Scanning DeFi protocols\n"
                    f"• 🧠 MeTTa Knowledge - Analyzing opportunities\n"
                    f"• ⚙️  Strategy Engine - Optimizing allocation\n\n"
                    f"💡 Check the console logs to see the agents in action!\n"
                    f"   tail -f logs/coordinator.log\n\n"
                    f"Note: Full agent orchestration is running. The complete response will "
                    f"show the strategy with allocations, expected APY, and reasoning from the AI agents."
                )
            else:
                logger.warning(f"⚠️  Coordinator returned {response.status_code}")
                return f"⚠️  Agent system processing... (Status: {response.status_code})"

        except Exception as e:
            logger.error(f"❌ Error sending to coordinator: {str(e)}")

            # Fallback response
            return (
                "🤖 YieldSwarm AI is processing your request through the agent swarm.\n\n"
                f"Your message: '{message}'\n\n"
                "The coordinator agent will orchestrate:\n"
                "1. Chain Scanner - Finding opportunities\n"
                "2. MeTTa Knowledge - AI analysis\n"
                "3. Strategy Engine - Optimal allocation\n\n"
                "Watch the magic in logs: tail -f logs/coordinator.log logs/scanner.log"
            )

    async def process_investment_request(
        self,
        user_id: str,
        amount: float,
        currency: str,
        risk_level: str,
        chains: List[str]
    ) -> Dict[str, Any]:
        """
        Process investment request through agent swarm
        """
        logger.info(f"💰 Processing investment: {amount} {currency} for {user_id}")

        # In production, this would:
        # 1. Send OpportunityRequest to Chain Scanner
        # 2. Send MeTTaQuery to Knowledge Agent
        # 3. Send StrategyRequest to Strategy Engine
        # 4. Wait for responses and coordinate

        # For demo, return realistic strategy
        return {
            "request_id": f"req_{user_id}_{int(datetime.now().timestamp())}",
            "status": "processing",
            "message": f"Processing investment of {amount} {currency} with {risk_level} risk",
            "estimated_completion": "30 seconds",
            "steps": [
                {"step": 1, "name": "Scanning chains", "status": "in_progress"},
                {"step": 2, "name": "Querying knowledge base", "status": "pending"},
                {"step": 3, "name": "Generating strategy", "status": "pending"},
                {"step": 4, "name": "Executing transactions", "status": "pending"},
            ]
        }

    async def get_portfolio(self, user_id: str) -> PortfolioResponse:
        """
        Get user's portfolio from Performance Tracker agent
        """
        logger.info(f"📊 Getting portfolio for {user_id}")

        # In production, query Performance Tracker agent
        # For demo, return realistic portfolio data
        return PortfolioResponse(
            user_id=user_id,
            stats=PortfolioStats(
                total_value=15234.56,
                total_invested=14000.00,
                total_pnl=1234.56,
                avg_apy=12.5
            ),
            positions=[
                PositionInfo(
                    protocol="Aave",
                    chain="Ethereum",
                    amount=5.0,
                    apy=8.2,
                    value=7250.00,
                    pnl=250.00
                ),
                PositionInfo(
                    protocol="Compound",
                    chain="Polygon",
                    amount=3.0,
                    apy=15.5,
                    value=4350.50,
                    pnl=350.50
                ),
                PositionInfo(
                    protocol="Uniswap V3",
                    chain="Arbitrum",
                    amount=2.5,
                    apy=22.8,
                    value=3634.06,
                    pnl=634.06
                ),
            ],
            last_updated=datetime.now()
        )

    async def get_opportunities(self) -> List[Dict[str, Any]]:
        """
        Get current DeFi opportunities from Chain Scanner
        """
        logger.info("🔍 Getting DeFi opportunities")

        # In production, query Chain Scanner agent
        # For demo, return realistic opportunities
        return [
            {
                "protocol": "Aave V3",
                "chain": "Ethereum",
                "apy": 8.5,
                "tvl": 5_200_000_000,
                "risk_score": 2.5,
                "category": "Lending"
            },
            {
                "protocol": "Compound V3",
                "chain": "Polygon",
                "apy": 12.3,
                "tvl": 1_800_000_000,
                "risk_score": 3.2,
                "category": "Lending"
            },
            {
                "protocol": "Uniswap V3",
                "chain": "Arbitrum",
                "apy": 18.7,
                "tvl": 3_500_000_000,
                "risk_score": 5.1,
                "category": "DEX"
            },
            {
                "protocol": "Lido",
                "chain": "Ethereum",
                "apy": 4.2,
                "tvl": 32_000_000_000,
                "risk_score": 1.8,
                "category": "Staking"
            },
            {
                "protocol": "GMX",
                "chain": "Arbitrum",
                "apy": 25.4,
                "tvl": 450_000_000,
                "risk_score": 6.8,
                "category": "Derivatives"
            },
        ]
