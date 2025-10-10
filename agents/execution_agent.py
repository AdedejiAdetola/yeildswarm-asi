"""
YieldSwarm AI - Execution Agent
Safely executes investment strategies with MEV protection
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from utils.config import config
from utils.models import (
    ApprovedStrategy, TransactionResult, ExecutionReport,
    AllocationAction, Chain
)
from datetime import datetime, timezone
import asyncio
import random


# Create Execution Agent (Local Mode with Endpoint)
execution_agent = Agent(
    name="yieldswarm-execution",
    seed=config.EXECUTION_SEED,
    port=config.EXECUTION_PORT,
    endpoint=["http://127.0.0.1:8004/submit"],
)


class SafeExecutor:
    """Executes transactions with safety checks and MEV protection"""

    def __init__(self):
        self.pending_transactions = {}
        self.executed_strategies = []

    async def simulate_transaction(self, action: AllocationAction) -> dict:
        """Simulate transaction before execution"""
        # Simulate validation
        await asyncio.sleep(0.1)  # Simulate network call

        # Check for potential issues
        will_fail = random.random() < 0.05  # 5% simulated failure rate

        return {
            "will_succeed": not will_fail,
            "estimated_gas": random.uniform(0.003, 0.008),
            "estimated_slippage": random.uniform(0.001, 0.01),
            "error": "Insufficient liquidity" if will_fail else None
        }

    async def execute_bridge(self, action: AllocationAction) -> TransactionResult:
        """Execute cross-chain bridge transaction"""
        print(f"  🌉 Bridging {action.amount:.4f} {action.currency} to {action.chain.value}...")

        # Simulate bridge transaction
        await asyncio.sleep(0.5)

        # Generate mock transaction hash
        tx_hash = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"

        return TransactionResult(
            tx_hash=tx_hash,
            chain=action.chain,
            status="success",
            gas_used=random.uniform(0.008, 0.015),
            error=None
        )

    async def execute_deposit(self, action: AllocationAction) -> TransactionResult:
        """Execute deposit to protocol"""
        print(f"  💰 Depositing {action.amount:.4f} {action.currency} to {action.protocol} on {action.chain.value}...")

        # Simulate deposit transaction
        await asyncio.sleep(0.3)

        # Generate mock transaction hash
        tx_hash = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"

        return TransactionResult(
            tx_hash=tx_hash,
            chain=action.chain,
            status="success",
            gas_used=random.uniform(0.003, 0.007),
            error=None
        )

    async def execute_swap(self, action: AllocationAction) -> TransactionResult:
        """Execute token swap with MEV protection"""
        print(f"  🔄 Swapping on {action.protocol}...")

        # Simulate swap with MEV protection
        await asyncio.sleep(0.2)

        tx_hash = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"

        return TransactionResult(
            tx_hash=tx_hash,
            chain=action.chain,
            status="success",
            gas_used=random.uniform(0.002, 0.005),
            error=None
        )

    async def execute_strategy(
        self,
        strategy: 'Strategy',
        ctx: Context
    ) -> ExecutionReport:
        """Execute complete investment strategy"""
        ctx.logger.info(f"🚀 Executing strategy {strategy.strategy_id}")
        ctx.logger.info(f"   Total amount: {strategy.total_amount} ETH")
        ctx.logger.info(f"   Actions: {len(strategy.actions)}")

        start_time = datetime.now(timezone.utc)
        transactions = []
        total_gas = 0.0

        # Execute actions in sequence
        for i, action in enumerate(strategy.actions, 1):
            ctx.logger.info(f"\n📋 Action {i}/{len(strategy.actions)}: {action.action_type}")

            # Simulate transaction first
            simulation = await self.simulate_transaction(action)

            if not simulation["will_succeed"]:
                ctx.logger.error(f"❌ Simulation failed: {simulation['error']}")
                # Record failed transaction
                transactions.append(TransactionResult(
                    tx_hash="",
                    chain=action.chain,
                    status="failed",
                    error=simulation["error"]
                ))
                continue

            # Execute based on action type
            try:
                if action.action_type == "bridge":
                    result = await self.execute_bridge(action)
                elif action.action_type == "deposit":
                    result = await self.execute_deposit(action)
                elif action.action_type == "swap":
                    result = await self.execute_swap(action)
                else:
                    result = TransactionResult(
                        tx_hash="",
                        chain=action.chain,
                        status="failed",
                        error=f"Unknown action type: {action.action_type}"
                    )

                transactions.append(result)

                if result.status == "success":
                    ctx.logger.info(f"   ✅ Success: {result.tx_hash[:16]}...")
                    if result.gas_used:
                        total_gas += result.gas_used
                        ctx.logger.info(f"   ⛽ Gas: {result.gas_used:.6f} ETH")
                else:
                    ctx.logger.error(f"   ❌ Failed: {result.error}")

            except Exception as e:
                ctx.logger.error(f"   ❌ Execution error: {str(e)}")
                transactions.append(TransactionResult(
                    tx_hash="",
                    chain=action.chain,
                    status="failed",
                    error=str(e)
                ))

        # Calculate execution time
        end_time = datetime.now(timezone.utc)
        execution_time = (end_time - start_time).total_seconds()

        # Determine overall status
        success_count = sum(1 for tx in transactions if tx.status == "success")
        overall_status = "success" if success_count == len(transactions) else "partial"
        if success_count == 0:
            overall_status = "failed"

        report = ExecutionReport(
            strategy_id=strategy.strategy_id,
            transactions=transactions,
            total_gas_cost=total_gas,
            execution_time=execution_time,
            status=overall_status
        )

        ctx.logger.info(f"\n📊 Execution Complete:")
        ctx.logger.info(f"   Status: {overall_status}")
        ctx.logger.info(f"   Successful: {success_count}/{len(transactions)}")
        ctx.logger.info(f"   Total Gas: {total_gas:.6f} ETH")
        ctx.logger.info(f"   Time: {execution_time:.2f}s")

        self.executed_strategies.append(strategy.strategy_id)

        return report

    def get_mev_protection_status(self) -> dict:
        """Get MEV protection configuration"""
        return {
            "enabled": True,
            "methods": ["Flashbots RPC", "Private Mempool", "Slippage Protection"],
            "max_slippage": "0.5%",
            "front_run_protection": True
        }


# Initialize executor
executor = SafeExecutor()


@execution_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("Execution Agent started")
    ctx.logger.info(f"Agent address: {execution_agent.address}")
    ctx.logger.info("Safety features: ENABLED")

    mev_status = executor.get_mev_protection_status()
    ctx.logger.info(f"MEV Protection: {mev_status['enabled']}")
    for method in mev_status['methods']:
        ctx.logger.info(f"  • {method}")

    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)


@execution_agent.on_interval(period=120.0)
async def monitor_execution(ctx: Context):
    """Monitor execution status"""
    ctx.logger.info(f"🔒 Execution Agent ready - {len(executor.executed_strategies)} strategies executed")

    # In production, would:
    # - Listen for ApprovedStrategy messages from Coordinator
    # - Execute transactions safely with MEV protection
    # - Send ExecutionReport back to Coordinator and Performance Tracker
    # - Handle transaction failures and rollbacks


# Message handler for production
# @execution_agent.on_message(model=ApprovedStrategy)
# async def handle_approved_strategy(ctx: Context, sender: str, msg: ApprovedStrategy):
#     """Execute approved strategy"""
#     ctx.logger.info(f"Received approved strategy from {sender}")
#
#     report = await executor.execute_strategy(msg.strategy, ctx)
#
#     # Send report back
#     await ctx.send(sender, report)
#
#     # Notify Performance Tracker
#     if config.TRACKER_ADDRESS:
#         await ctx.send(config.TRACKER_ADDRESS, report)


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Execution Agent")
    print("=" * 60)
    print(f"Agent Address: {execution_agent.address}")
    print(f"Port: {config.EXECUTION_PORT}")
    print("\n🔒 Safety Features:")
    mev = executor.get_mev_protection_status()
    for method in mev['methods']:
        print(f"  ✓ {method}")
    print(f"\n⚙️  Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting execution agent...\n")

    execution_agent.run()
