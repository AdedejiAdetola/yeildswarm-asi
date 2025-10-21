"""
YieldSwarm AI - Execution Agent
AGENTVERSE DEPLOYMENT VERSION - Self-contained
"""
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import random

# ===== INLINE MESSAGE MODELS =====

class Chain(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"

class AllocationItem(BaseModel):
    protocol: str
    chain: str
    amount: float
    percentage: float
    expected_apy: float
    risk_score: float = 5.0

class StrategyResponse(BaseModel):
    request_id: str
    allocations: List[AllocationItem]
    expected_apy: float
    risk_score: float
    estimated_gas_cost: float
    reasoning: str
    timestamp: str

class ExecutionRequest(BaseModel):
    request_id: str
    user_id: str
    strategy: StrategyResponse
    user_wallet: str
    max_slippage: float = 0.5

class TransactionDetail(BaseModel):
    tx_hash: str
    chain: Chain
    protocol: str
    action: str
    amount: float
    status: str
    gas_used: Optional[float] = None
    timestamp: str

class ExecutionResponse(BaseModel):
    request_id: str
    user_id: str
    status: str
    transactions: List[TransactionDetail]
    total_gas_cost: float
    execution_time_seconds: float
    errors: List[str] = []

# ===== CONFIGURATION =====
EXECUTION_SEED = process.env.EXECUTION_SEED
EXECUTION_PORT = 8004

# ASI:One API Configuration
ASI_ONE_API_KEY = process.env.ASI_ONE_API_KEY

# ===== AGENT INITIALIZATION =====
try:
    execution_agent = agent  # type: ignore
except NameError:
    execution_agent = Agent(
        name="yieldswarm-execution",
        seed=EXECUTION_SEED,
        port=EXECUTION_PORT,
        mailbox=True,
        # NOTE: No endpoint for Agentverse - auto-configured
    )

# # Create chat protocol for ASI:One compatibility
# chat_protocol = Protocol(spec=chat_protocol_spec)

# # Include chat protocol with manifest publishing for ASI:One compatibility
# execution_agent.include(chat_protocol, publish_manifest=True)

# ===== MESSAGE HANDLER =====

@execution_agent.on_message(model=ExecutionRequest)
async def handle_execution_request(ctx: Context, sender: str, msg: ExecutionRequest):
    """Handle execution request from Portfolio Coordinator"""
    ctx.logger.info(f"📨 Received Execution Request: {msg.request_id}")
    ctx.logger.info(f"   User: {msg.user_id}")
    ctx.logger.info(f"   Wallet: {msg.user_wallet}")
    ctx.logger.info(f"   Allocations: {len(msg.strategy.allocations)}")

    try:
        # Simulate transaction execution
        response = _execute_strategy(msg)

        # Send response back to coordinator
        await ctx.send(sender, response)

        ctx.logger.info(f"✅ Sent Execution Response: {msg.request_id}")
        ctx.logger.info(f"   Status: {response.status}")
        ctx.logger.info(f"   Transactions: {len(response.transactions)}")

    except Exception as e:
        ctx.logger.error(f"❌ Error executing strategy: {str(e)}")
        error_response = ExecutionResponse(
            request_id=msg.request_id,
            user_id=msg.user_id,
            status="failed",
            transactions=[],
            total_gas_cost=0.0,
            execution_time_seconds=0.0,
            errors=[f"Execution error: {str(e)}"]
        )
        await ctx.send(sender, error_response)

def _execute_strategy(msg: ExecutionRequest) -> ExecutionResponse:
    """
    Execute portfolio strategy (SIMULATED)

    In production, this would:
    - Connect to Web3 providers
    - Execute real transactions
    - Monitor for MEV protection
    - Handle slippage and errors

    For demo: Simulates successful execution
    """

    transactions = []
    total_gas = 0.0
    start_time = datetime.now(timezone.utc)

    # Simulate transaction for each allocation
    for alloc in msg.strategy.allocations:
        # Generate simulated transaction hash
        tx_hash = _generate_tx_hash()

        # Estimate gas based on chain
        gas_used = _estimate_gas(alloc.chain)
        total_gas += gas_used

        # Create transaction detail
        tx = TransactionDetail(
            tx_hash=tx_hash,
            chain=Chain(alloc.chain.lower()) if isinstance(alloc.chain, str) else alloc.chain,
            protocol=alloc.protocol,
            action="deposit",
            amount=alloc.amount,
            status="confirmed",
            gas_used=gas_used,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        transactions.append(tx)

        ctx.logger.info(f"   ✅ Simulated TX: {alloc.protocol} - {alloc.amount:.2f} ETH")

    # Calculate execution time
    end_time = datetime.now(timezone.utc)
    execution_time = (end_time - start_time).total_seconds()

    return ExecutionResponse(
        request_id=msg.request_id,
        user_id=msg.user_id,
        status="success",
        transactions=transactions,
        total_gas_cost=total_gas,
        execution_time_seconds=execution_time,
        errors=[]
    )

def _generate_tx_hash() -> str:
    """Generate simulated transaction hash"""
    import hashlib
    random_data = f"{random.random()}{datetime.now(timezone.utc).isoformat()}"
    return "0x" + hashlib.sha256(random_data.encode()).hexdigest()

def _estimate_gas(chain: str) -> float:
    """Estimate gas cost based on chain"""
    gas_costs = {
        "ethereum": 0.015,
        "polygon": 0.0001,
        "arbitrum": 0.0008,
        "bsc": 0.0002,
        "solana": 0.00001
    }
    return gas_costs.get(chain.lower(), 0.01)

# ===== STARTUP EVENT HANDLER =====

@execution_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🔒 Execution Agent Started")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent Address: {execution_agent.address}")
    ctx.logger.info(f"Mailbox: Enabled ✓")
    ctx.logger.info(f"Mode: SIMULATION (Safe for demo)")
    ctx.logger.info(f"Capabilities: Transaction Execution, MEV Protection")
    ctx.logger.info("=" * 60)
    ctx.logger.info("✅ Ready to receive execution requests")

if __name__ == "__main__":
    print("\n🐝 YieldSwarm AI - Execution Agent")
    print(f"Address: {execution_agent.address}")
    print(f"Mailbox: Enabled\n")
    execution_agent.run()
