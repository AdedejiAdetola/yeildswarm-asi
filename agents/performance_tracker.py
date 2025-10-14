"""
YieldSwarm AI - Performance Tracker Agent (Clean)
Pure uAgents implementation for portfolio performance monitoring
"""

import os
import sys
import logging
from datetime import datetime, timezone
from typing import Dict, List
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from protocols.messages import (
    PerformanceQuery,
    PerformanceResponse,
    PositionDetail
)
from utils.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Performance Tracker Agent
performance_agent = Agent(
    name="performance_tracker",
    seed=config.TRACKER_SEED,
    port=8005,
    endpoint=["http://0.0.0.0:8005/submit"]
)

# In-memory storage for tracking (in production, use database)
user_portfolios: Dict[str, Dict] = {}


@performance_agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("📊 Performance Tracker Agent Starting")
    logger.info("=" * 60)
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Port: 8005")
    logger.info(f"Coordinator: {config.COORDINATOR_ADDRESS}")
    logger.info("=" * 60)


@performance_agent.on_message(model=PerformanceQuery)
async def handle_performance_query(ctx: Context, sender: str, msg: PerformanceQuery):
    """
    Handle performance query from Portfolio Coordinator

    Query Types:
    - portfolio_status: Current portfolio value and positions
    - performance_history: Historical P&L over time
    - tax_report: Tax reporting data for realized gains

    Process:
    1. Retrieve user's positions from storage
    2. Query current prices from oracles/APIs
    3. Calculate P&L and performance metrics
    4. Return comprehensive performance data

    NOTE: This is a SIMULATION for the hackathon.
    In production, this would:
    - Query on-chain positions via RPC
    - Integrate with price oracles (Chainlink, etc.)
    - Track all historical transactions
    - Calculate accurate P&L including gas
    """
    logger.info("=" * 60)
    logger.info(f"📨 Received Performance Query: {msg.request_id}")
    logger.info(f"   From: {sender}")
    logger.info(f"   User: {msg.user_id}")
    logger.info(f"   Query Type: {msg.query_type}")
    logger.info("=" * 60)

    try:
        # Handle different query types
        if msg.query_type == "portfolio_status":
            response = await _get_portfolio_status(msg)
        elif msg.query_type == "performance_history":
            response = await _get_performance_history(msg)
        elif msg.query_type == "tax_report":
            response = await _get_tax_report(msg)
        else:
            # Default to portfolio status
            response = await _get_portfolio_status(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        logger.info(f"✅ Sent Performance Response: {msg.request_id}")
        logger.info(f"   Portfolio Value: ${response.total_portfolio_value:.2f}")
        logger.info(f"   P&L: ${response.total_pnl:.2f} ({response.total_pnl_percentage:.2f}%)")
        logger.info(f"   Positions: {len(response.positions)}")

    except Exception as e:
        logger.error(f"❌ Error processing performance query: {str(e)}")
        # Send error response with empty data
        error_response = PerformanceResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            total_portfolio_value=0.0,
            total_pnl=0.0,
            total_pnl_percentage=0.0,
            positions=[],
            realized_apy=0.0,
            total_gas_spent=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        await ctx.send(sender, error_response)


async def _get_portfolio_status(msg: PerformanceQuery) -> PerformanceResponse:
    """
    Get current portfolio status

    In production, this would:
    - Query on-chain positions for user's wallet
    - Get current token prices
    - Calculate current value vs entry value
    """

    # Check if user has portfolio data
    if msg.user_id not in user_portfolios:
        # Return empty portfolio for new users
        return PerformanceResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            total_portfolio_value=0.0,
            total_pnl=0.0,
            total_pnl_percentage=0.0,
            positions=[],
            realized_apy=0.0,
            total_gas_spent=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    # Retrieve user's portfolio
    portfolio = user_portfolios[msg.user_id]

    # Simulate getting current positions with updated prices
    positions = _simulate_positions(portfolio)

    # Calculate totals
    total_value = sum(pos.current_value for pos in positions)
    total_entry = sum(pos.entry_value for pos in positions)
    total_pnl = total_value - total_entry
    total_pnl_pct = (total_pnl / total_entry * 100) if total_entry > 0 else 0.0

    # Calculate realized APY
    # Simplified: sum of position APYs weighted by allocation
    realized_apy = sum(
        pos.current_apy * (pos.current_value / total_value)
        for pos in positions
    ) if total_value > 0 else 0.0

    return PerformanceResponse(
        request_id=msg.request_id,
        user_id=msg.user_id,
        total_portfolio_value=total_value,
        total_pnl=total_pnl,
        total_pnl_percentage=total_pnl_pct,
        positions=positions,
        realized_apy=realized_apy,
        total_gas_spent=portfolio.get("total_gas_spent", 0.0),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


async def _get_performance_history(msg: PerformanceQuery) -> PerformanceResponse:
    """Get historical performance data"""
    # For hackathon, return current status
    # In production, would return time-series data
    return await _get_portfolio_status(msg)


async def _get_tax_report(msg: PerformanceQuery) -> PerformanceResponse:
    """Generate tax report"""
    # For hackathon, return current status
    # In production, would calculate realized gains/losses
    return await _get_portfolio_status(msg)


def _simulate_positions(portfolio: Dict) -> List[PositionDetail]:
    """
    Simulate current positions with price changes

    In production, this would:
    1. Query on-chain positions
    2. Get current token prices from oracles
    3. Calculate real P&L
    """
    positions = []

    for position_data in portfolio.get("positions", []):
        # Simulate price change (random between -10% to +30%)
        import random
        price_change = random.uniform(-0.10, 0.30)

        entry_value = position_data["entry_value"]
        current_value = entry_value * (1 + price_change)
        pnl = current_value - entry_value
        pnl_pct = (pnl / entry_value * 100) if entry_value > 0 else 0.0

        # Calculate days held (for demo, use random 1-30 days)
        days_held = random.randint(1, 30)

        position = PositionDetail(
            protocol=position_data["protocol"],
            chain=position_data["chain"],
            amount=position_data["amount"],
            entry_value=entry_value,
            current_value=current_value,
            pnl=pnl,
            pnl_percentage=pnl_pct,
            current_apy=position_data.get("current_apy", 5.0),
            days_held=days_held
        )
        positions.append(position)

    return positions


def update_user_portfolio(user_id: str, allocations: List, total_gas: float):
    """
    Update user portfolio after execution
    Called by coordinator after successful execution
    """
    positions = []
    for alloc in allocations:
        positions.append({
            "protocol": alloc.protocol,
            "chain": alloc.chain,
            "amount": alloc.amount,
            "entry_value": alloc.amount * 2000,  # Assume ETH = $2000
            "current_apy": alloc.expected_apy
        })

    user_portfolios[user_id] = {
        "positions": positions,
        "total_gas_spent": total_gas,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

    logger.info(f"📝 Updated portfolio for user {user_id}: {len(positions)} positions")


if __name__ == "__main__":
    logger.info("\n📊 Starting Performance Tracker Agent...\n")
    performance_agent.run()
