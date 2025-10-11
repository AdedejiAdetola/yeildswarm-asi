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
from protocols.messages import (
    StrategyRequest as ProtocolStrategyRequest,
    StrategyResponse, AllocationItem, Opportunity
)
from datetime import datetime, timezone
from uuid import uuid4
import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import uvicorn


# Create Strategy Engine Agent (Mailbox Mode for Agentverse)
strategy_engine = Agent(
    name="yieldswarm-strategy",
    seed=config.STRATEGY_SEED,
    port=config.STRATEGY_PORT,
    mailbox=f"{config.STRATEGY_MAILBOX_KEY}@https://agentverse.ai",
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


# ===== MESSAGE HANDLERS FOR INTER-AGENT COMMUNICATION =====

@strategy_engine.on_message(model=StrategyRequest)
async def generate_strategy(ctx: Context, sender: str, msg: StrategyRequest):
    """
    Generate optimal investment strategy based on opportunities and constraints

    Pattern: @agent.on_message(model=MessageModel)
    """
    ctx.logger.info(f"⚙️  Received strategy request from {sender}")
    ctx.logger.info(f"   Request ID: {msg.request_id}")
    ctx.logger.info(f"   User: {msg.investment_request.user_id}")
    ctx.logger.info(f"   Amount: {msg.investment_request.amount} {msg.investment_request.currency}")
    ctx.logger.info(f"   Risk Level: {msg.investment_request.risk_level.value}")
    ctx.logger.info(f"   Opportunities: {len(msg.opportunities)}")

    try:
        # Generate optimal strategy using opportunities
        strategy = optimizer.calculate_optimal_strategy(
            msg.investment_request,
            msg.opportunities,
            msg.metta_knowledge
        )

        ctx.logger.info(f"✅ Strategy generated successfully")
        ctx.logger.info(f"   Strategy ID: {strategy.strategy_id}")
        ctx.logger.info(f"   Actions: {len(strategy.actions)}")
        ctx.logger.info(f"   Expected APY: {strategy.expected_apy:.2f}%")
        ctx.logger.info(f"   Risk Score: {strategy.risk_score:.2f}")
        ctx.logger.info(f"   Estimated Gas: {strategy.estimated_gas_cost:.6f} ETH")

        # Send strategy back to coordinator
        await ctx.send(sender, strategy)
        ctx.logger.info(f"📤 Sent strategy to {sender}")

    except Exception as e:
        ctx.logger.error(f"❌ Error generating strategy: {str(e)}")
        # Send error response - create a minimal strategy with error info
        error_strategy = Strategy(
            strategy_id=str(uuid4()),
            user_id=msg.investment_request.user_id,
            total_amount=msg.investment_request.amount,
            actions=[],
            expected_apy=0.0,
            risk_score=0.0,
            estimated_gas_cost=0.0,
            created_at=datetime.now(timezone.utc)
        )
        await ctx.send(sender, error_strategy)


# ===== HTTP API ENDPOINTS (for Coordinator integration) =====

http_app = FastAPI(title="Strategy Engine HTTP API")

http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_app.get("/")
async def http_root():
    """Health check"""
    return {
        "status": "online",
        "service": "Strategy Engine",
        "agent_address": str(strategy_engine.address),
        "optimization": "multi-objective"
    }


@http_app.post("/generate_strategy")
async def http_generate_strategy(request: Request):
    """HTTP endpoint to generate strategy (called by Coordinator)"""
    try:
        data = await request.json()
        strategy_request = ProtocolStrategyRequest(**data)

        # Convert protocol messages to internal models
        investment_req = InvestmentRequest(
            user_id=strategy_request.user_id,
            amount=strategy_request.amount,
            currency=strategy_request.currency,
            risk_level=strategy_request.risk_level,
            preferred_chains=strategy_request.preferred_chains
        )

        # Convert opportunities
        opportunities = [
            YieldOpportunity(
                protocol=opp.protocol,
                chain=opp.chain,
                apy=opp.apy,
                tvl=opp.tvl,
                risk_score=opp.risk_score
            )
            for opp in strategy_request.opportunities
        ]

        # Generate strategy using optimizer
        strategy = optimizer.calculate_optimal_strategy(
            investment_req,
            opportunities,
            strategy_request.metta_insights
        )

        # Convert strategy actions to allocation items
        allocations = []
        for action in strategy.actions:
            if action.action_type == "deposit":
                allocations.append(AllocationItem(
                    protocol=action.protocol,
                    chain=action.chain,
                    amount=action.amount,
                    percentage=(action.amount / strategy.total_amount) * 100,
                    expected_apy=action.expected_apy,
                    risk_score=0.0  # Will be filled from opportunity data
                ))

        # Update risk scores from opportunities
        protocol_risk_map = {opp.protocol: opp.risk_score for opp in strategy_request.opportunities}
        for alloc in allocations:
            alloc.risk_score = protocol_risk_map.get(alloc.protocol, 5.0)

        # Build response
        response = StrategyResponse(
            request_id=strategy_request.request_id,
            user_id=strategy_request.user_id,
            allocations=allocations,
            total_amount=strategy.total_amount,
            expected_portfolio_apy=strategy.expected_apy,
            portfolio_risk_score=strategy.risk_score,
            reasoning=f"Optimized allocation using {len(allocations)} protocols. "
                     f"Estimated gas: {strategy.estimated_gas_cost:.4f} ETH. "
                     f"Strategy favors {'safety' if investment_req.risk_level.value == 'conservative' else 'yield' if investment_req.risk_level.value == 'aggressive' else 'balance'}.",
            timestamp=strategy.created_at.isoformat()
        )

        return JSONResponse(response.dict())

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


def run_http_server():
    """Run HTTP server in background thread"""
    uvicorn.run(http_app, host="0.0.0.0", port=8003, log_level="warning")


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Strategy Engine Agent")
    print("=" * 60)
    print(f"Agent Address: {strategy_engine.address}")
    print(f"Port: {config.STRATEGY_PORT}")
    print(f"HTTP API: http://localhost:8003")
    print(f"Optimization: Multi-objective (yield, risk, gas)")
    print(f"Risk Profiles: {', '.join(config.RISK_PROFILES.keys())}")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting dual-mode agent (uAgents + HTTP)...\n")

    # Start HTTP server in background thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run the agent (this blocks)
    strategy_engine.run()
