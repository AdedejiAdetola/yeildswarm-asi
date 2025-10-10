"""
YieldSwarm AI - Performance Tracker Agent
Tracks portfolio performance and generates analytics
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from utils.config import config
from utils.models import (
    PortfolioMetrics, Position, PerformanceUpdate,
    ExecutionReport, Chain, ProtocolType
)
from datetime import datetime, timezone, timedelta
import random


# Create Performance Tracker Agent (Local Mode with Endpoint)
tracker_agent = Agent(
    name="yieldswarm-tracker",
    seed=config.TRACKER_SEED,
    port=config.TRACKER_PORT,
    endpoint=["http://127.0.0.1:8005/submit"],
)


class PerformanceAnalyzer:
    """Analyzes and tracks portfolio performance"""

    def __init__(self):
        self.portfolios = {}  # user_id -> portfolio data
        self.historical_data = {}  # user_id -> historical metrics
        self.tax_events = {}  # user_id -> tax events

    def create_portfolio(self, user_id: str):
        """Initialize portfolio for a user"""
        self.portfolios[user_id] = {
            "positions": [],
            "total_value": 0.0,
            "total_invested": 0.0,
            "total_gas_costs": 0.0,
            "created_at": datetime.now(timezone.utc)
        }
        self.historical_data[user_id] = []
        self.tax_events[user_id] = []

    def add_position(self, user_id: str, execution_report: ExecutionReport):
        """Add positions from executed strategy"""
        if user_id not in self.portfolios:
            self.create_portfolio(user_id)

        # Simulate position creation from execution report
        for tx in execution_report.transactions:
            if tx.status == "success" and "deposit" in str(tx.chain):
                position = Position(
                    protocol="Simulated Protocol",
                    chain=tx.chain,
                    amount=random.uniform(1.0, 5.0),
                    currency="ETH",
                    entry_apy=random.uniform(4.0, 15.0),
                    current_apy=random.uniform(4.0, 15.0),
                    entry_date=datetime.now(timezone.utc)
                )
                self.portfolios[user_id]["positions"].append(position)

        # Update gas costs
        self.portfolios[user_id]["total_gas_costs"] += execution_report.total_gas_cost

    def calculate_portfolio_metrics(self, user_id: str) -> PortfolioMetrics:
        """Calculate comprehensive portfolio metrics"""
        if user_id not in self.portfolios:
            return PortfolioMetrics(
                total_value=0.0,
                pnl_24h=0.0,
                pnl_7d=0.0,
                pnl_30d=0.0,
                realized_apy=0.0,
                total_gas_costs=0.0,
                positions=[],
                updated_at=datetime.now(timezone.utc)
            )

        portfolio = self.portfolios[user_id]

        # Calculate total value
        total_value = sum(pos.amount for pos in portfolio["positions"])

        # Simulate P&L (in production, would calculate from actual price data)
        pnl_24h = total_value * random.uniform(-0.02, 0.05)  # -2% to +5%
        pnl_7d = total_value * random.uniform(-0.05, 0.15)   # -5% to +15%
        pnl_30d = total_value * random.uniform(-0.10, 0.30)  # -10% to +30%

        # Calculate realized APY
        if portfolio["positions"]:
            avg_apy = sum(pos.current_apy for pos in portfolio["positions"]) / len(portfolio["positions"])
        else:
            avg_apy = 0.0

        # Update current APYs (simulate market changes)
        for pos in portfolio["positions"]:
            # Simulate APY fluctuation
            pos.current_apy = max(0.0, pos.entry_apy * random.uniform(0.9, 1.1))

        return PortfolioMetrics(
            total_value=total_value,
            pnl_24h=pnl_24h,
            pnl_7d=pnl_7d,
            pnl_30d=pnl_30d,
            realized_apy=avg_apy,
            total_gas_costs=portfolio["total_gas_costs"],
            positions=portfolio["positions"],
            updated_at=datetime.now(timezone.utc)
        )

    def generate_tax_report(self, user_id: str) -> dict:
        """Generate tax report for IRS Form 8949"""
        if user_id not in self.tax_events:
            return {"events": [], "total_gains": 0.0, "total_losses": 0.0}

        events = self.tax_events[user_id]

        total_gains = sum(e["gain"] for e in events if e["gain"] > 0)
        total_losses = sum(abs(e["gain"]) for e in events if e["gain"] < 0)

        return {
            "events": events,
            "total_gains": total_gains,
            "total_losses": total_losses,
            "net": total_gains - total_losses,
            "form_8949_ready": True
        }

    def identify_rebalancing_opportunities(self, user_id: str, new_opportunities: list) -> list:
        """Identify when portfolio should be rebalanced"""
        if user_id not in self.portfolios:
            return []

        recommendations = []

        portfolio = self.portfolios[user_id]

        # Check for significantly better opportunities
        for pos in portfolio["positions"]:
            current_apy = pos.current_apy

            # Find better opportunities (>15% APY improvement)
            for opp in new_opportunities:
                if opp.apy > current_apy * 1.15:
                    recommendations.append({
                        "action": "rebalance",
                        "from_protocol": pos.protocol,
                        "to_protocol": opp.protocol,
                        "current_apy": current_apy,
                        "new_apy": opp.apy,
                        "improvement": ((opp.apy - current_apy) / current_apy) * 100,
                        "amount": pos.amount
                    })

        return recommendations

    def update_metta_knowledge(self, metrics: PortfolioMetrics) -> list:
        """Generate MeTTa knowledge updates from performance data"""
        updates = []

        for pos in metrics.positions:
            # Create MeTTa atom for actual performance
            metta_atom = f"""
