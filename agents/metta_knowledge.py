"""
YieldSwarm AI - MeTTa Knowledge Agent
Symbolic AI knowledge base for DeFi protocols using MeTTa/Hyperon
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
from utils.config import config
from utils.models import MeTTaQuery, ProtocolKnowledge
from datetime import datetime


# Create MeTTa Knowledge Agent
metta_agent = Agent(
    name="yieldswarm-metta",
    seed=config.METTA_SEED,
    port=config.METTA_PORT,
    mailbox=config.METTA_MAILBOX_KEY if config.METTA_MAILBOX_KEY else None,
)

# MeTTa Knowledge Base (simulation for now, would use actual MeTTa in production)
class DeFiKnowledgeBase:
    """Simulated MeTTa knowledge base"""

    def __init__(self):
        self.protocol_knowledge = {
            "Aave-V3": {
                "chains": ["ethereum", "polygon", "arbitrum"],
                "type": "lending",
                "risk_score": 2.0,
                "audited": True,
                "historical_apy": [3.5, 4.2, 4.8, 4.1, 5.2],
                "tvl": 5_000_000_000,
            },
            "Uniswap-V3": {
                "chains": ["ethereum", "polygon", "arbitrum"],
                "type": "dex",
                "risk_score": 3.5,
                "audited": True,
                "historical_apy": [8.0, 12.5, 15.2, 10.8, 13.5],
                "impermanent_loss": "high",
                "tvl": 3_200_000_000,
            },
            "Raydium": {
                "chains": ["solana"],
                "type": "dex",
                "risk_score": 5.5,
                "audited": True,
                "historical_apy": [15.0, 22.3, 25.8, 18.2, 20.5],
                "tvl": 450_000_000,
            },
            "PancakeSwap": {
                "chains": ["bsc"],
                "type": "dex",
                "risk_score": 5.0,
                "audited": True,
                "historical_apy": [10.0, 15.2, 18.5, 12.8, 16.2],
                "tvl": 1_200_000_000,
            },
            "Curve": {
                "chains": ["ethereum"],
                "type": "stablecoin-amm",
                "risk_score": 2.5,
                "audited": True,
                "historical_apy": [4.0, 5.2, 6.1, 4.8, 5.5],
                "impermanent_loss": "low",
                "tvl": 2_800_000_000,
            },
        }

    def query_best_protocols(self, risk_tolerance: float, chains: list) -> list:
        """Find best protocols based on risk and chains"""
        results = []

        for protocol, data in self.protocol_knowledge.items():
            # Filter by risk tolerance
            if data["risk_score"] > risk_tolerance:
                continue

            # Filter by chains
            if chains and not any(chain in data["chains"] for chain in chains):
                continue

            # Calculate average historical APY
            avg_apy = sum(data["historical_apy"]) / len(data["historical_apy"])

            results.append({
                "protocol": protocol,
                "chain": data["chains"][0],  # Primary chain
                "risk_score": data["risk_score"],
                "avg_apy": avg_apy,
                "tvl": data["tvl"],
                "type": data["type"],
            })

        # Sort by APY descending
        results.sort(key=lambda x: x["avg_apy"], reverse=True)
        return results

    def assess_risk(self, protocol: str) -> dict:
        """Assess comprehensive risk for a protocol"""
        if protocol not in self.protocol_knowledge:
            return {"error": f"Protocol {protocol} not found"}

        data = self.protocol_knowledge[protocol]

        return {
            "protocol": protocol,
            "overall_risk_score": data["risk_score"],
            "smart_contract_risk": "low" if data["audited"] else "high",
            "market_risk": "high" if data["type"] == "dex" else "moderate",
            "impermanent_loss_risk": data.get("impermanent_loss", "n/a"),
            "tvl": data["tvl"],
            "recommendation": self._get_risk_recommendation(data["risk_score"]),
        }

    def _get_risk_recommendation(self, score: float) -> str:
        """Get risk recommendation based on score"""
        if score <= 3.0:
            return "Suitable for conservative investors"
        elif score <= 5.0:
            return "Suitable for moderate risk tolerance"
        else:
            return "Only for aggressive investors"

    def get_allocation_strategy(self, amount: float, risk_level: str) -> dict:
        """Get optimal allocation strategy using MeTTa-like reasoning"""
        if risk_level == "conservative":
            return {
                "allocations": [
                    {"protocol": "Aave-V3", "chain": "ethereum", "percentage": 50, "amount": amount * 0.5},
                    {"protocol": "Curve", "chain": "ethereum", "percentage": 30, "amount": amount * 0.3},
                    {"protocol": "Uniswap-V3", "chain": "polygon", "percentage": 20, "amount": amount * 0.2},
                ],
                "expected_apy": 4.8,
                "risk_score": 2.3,
                "reasoning": "Low-risk allocation focused on audited lending protocols",
            }
        elif risk_level == "moderate":
            return {
                "allocations": [
                    {"protocol": "Aave-V3", "chain": "ethereum", "percentage": 30, "amount": amount * 0.3},
                    {"protocol": "Uniswap-V3", "chain": "ethereum", "percentage": 30, "amount": amount * 0.3},
                    {"protocol": "PancakeSwap", "chain": "bsc", "percentage": 20, "amount": amount * 0.2},
                    {"protocol": "Raydium", "chain": "solana", "percentage": 20, "amount": amount * 0.2},
                ],
                "expected_apy": 8.5,
                "risk_score": 4.0,
                "reasoning": "Balanced allocation across chains and protocol types",
            }
        else:  # aggressive
            return {
                "allocations": [
                    {"protocol": "Raydium", "chain": "solana", "percentage": 35, "amount": amount * 0.35},
                    {"protocol": "PancakeSwap", "chain": "bsc", "percentage": 25, "amount": amount * 0.25},
                    {"protocol": "Uniswap-V3", "chain": "ethereum", "percentage": 25, "amount": amount * 0.25},
                    {"protocol": "Uniswap-V3", "chain": "arbitrum", "percentage": 15, "amount": amount * 0.15},
                ],
                "expected_apy": 15.2,
                "risk_score": 5.8,
                "reasoning": "High-yield allocation prioritizing DEX protocols across multiple chains",
            }


# Initialize knowledge base
kb = DeFiKnowledgeBase()


@metta_agent.on_event("startup")
async def startup(ctx: Context):
    """Startup event handler"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("MeTTa Knowledge Agent started")
    ctx.logger.info(f"Agent address: {metta_agent.address}")
    ctx.logger.info(f"Knowledge base loaded: {len(kb.protocol_knowledge)} protocols")
    ctx.logger.info("MeTTa reasoning: ENABLED (simulated)")
    ctx.logger.info(f"Environment: {config.ENVIRONMENT}")
    ctx.logger.info("=" * 60)

    # Log loaded protocols
    for protocol in kb.protocol_knowledge.keys():
        ctx.logger.info(f"  ✓ {protocol}")


