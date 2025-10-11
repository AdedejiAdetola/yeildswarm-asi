"""
YieldSwarm AI - FastAPI Backend Server
Connects frontend to uAgents via REST API
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Dict, Any
import asyncio
import logging
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.requests import InvestmentRequest, ChatMessage
from models.responses import AgentStatusResponse, PortfolioResponse
from services.agent_client import AgentClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent client
agent_client: AgentClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global agent_client

    # Startup
    logger.info("🚀 Starting YieldSwarm AI Backend...")
    agent_client = AgentClient()
    await agent_client.start()
    logger.info("✅ Backend ready!")

    yield

    # Shutdown
    logger.info("👋 Shutting down backend...")
    await agent_client.stop()


# Create FastAPI app
app = FastAPI(
    title="YieldSwarm AI API",
    description="Backend API for YieldSwarm AI - Autonomous DeFi Yield Optimizer",
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
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "YieldSwarm AI Backend",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agent_client": "connected" if agent_client else "disconnected",
        "timestamp": asyncio.get_event_loop().time()
    }


@app.get("/api/agents/status", response_model=List[AgentStatusResponse])
async def get_agent_status():
    """Get status of all agents"""
    try:
        statuses = await agent_client.get_agent_statuses()
        return statuses
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def send_chat_message(message: ChatMessage):
    """Send chat message to Portfolio Coordinator agent"""
    try:
        response = await agent_client.send_chat_message(message.text, message.user_id)
        return {"success": True, "response": response}
    except Exception as e:
        logger.error(f"Error sending chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/invest")
async def create_investment(request: InvestmentRequest):
    """Create investment request and process with agents"""
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
        logger.error(f"Error processing investment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/portfolio/{user_id}", response_model=PortfolioResponse)
async def get_portfolio(user_id: str):
    """Get user's portfolio"""
    try:
        portfolio = await agent_client.get_portfolio(user_id)
        return portfolio
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/opportunities")
async def get_opportunities():
    """Get current DeFi opportunities"""
    try:
        opportunities = await agent_client.get_opportunities()
        return {"success": True, "opportunities": opportunities}
    except Exception as e:
        logger.error(f"Error getting opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket connection for real-time agent updates"""
    await websocket.accept()
    logger.info(f"WebSocket connected: {user_id}")

    try:
        while True:
            # Send periodic updates
            status = await agent_client.get_agent_statuses()
            await websocket.send_json({"type": "status", "data": status})
            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
