"""
YieldSwarm AI - FastAPI Backend Server
Run this from the project root with: python run_backend.py
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Dict, Any
from datetime import datetime
import asyncio
import logging
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
from utils.config import config

# ===== Models =====
from pydantic import BaseModel, Field
from enum import Enum

class RiskLevel(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"

class ChatMessage(BaseModel):
    text: str
    user_id: str

class InvestmentRequest(BaseModel):
    user_id: str
    amount: float
    currency: str = "ETH"
    risk_level: RiskLevel
    chains: List[Chain]

class AgentStatusResponse(BaseModel):
    name: str
    status: str
    icon: str
    last_activity: str
    tasks_completed: int

class PositionInfo(BaseModel):
    protocol: str
    chain: str
    amount: float
    apy: float
    value: float
    pnl: float

class PortfolioStats(BaseModel):
    total_value: float
    total_invested: float
    total_pnl: float
    avg_apy: float

class PortfolioResponse(BaseModel):
    user_id: str
    stats: PortfolioStats
    positions: List[PositionInfo]
    last_updated: datetime

# ===== Agent Client Service =====
class AgentClient:
    def __init__(self):
        self.http_client = None
        logger.info("🤖 AgentClient initialized")

    async def start(self):
        self.http_client = httpx.AsyncClient(timeout=10.0)
        logger.info("✅ AgentClient started")

    async def stop(self):
        if self.http_client:
            await self.http_client.aclose()
        logger.info("👋 AgentClient stopped")

    async def get_agent_statuses(self) -> List[AgentStatusResponse]:
        return [
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

    async def send_chat_message(self, message: str, user_id: str) -> str:
        logger.info(f"📤 Chat message from {user_id}: {message}")

        message_lower = message.lower()
        if "invest" in message_lower:
            return "I'll help you invest! Specify amount, risk level, and chains."
        elif "portfolio" in message_lower:
            return "📊 Your portfolio:\n- Total Value: $15,234\n- P&L: +$1,234 (+8.82%)"
        elif "status" in message_lower:
            return "🤖 All 6 agents are online and operational!"
        else:
            return "👋 I'm YieldSwarm AI! Ask me to invest, check portfolio, or get status."

    async def process_investment_request(
        self, user_id: str, amount: float, currency: str,
        risk_level: str, chains: List[str]
    ) -> Dict[str, Any]:
        logger.info(f"💰 Processing {amount} {currency} investment")
        return {
            "request_id": f"req_{user_id}_{int(datetime.now().timestamp())}",
            "status": "processing",
            "message": f"Processing {amount} {currency} with {risk_level} risk",
            "steps": [
                {"step": 1, "name": "Scanning chains", "status": "in_progress"},
                {"step": 2, "name": "Querying knowledge", "status": "pending"},
                {"step": 3, "name": "Generating strategy", "status": "pending"},
            ]
        }

    async def get_portfolio(self, user_id: str) -> PortfolioResponse:
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
            ],
            last_updated=datetime.now()
        )

    async def get_opportunities(self) -> List[Dict[str, Any]]:
        return [
            {"protocol": "Aave V3", "chain": "Ethereum", "apy": 8.5, "tvl": 5200000000, "risk_score": 2.5},
            {"protocol": "Compound", "chain": "Polygon", "apy": 12.3, "tvl": 1800000000, "risk_score": 3.2},
            {"protocol": "Uniswap V3", "chain": "Arbitrum", "apy": 18.7, "tvl": 3500000000, "risk_score": 5.1},
        ]

# Global agent client
agent_client: AgentClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_client
    logger.info("🚀 Starting YieldSwarm AI Backend...")
    agent_client = AgentClient()
    await agent_client.start()
    logger.info("✅ Backend ready!")
    yield
    logger.info("👋 Shutting down...")
    await agent_client.stop()

# Create FastAPI app
app = FastAPI(
    title="YieldSwarm AI API",
    description="Backend API for YieldSwarm AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== API ENDPOINTS =====

@app.get("/")
async def root():
    return {"status": "online", "service": "YieldSwarm AI", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_client": "connected" if agent_client else "disconnected"
    }

@app.get("/api/agents/status", response_model=List[AgentStatusResponse])
async def get_agent_status():
    try:
        return await agent_client.get_agent_statuses()
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def send_chat_message(message: ChatMessage):
    try:
        response = await agent_client.send_chat_message(message.text, message.user_id)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/invest")
async def create_investment(request: InvestmentRequest):
    try:
        result = await agent_client.process_investment_request(
            user_id=request.user_id,
            amount=request.amount,
            currency=request.currency,
            risk_level=request.risk_level,
            chains=request.chains
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio/{user_id}", response_model=PortfolioResponse)
async def get_portfolio(user_id: str):
    try:
        return await agent_client.get_portfolio(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/opportunities")
async def get_opportunities():
    try:
        opportunities = await agent_client.get_opportunities()
        return {"success": True, "opportunities": opportunities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connected: {user_id}")
    try:
        while True:
            status = await agent_client.get_agent_statuses()
            await websocket.send_json({"type": "status", "data": status})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run_backend:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
