"""
Request models for FastAPI endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    """Investment risk levels"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class Chain(str, Enum):
    """Supported blockchain networks"""
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"


class ChatMessage(BaseModel):
    """Chat message from user"""
    text: str = Field(..., description="Message text")
    user_id: str = Field(..., description="User ID")


class InvestmentRequest(BaseModel):
    """Investment request from user"""
    user_id: str = Field(..., description="User ID")
    amount: float = Field(..., gt=0, description="Investment amount")
    currency: str = Field(default="ETH", description="Currency")
    risk_level: RiskLevel = Field(..., description="Risk tolerance level")
    chains: List[Chain] = Field(..., description="Preferred blockchain networks")
    min_apy: Optional[float] = Field(None, description="Minimum desired APY")
    max_risk_score: Optional[float] = Field(None, description="Maximum risk score")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "amount": 10.0,
                "currency": "ETH",
                "risk_level": "moderate",
                "chains": ["ethereum", "polygon"],
                "min_apy": 5.0,
                "max_risk_score": 6.0
            }
        }
