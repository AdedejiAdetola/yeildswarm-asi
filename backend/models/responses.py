"""
Response models for FastAPI endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentStatusResponse(BaseModel):
    """Agent status information"""
    name: str
    status: str  # "online", "busy", "offline"
    icon: str
    last_activity: str
    tasks_completed: int


class PositionInfo(BaseModel):
    """Single position in portfolio"""
    protocol: str
    chain: str
    amount: float
    apy: float
    value: float
    pnl: float


class PortfolioStats(BaseModel):
    """Portfolio statistics"""
    total_value: float
    total_invested: float
    total_pnl: float
    avg_apy: float


class PortfolioResponse(BaseModel):
    """User portfolio information"""
    user_id: str
    stats: PortfolioStats
    positions: List[PositionInfo]
    last_updated: datetime


class OpportunityInfo(BaseModel):
    """DeFi opportunity information"""
    protocol: str
    chain: str
    apy: float
    tvl: float
    risk_score: float
    category: str


class StrategyAction(BaseModel):
    """Action in investment strategy"""
    action_type: str
    protocol: str
    chain: str
    amount: float
    expected_apy: float


class StrategyResponse(BaseModel):
    """Investment strategy response"""
    strategy_id: str
    user_id: str
    total_amount: float
    actions: List[StrategyAction]
    expected_apy: float
    risk_score: float
    estimated_gas_cost: float
    created_at: datetime
