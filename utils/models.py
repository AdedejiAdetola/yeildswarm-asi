"""
YieldSwarm AI - Data Models
"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk tolerance levels"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class Chain(str, Enum):
    """Supported blockchain networks"""
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"


class ProtocolType(str, Enum):
    """Types of DeFi protocols"""
    DEX = "dex"
    LENDING = "lending"
    STAKING = "staking"
    YIELD = "yield"


# User Requests
class InvestmentRequest(BaseModel):
    """User investment request"""
    user_id: str
    amount: float
    currency: str = "ETH"
    risk_level: RiskLevel
    preferred_chains: List[Chain] = []
    min_apy: Optional[float] = None
    max_gas_cost: Optional[float] = None


# Opportunities
class YieldOpportunity(BaseModel):
    """Yield opportunity from chain scanner"""
    protocol: str
    chain: Chain
    protocol_type: ProtocolType
    apy: float
    tvl: float
    risk_score: float
    timestamp: datetime


# Strategies
class AllocationAction(BaseModel):
    """Individual allocation action"""
    action_type: str  # "deposit", "swap", "bridge", "withdraw"
    protocol: str
    chain: Chain
    amount: float
    currency: str
    expected_apy: Optional[float] = None


class Strategy(BaseModel):
    """Investment strategy"""
    strategy_id: str
    user_id: str
    total_amount: float
    actions: List[AllocationAction]
    expected_apy: float
    risk_score: float
    estimated_gas_cost: float
    created_at: datetime


# Execution
class TransactionResult(BaseModel):
    """Result of transaction execution"""
    tx_hash: str
    chain: Chain
    status: str  # "success", "failed", "pending"
    gas_used: Optional[float] = None
    error: Optional[str] = None


class ExecutionReport(BaseModel):
    """Report of strategy execution"""
    strategy_id: str
    transactions: List[TransactionResult]
    total_gas_cost: float
    execution_time: float
    status: str


# Performance
class Position(BaseModel):
    """Active position in a protocol"""
    protocol: str
    chain: Chain
    amount: float
    currency: str
    entry_apy: float
    current_apy: float
    entry_date: datetime


class PortfolioMetrics(BaseModel):
    """Portfolio performance metrics"""
    total_value: float
    pnl_24h: float
    pnl_7d: float
    pnl_30d: float
    realized_apy: float
    total_gas_costs: float
    positions: List[Position]
    updated_at: datetime


# Agent Messages
class OpportunityData(BaseModel):
    """Message containing opportunity data"""
    opportunities: List[YieldOpportunity]
    timestamp: datetime


class StrategyRequest(BaseModel):
    """Request to generate a strategy"""
    investment_request: InvestmentRequest
    opportunities: List[YieldOpportunity]
    metta_knowledge: Optional[Dict] = None


class ApprovedStrategy(BaseModel):
    """Approved strategy ready for execution"""
    strategy: Strategy
    user_confirmation: bool = True


class PerformanceUpdate(BaseModel):
    """Performance update message"""
    user_id: str
    metrics: PortfolioMetrics


# MeTTa Knowledge
class ProtocolKnowledge(BaseModel):
    """Knowledge about a DeFi protocol"""
    protocol_name: str
    protocol_type: ProtocolType
    supported_chains: List[Chain]
    risk_score: float
    historical_apy: List[float]
    smart_contract_audited: bool
    last_updated: datetime


class MeTTaQuery(BaseModel):
    """Query to MeTTa knowledge base"""
    query_type: str  # "find_best_strategy", "assess_risk", "get_protocol_info"
    parameters: Dict