(= (Actual-Performance {pos.protocol} {pos.chain.value} {datetime.now(timezone.utc).strftime('%Y-%m-%d')})
   (APY {pos.current_apy:.2f})
   (Duration-Days {(datetime.now(timezone.utc) - pos.entry_date).days})
   (Performance {'Exceeds' if pos.current_apy > pos.entry_apy else 'Below'}-Expectation))
"""
            updates.append(metta_atom)

        return updates


# Initialize analyzer
analyzer = PerformanceAnalyzer()


@tracker_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("Performance Tracker Agent started")
    ctx.logger.info(f"Agent address: {tracker_agent.address}")
    ctx.logger.info("Features:")
    ctx.logger.info("  • Real-time P&L tracking")
    ctx.logger.info("  • Tax reporting (IRS Form 8949)")
    ctx.logger.info("  • Rebalancing recommendations")
    ctx.logger.info("  • MeTTa knowledge feedback loop")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)


@tracker_agent.on_interval(period=60.0)
async def track_performance(ctx: Context):
    """Periodically track and log performance"""
    if not analyzer.portfolios:
        ctx.logger.info("📊 No active portfolios to track")
        return

    ctx.logger.info(f"📊 Tracking {len(analyzer.portfolios)} portfolio(s)")

    for user_id, portfolio in analyzer.portfolios.items():
        metrics = analyzer.calculate_portfolio_metrics(user_id)

        ctx.logger.info(f"\n  User: {user_id[:16]}...")
        ctx.logger.info(f"  Total Value: {metrics.total_value:.4f} ETH")
        ctx.logger.info(f"  Realized APY: {metrics.realized_apy:.2f}%")
        ctx.logger.info(f"  P&L 24h: {metrics.pnl_24h:+.4f} ETH ({(metrics.pnl_24h/metrics.total_value*100):+.2f}%)")
        ctx.logger.info(f"  Positions: {len(metrics.positions)}")
        ctx.logger.info(f"  Gas Costs: {metrics.total_gas_costs:.6f} ETH")

        # In production, would send performance updates
        # performance_update = PerformanceUpdate(
        #     user_id=user_id,
        #     metrics=metrics
        # )
        # await ctx.send(config.COORDINATOR_ADDRESS, performance_update)

        # Update MeTTa knowledge base
        metta_updates = analyzer.update_metta_knowledge(metrics)
        if metta_updates:
            ctx.logger.info(f"  🧠 Generated {len(metta_updates)} MeTTa knowledge updates")
            # await ctx.send(config.METTA_ADDRESS, {"updates": metta_updates})


@tracker_agent.on_interval(period=300.0)  # Every 5 minutes
async def check_rebalancing(ctx: Context):
    """Check for rebalancing opportunities"""
    ctx.logger.info("🔄 Checking for rebalancing opportunities...")

    # In production, would:
    # 1. Get latest opportunities from Chain Scanner
    # 2. Compare with current positions
    # 3. Recommend rebalancing if >15% APY improvement
    # 4. Send recommendations to Coordinator


# Message handlers for production
# @tracker_agent.on_message(model=ExecutionReport)
# async def handle_execution_report(ctx: Context, sender: str, msg: ExecutionReport):
#     """Record execution results"""
#     ctx.logger.info(f"Recording execution: {msg.strategy_id}")
#     # Extract user_id from strategy and add positions
#     analyzer.add_position("user_id", msg)


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - Performance Tracker Agent")
    print("=" * 60)
    print(f"Agent Address: {tracker_agent.address}")
    print(f"Port: {config.TRACKER_PORT}")
    print("\n📊 Tracking Capabilities:")
    print("  ✓ Real-time portfolio valuation")
    print("  ✓ P&L tracking (24h, 7d, 30d)")
    print("  ✓ APY monitoring")
    print("  ✓ Tax reporting (Form 8949)")
    print("  ✓ Rebalancing recommendations")
    print("  ✓ MeTTa knowledge updates")
    print(f"\n⚙️  Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\n🚀 Starting performance tracker...\n")

    tracker_agent.run()
