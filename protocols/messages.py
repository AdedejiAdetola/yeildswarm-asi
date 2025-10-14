"""
YieldSwarm AI - Inter-Agent Message Models
Pydantic models for agent-to-agent communication
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


# ===== ENUMS =====

class RiskLevel(str, Enum):
    """Risk tolerance levels for investment strategies"""
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


# ===== PORTFOLIO COORDINATOR <-> CHAIN SCANNER =====

class OpportunityRequest(BaseModel):
    """Request from Portfolio Coordinator to Chain Scanner"""
    request_id: str = Field(..., description="Unique request identifier")
    chains: List[Chain] = Field(..., description="Chains to scan")
    min_apy: float = Field(default=0.0, description="Minimum APY threshold (%)")
    max_risk_score: float = Field(default=10.0, description="Maximum risk score (0-10)")


class Opportunity(BaseModel):
    """Single DeFi opportunity"""
    protocol: str = Field(..., description="Protocol name (e.g., Aave-V3)")
    chain: Chain = Field(..., description="Blockchain network")
    apy: float = Field(..., description="Annual Percentage Yield (%)")
    tvl: float = Field(..., description="Total Value Locked (USD)")
    risk_score: float = Field(..., description="Risk score (0-10, lower is safer)")
    pool_address: Optional[str] = Field(None, description="Smart contract address")
    token_pair: Optional[str] = Field(None, description="Token pair (e.g., ETH-USDC)")


class OpportunityResponse(BaseModel):
    """Response from Chain Scanner to Portfolio Coordinator"""
    request_id: str = Field(..., description="Matches request ID")
    opportunities: List[Opportunity] = Field(..., description="List of opportunities found")
    timestamp: str = Field(..., description="ISO timestamp of scan")
    chains_scanned: List[Chain] = Field(..., description="Chains that were scanned")


# ===== PORTFOLIO COORDINATOR <-> METTA KNOWLEDGE =====

class MeTTaQueryRequest(BaseModel):
    """Request to MeTTa Knowledge Agent"""
    request_id: str = Field(..., description="Unique request identifier")
    opportunities: List[Opportunity] = Field(..., description="Opportunities to analyze")
    risk_level: str = Field(..., description="Risk level: conservative, moderate, aggressive")
    amount: float = Field(..., description="Investment amount")
    chains: List[Chain] = Field(..., description="Preferred chains")


class MeTTaQueryResponse(BaseModel):
    """Response from MeTTa Knowledge Agent"""
    request_id: str = Field(..., description="Matches request ID")
    recommended_protocols: List[str] = Field(..., description="List of recommended protocol names")
    reasoning: str = Field(..., description="Explainable AI reasoning for the recommendations")
    confidence: float = Field(default=0.85, description="Confidence score (0-1)")
    risk_assessments: Optional[Dict[str, float]] = Field(default=None, description="Risk scores per protocol")


# ===== PORTFOLIO COORDINATOR <-> STRATEGY ENGINE =====

class StrategyRequest(BaseModel):
    """Request from Portfolio Coordinator to Strategy Engine"""
    request_id: str = Field(..., description="Unique request identifier")
    amount: float = Field(..., description="Investment amount")
    currency: str = Field(default="ETH", description="Currency (ETH, USDC, etc.)")
    risk_level: str = Field(..., description="Risk level: conservative, moderate, aggressive")
    opportunities: List[Opportunity] = Field(..., description="Available opportunities from scanner")
    recommended_protocols: List[str] = Field(..., description="Recommended protocols from MeTTa")
    chains: List[Chain] = Field(..., description="Preferred blockchain networks")


class AllocationItem(BaseModel):
    """Single allocation in a strategy"""
    protocol: str = Field(..., description="Protocol name")
    chain: str = Field(..., description="Blockchain network")
    amount: float = Field(..., description="Amount to allocate")
    percentage: float = Field(..., description="Percentage of total portfolio (0-100)")
    expected_apy: float = Field(..., description="Expected APY (%)")
    risk_score: float = Field(default=5.0, description="Risk score (0-10)")


class StrategyResponse(BaseModel):
    """Response from Strategy Engine to Portfolio Coordinator"""
    request_id: str = Field(..., description="Matches request ID")
    allocations: List[AllocationItem] = Field(..., description="Recommended allocations")
    expected_apy: float = Field(..., description="Expected weighted average APY (%)")
    risk_score: float = Field(..., description="Portfolio risk score (0-10)")
    estimated_gas_cost: float = Field(..., description="Estimated gas cost in ETH")
    reasoning: str = Field(..., description="Strategy reasoning and justification")
    timestamp: str = Field(..., description="ISO timestamp")


# ===== PORTFOLIO COORDINATOR <-> EXECUTION AGENT =====

class ExecutionRequest(BaseModel):
    """Request from Portfolio Coordinator to Execution Agent"""
    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="User identifier")
    strategy: StrategyResponse = Field(..., description="Approved strategy to execute")
    user_wallet: str = Field(..., description="User wallet address")
    max_slippage: float = Field(default=0.5, description="Maximum slippage tolerance (%)")


class TransactionDetail(BaseModel):
    """Details of a single transaction"""
    tx_hash: str = Field(..., description="Transaction hash")
    chain: Chain = Field(..., description="Blockchain network")
    protocol: str = Field(..., description="Protocol name")
    action: str = Field(..., description="Action type: deposit, swap, bridge, etc.")
    amount: float = Field(..., description="Transaction amount")
    status: str = Field(..., description="Status: pending, confirmed, failed")
    gas_used: Optional[float] = Field(None, description="Gas used (in native token)")
    timestamp: str = Field(..., description="ISO timestamp")


class ExecutionResponse(BaseModel):
    """Response from Execution Agent to Portfolio Coordinator"""
    request_id: str = Field(..., description="Matches request ID")
    user_id: str = Field(..., description="User identifier")
    status: str = Field(..., description="Overall status: success, partial, failed")
    transactions: List[TransactionDetail] = Field(..., description="List of executed transactions")
    total_gas_cost: float = Field(..., description="Total gas cost (USD)")
    execution_time_seconds: float = Field(..., description="Total execution time")
    errors: List[str] = Field(default_factory=list, description="List of errors if any")


# ===== PORTFOLIO COORDINATOR <-> PERFORMANCE TRACKER =====

class PerformanceQuery(BaseModel):
    """Request to Performance Tracker Agent"""
    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="User identifier")
    query_type: str = Field(..., description="Query type: portfolio_status, performance_history, tax_report")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional parameters")


class PositionDetail(BaseModel):
    """Details of a single position"""
    protocol: str = Field(..., description="Protocol name")
    chain: Chain = Field(..., description="Blockchain network")
    amount: float = Field(..., description="Current position amount")
    entry_value: float = Field(..., description="Entry value (USD)")
    current_value: float = Field(..., description="Current value (USD)")
    pnl: float = Field(..., description="Profit/Loss (USD)")
    pnl_percentage: float = Field(..., description="P&L percentage")
    current_apy: float = Field(..., description="Current APY (%)")
    days_held: int = Field(..., description="Number of days position held")


class PerformanceResponse(BaseModel):
    """Response from Performance Tracker Agent"""
    request_id: str = Field(..., description="Matches request ID")
    user_id: str = Field(..., description="User identifier")
    total_portfolio_value: float = Field(..., description="Total portfolio value (USD)")
    total_pnl: float = Field(..., description="Total profit/loss (USD)")
    total_pnl_percentage: float = Field(..., description="Total P&L percentage")
    positions: List[PositionDetail] = Field(..., description="List of current positions")
    realized_apy: float = Field(..., description="Realized APY (%)")
    total_gas_spent: float = Field(..., description="Total gas spent (USD)")
    timestamp: str = Field(..., description="ISO timestamp")


# ===== ERROR HANDLING =====

class ErrorMessage(BaseModel):
    """Generic error message"""
    request_id: str = Field(..., description="Request ID that caused error")
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Human-readable error message")
    agent_name: str = Field(..., description="Agent that encountered the error")
    timestamp: str = Field(..., description="ISO timestamp")