@metta_agent.on_interval(period=300.0)  # Update knowledge every 5 minutes
async def update_knowledge(ctx: Context):
    """Periodically update knowledge base with new data"""
    ctx.logger.info("🧠 Updating DeFi knowledge base...")

    # In production, would:
    # 1. Fetch latest protocol data from chains
    # 2. Update historical APY data
    # 3. Update TVL information
    # 4. Recompute risk scores
    # 5. Update MeTTa knowledge graph

    ctx.logger.info("✅ Knowledge base updated")


# Message handlers would go here for production
# @metta_agent.on_message(model=MeTTaQuery)
# async def handle_query(ctx: Context, sender: str, msg: MeTTaQuery):
#     ...


if __name__ == "__main__":
    print("=" * 60)
    print("YieldSwarm AI - MeTTa Knowledge Agent")
    print("=" * 60)
    print(f"Agent Address: {metta_agent.address}")
    print(f"Port: {config.METTA_PORT}")
    print(f"Protocols in Knowledge Base: {len(kb.protocol_knowledge)}")
    print(f"Environment: {config.ENVIRONMENT}")
    print("=" * 60)
    print("\nProtocols:")
    for protocol, data in kb.protocol_knowledge.items():
        print(f"  • {protocol}: Risk {data['risk_score']}, TVL ${data['tvl']:,}")
    print("\n🚀 Starting knowledge agent...\n")

    metta_agent.run()
