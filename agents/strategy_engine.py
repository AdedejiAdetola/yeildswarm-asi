"""
YieldSwarm AI - Strategy Engine Agent
Calculates optimal allocation strategies
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from utils.config import config
from utils.models import (
    StrategyRequest, Strategy, AllocationAction,
    YieldOpportunity, InvestmentRequest, Chain
)
from datetime import datetime, timezone
from uuid import uuid4
import random


# Create Strategy Engine Agent (Local Mode with Endpoint)
strategy_engine = Agent(
    name="yieldswarm-strategy",
    seed=config.STRATEGY_SEED,
    port=config.STRATEGY_PORT,
    endpoint=["http://127.0.0.1:8003/submit"],
)


class StrategyOptimizer:
    """Optimizes investment strategies based on opportunities and constraints"""

    @staticmethod
    def calculate_optimal_strategy(
        investment_req: InvestmentRequest,
        opportunities: list[YieldOpportunity],
        metta_knowledge: dict = None
    ) -> Strategy:
        """Calculate optimal allocation strategy"""

        # Filter opportunities by risk tolerance
        risk_limits = config.RISK_PROFILES[investment_req.risk_level.value]
        filtered_opps = [
            opp for opp in opportunities
            if opp.risk_score <= risk_limits["max_risk_score"]
            and opp.apy >= risk_limits["min_apy"]
        ]

        # Filter by preferred chains if specified
        if investment_req.preferred_chains:
            filtered_opps = [
                opp for opp in filtered_opps
                if opp.chain in investment_req.preferred_chains
            ]

        # Sort by risk-adjusted return (APY / Risk Score)
        filtered_opps.sort(
            key=lambda x: x.apy / max(x.risk_score, 1.0),
            reverse=True
        )

        # Select top opportunities based on risk level
        if investment_req.risk_level.value == "conservative":
            selected_opps = filtered_opps[:2]  # Conservative: 2 protocols
        elif investment_req.risk_level.value == "moderate":
            selected_opps = filtered_opps[:4]  # Moderate: 4 protocols
        else:
            selected_opps = filtered_opps[:5]  # Aggressive: 5 protocols

        # Calculate allocations
        actions = StrategyOptimizer._calculate_allocations(
            investment_req.amount,
            selected_opps,
            investment_req.risk_level.value
        )

        # Calculate expected metrics
        expected_apy = StrategyOptimizer._calculate_expected_apy(actions, selected_opps)
        risk_score = StrategyOptimizer._calculate_portfolio_risk(actions, selected_opps)
        estimated_gas = StrategyOptimizer._estimate_gas_costs(actions)

        return Strategy(
            strategy_id=str(uuid4()),
            user_id=investment_req.user_id,
            total_amount=investment_req.amount,
            actions=actions,
            expected_apy=expected_apy,
            risk_score=risk_score,
            estimated_gas_cost=estimated_gas,
            created_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def _calculate_allocations(
        total_amount: float,
        opportunities: list[YieldOpportunity],
        risk_level: str
    ) -> list[AllocationAction]:
        """Calculate allocation amounts for each opportunity"""
        if not opportunities:
            return []

        actions = []

        # Allocation weights based on risk level
        if risk_level == "conservative":
            # Equal weighted for safety
            weights = [1.0 / len(opportunities)] * len(opportunities)
        elif risk_level == "moderate":
            # Slightly favor higher APY
            total_apy = sum(opp.apy for opp in opportunities)
            weights = [opp.apy / total_apy for opp in opportunities]
        else:  # aggressive
            # Heavily favor highest APY
            sorted_opps = sorted(opportunities, key=lambda x: x.apy, reverse=True)
            if len(sorted_opps) == 1:
                weights = [1.0]
            else:
                # Top opportunity gets 40%, rest distributed
                weights = [0.40] + [0.60 / (len(sorted_opps) - 1)] * (len(sorted_opps) - 1)
                # Reorder weights to match original order
                weight_map = {opp: w for opp, w in zip(sorted_opps, weights)}
                weights = [weight_map[opp] for opp in opportunities]

        # Create allocation actions
        for opp, weight in zip(opportunities, weights):
            allocation_amount = total_amount * weight

            # Determine if cross-chain bridge needed
            action_type = "deposit"
            # Simplified: assume we need to bridge to non-Ethereum chains
            if opp.chain != Chain.ETHEREUM:
                # Create bridge action first
                bridge_action = AllocationAction(
                    action_type="bridge",
                    protocol=f"Bridge-to-{opp.chain.value}",
                    chain=opp.chain,
                    amount=allocation_amount,
                    currency="ETH",
                    expected_apy=0.0
                )
                actions.append(bridge_action)

            # Create deposit action
            deposit_action = AllocationAction(
                action_type="deposit",
                protocol=opp.protocol,
                chain=opp.chain,
                amount=allocation_amount,
                currency="ETH",
                expected_apy=opp.apy
            )
            actions.append(deposit_action)

        return actions

    @staticmethod
    def _calculate_expected_apy(
        actions: list[AllocationAction],
        opportunities: list[YieldOpportunity]
    ) -> float:
        """Calculate weighted expected APY"""
        total_amount = sum(a.amount for a in actions if a.action_type == "deposit")
        if total_amount == 0:
            return 0.0

        weighted_apy = sum(
            action.amount * action.expected_apy
            for action in actions
            if action.action_type == "deposit" and action.expected_apy
        )

        return weighted_apy / total_amount

    @staticmethod
    def _calculate_portfolio_risk(
        actions: list[AllocationAction],
        opportunities: list[YieldOpportunity]
    ) -> float:
        """Calculate overall portfolio risk score"""
        if not opportunities:
            return 0.0

        # Create protocol to opportunity mapping
        protocol_risk = {opp.protocol: opp.risk_score for opp in opportunities}

        # Calculate weighted risk
        total_amount = sum(a.amount for a in actions if a.action_type == "deposit")
        if total_amount == 0:
            return 0.0

        weighted_risk = sum(
            action.amount * protocol_risk.get(action.protocol, 5.0)
            for action in actions
            if action.action_type == "deposit"
        )

        return weighted_risk / total_amount

    @staticmethod
    def _estimate_gas_costs(actions: list[AllocationAction]) -> float:
        """Estimate total gas costs for all actions"""
        gas_estimates = {
            "deposit": 0.005,  # ~$15-20 on Ethereum
            "swap": 0.003,
            "bridge": 0.01,    # Higher for cross-chain
            "withdraw": 0.004
        }

        total_gas = sum(
            gas_estimates.get(action.action_type, 0.005)
            for action in actions
        )

        return total_gas


# Initialize optimizer
optimizer = StrategyOptimizer()


@strategy_engine.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("Strategy Engine Agent started")
    ctx.logger.info(f"Agent address: {strategy_engine.address}")
    ctx.logger.info("Optimization algorithms: ENABLED")
    ctx.logger.info(f"Risk profiles supported: {len(config.RISK_PROFILES)}")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)


@strategy_engine.on_interval(period=60.0)
async def monitor_strategies(ctx: Context):
    """Monitor and log strategy generation capabilities"""
    ctx.logger.info("⚙️  Strategy Engine ready to optimize allocations")

    # In production, would:
    # - Listen for StrategyRequest messages from Coordinator
    # - Query MeTTa Knowledge Agent for protocol intelligence
    # - Use real-time opportunity data from Chain Scanner
    # - Generate and send optimized strategies back to Coordinator


# Message handler for production
# @strategy_engine.on_message(model=StrategyRequest)
# async def generate_strategy(ctx: Context, sender: str, msg: StrategyRequest):
#     """Generate optimal investment strategy"""
#     ctx.logger.info(f"Generating strategy for {msg.investment_request.user_id}")
#
#     strategy = optimizer.calculate_optimal_strategy(
#         msg.investment_request,
#         msg.opportunities,
#         msg.metta_knowledge
#     )
#
#     ctx.logger.info(f"Strategy generated: {len(strategy.actions)} actions, "
#                     f"Expected APY: {strategy.expected_apy:.2f}%")
#
#     # Send back to coordinator
#     await ctx.send(sender, strategy)


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Strategy Engine Agent")
    print("=" * 60)
    print(f"Agent Address: {strategy_engine.address}")
    print(f"Port: {config.STRATEGY_PORT}")
    print(f"Optimization: Multi-objective (yield, risk, gas)")
    print(f"Risk Profiles: {', '.join(config.RISK_PROFILES.keys())}")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting strategy engine...\n")

    strategy_engine.run()
