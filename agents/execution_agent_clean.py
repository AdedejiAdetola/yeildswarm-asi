"""
YieldSwarm AI - Execution Agent (Clean)
Pure uAgents implementation for transaction execution
"""

import os
import sys
import logging
from datetime import datetime, timezone
from typing import List
import asyncio
from uuid import uuid4

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from protocols.messages import (
    ExecutionRequest,
    ExecutionResponse,
    TransactionDetail,
    AllocationItem
)
from utils.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Execution Agent
execution_agent = Agent(
    name="execution_agent",
    seed=config.EXECUTION_SEED,
    port=8004,
    endpoint=["http://0.0.0.0:8004/submit"]
)


@execution_agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    logger.info("=" * 60)
    logger.info("🚀 Execution Agent Starting")
    logger.info("=" * 60)
    logger.info(f"Agent Address: {ctx.agent.address}")
    logger.info(f"Port: 8004")
    logger.info(f"Coordinator: {config.COORDINATOR_ADDRESS}")
    logger.info("=" * 60)


@execution_agent.on_message(model=ExecutionRequest)
async def handle_execution_request(ctx: Context, sender: str, msg: ExecutionRequest):
    """
    Handle execution request from Portfolio Coordinator

    Process:
    1. Receive approved strategy
    2. Prepare transactions for each allocation
    3. Execute transactions on respective chains
    4. Monitor transaction status
    5. Return execution report

    NOTE: This is a SIMULATION for the hackathon.
    In production, this would integrate with Web3 providers:
    - ethers.js / web3.py for EVM chains
    - @solana/web3.js for Solana
    - Actual wallet signing and transaction broadcasting
    """
    logger.info("=" * 60)
    logger.info(f"📨 Received Execution Request: {msg.request_id}")
    logger.info(f"   From: {sender}")
    logger.info(f"   User: {msg.user_id}")
    logger.info(f"   Wallet: {msg.user_wallet}")
    logger.info(f"   Allocations: {len(msg.strategy.allocations)}")
    logger.info(f"   Max Slippage: {msg.max_slippage}%")
    logger.info("=" * 60)

    try:
        start_time = datetime.now(timezone.utc)

        # Execute transactions (simulated for hackathon)
        transactions = await _execute_transactions(msg)

        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()

        # Calculate total gas cost
        total_gas = sum(tx.gas_used or 0 for tx in transactions)
        # Convert to USD (assuming ETH = $2000)
        total_gas_usd = total_gas * 2000

        # Determine overall status
        confirmed_count = sum(1 for tx in transactions if tx.status == "confirmed")
        if confirmed_count == len(transactions):
            status = "success"
        elif confirmed_count > 0:
            status = "partial"
        else:
            status = "failed"

        # Create response
        response = ExecutionResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            status=status,
            transactions=transactions,
            total_gas_cost=total_gas_usd,
            execution_time_seconds=execution_time,
            errors=[]
        )

        # Send response back to coordinator
        await ctx.send(sender, response)

        logger.info(f"✅ Sent Execution Response: {msg.request_id}")
        logger.info(f"   Status: {status}")
        logger.info(f"   Transactions: {len(transactions)}")
        logger.info(f"   Total Gas: ${total_gas_usd:.4f}")
        logger.info(f"   Execution Time: {execution_time:.2f}s")

    except Exception as e:
        logger.error(f"❌ Error executing transactions: {str(e)}")
        # Send error response
        error_response = ExecutionResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            status="failed",
            transactions=[],
            total_gas_cost=0.0,
            execution_time_seconds=0.0,
            errors=[str(e)]
        )
        await ctx.send(sender, error_response)


async def _execute_transactions(msg: ExecutionRequest) -> List[TransactionDetail]:
    """
    Execute transactions for each allocation

    SIMULATION MODE for hackathon:
    - Generates mock transaction hashes
    - Simulates transaction confirmation
    - Returns realistic transaction details

    PRODUCTION MODE would:
    - Connect to Web3 providers (Infura, Alchemy, etc.)
    - Sign transactions with user's wallet
    - Broadcast to blockchain networks
    - Monitor transaction status
    - Handle reverts and failures
    """
    transactions = []

    for i, allocation in enumerate(msg.strategy.allocations):
        logger.info(f"   Executing {i+1}/{len(msg.strategy.allocations)}: "
                   f"{allocation.protocol} on {allocation.chain}")

        # Simulate transaction execution
        # In production, this would be actual blockchain interaction
        tx = await _simulate_transaction(
            allocation=allocation,
            user_wallet=msg.user_wallet,
            max_slippage=msg.max_slippage
        )

        transactions.append(tx)

        # Simulate network delay
        await asyncio.sleep(0.1)

    return transactions


async def _simulate_transaction(
    allocation: AllocationItem,
    user_wallet: str,
    max_slippage: float
) -> TransactionDetail:
    """
    Simulate a single transaction

    In production, this would:
    1. Get protocol contract addresses
    2. Encode transaction data (deposit, swap, etc.)
    3. Estimate gas
    4. Sign with user's wallet
    5. Broadcast transaction
    6. Wait for confirmation
    """

    # Generate mock transaction hash
    tx_hash = f"0x{uuid4().hex}"

    # Determine action type based on protocol
    action = "deposit"  # Could be deposit, swap, bridge, etc.

    # Simulate gas used based on chain
    gas_costs = {
        "ethereum": 0.008,
        "bsc": 0.0008,
        "polygon": 0.0004,
        "arbitrum": 0.0015,
        "solana": 0.00008
    }
    gas_used = gas_costs.get(allocation.chain.lower(), 0.005)

    # Simulate 95% success rate
    import random
    status = "confirmed" if random.random() > 0.05 else "failed"

    return TransactionDetail(
        tx_hash=tx_hash,
        chain=allocation.chain,
        protocol=allocation.protocol,
        action=action,
        amount=allocation.amount,
        status=status,
        gas_used=gas_used,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


if __name__ == "__main__":
    logger.info("\n🚀 Starting Execution Agent...\n")
    execution_agent.run()
