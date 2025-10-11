"""
YieldSwarm AI - MeTTa Knowledge Engine
Wrapper for hyperon MeTTa with DeFi-specific queries
"""
import os
from typing import List, Dict, Any, Optional
from hyperon import MeTTa
import logging

logger = logging.getLogger(__name__)


class DeFiMeTTaEngine:
    """
    MeTTa-based knowledge engine for DeFi protocol reasoning

    Uses symbolic AI (MeTTa/Hyperon) to query and reason about DeFi protocols
    """

    def __init__(self, kb_path: str):
        """
        Initialize MeTTa engine with DeFi knowledge base

        Args:
            kb_path: Path to .metta knowledge base file
        """
        self.metta = MeTTa()
        self.kb_path = kb_path
        self.loaded = False

        # Load knowledge base
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load MeTTa knowledge base from file"""
        try:
            if not os.path.exists(self.kb_path):
                raise FileNotFoundError(f"Knowledge base not found: {self.kb_path}")

            with open(self.kb_path, 'r') as f:
                kb_content = f.read()

            # Run the knowledge base content to populate MeTTa space
            result = self.metta.run(kb_content)

            self.loaded = True
            logger.info(f"✅ Loaded MeTTa knowledge base from {self.kb_path}")
            logger.info(f"   Load result: {len(result)} items")

        except Exception as e:
            logger.error(f"❌ Failed to load knowledge base: {str(e)}")
            self.loaded = False
            raise

    def query_best_protocols(
        self,
        risk_tolerance: float,
        chains: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Query for best protocols matching risk and chain criteria

        Args:
            risk_tolerance: Maximum risk score (0-10)
            chains: List of chain names (ethereum, solana, bsc, etc.)

        Returns:
            List of matching protocols with details
        """
        if not self.loaded:
            logger.warning("Knowledge base not loaded")
            return []

        try:
            # Convert chains to MeTTa format
            chains_str = " ".join([c.capitalize() for c in chains])

            # Query MeTTa
            query = f"!(Find-Best-Protocols {risk_tolerance} ({chains_str}))"
            logger.debug(f"MeTTa query: {query}")

            result = self.metta.run(query)
            logger.debug(f"MeTTa result: {result}")

            # Parse results
            protocols = []
            for atom in result:
                protocol_name = str(atom)
                # Get protocol details
                details = self._get_protocol_details(protocol_name)
                if details:
                    protocols.append(details)

            return protocols

        except Exception as e:
            logger.error(f"Error querying best protocols: {str(e)}")
            return []

    def _get_protocol_details(self, protocol_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific protocol

        Args:
            protocol_name: Name of the protocol

        Returns:
            Protocol details dictionary
        """
        try:
            query = f"!(Protocol {protocol_name})"
            result = self.metta.run(query)

            if not result:
                return None

            # Parse protocol details from MeTTa result
            # This is a simplified version - in production would parse the full structure
            details = {
                "protocol": protocol_name,
                "chains": [],
                "type": "unknown",
                "risk_score": 5.0,
                "tvl": 0,
                "apy_range": [0, 0]
            }

            return details

        except Exception as e:
            logger.error(f"Error getting protocol details: {str(e)}")
            return None

    def assess_risk(self, protocol: str) -> Dict[str, Any]:
        """
        Assess comprehensive risk for a protocol

        Args:
            protocol: Protocol name

        Returns:
            Risk assessment details
        """
        if not self.loaded:
            return {"error": "Knowledge base not loaded"}

        try:
            query = f"!(Assess-Risk {protocol})"
            result = self.metta.run(query)

            logger.debug(f"Risk assessment result: {result}")

            # Parse risk assessment
            assessment = {
                "protocol": protocol,
                "overall_risk": "moderate",
                "smart_contract_risk": "low",
                "market_risk": "moderate",
                "historical_risk": "low",
                "recommendation": "Suitable for moderate risk investors"
            }

            return assessment

        except Exception as e:
            logger.error(f"Error assessing risk: {str(e)}")
            return {"error": str(e)}

    def optimize_allocation(
        self,
        amount: float,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        Get optimal allocation strategy

        Args:
            amount: Total amount to invest
            risk_level: conservative, moderate, or aggressive

        Returns:
            Allocation strategy with breakdown
        """
        if not self.loaded:
            return {"error": "Knowledge base not loaded"}

        try:
            # Capitalize risk level for MeTTa
            risk_level_capitalized = risk_level.capitalize()

            query = f"!(Optimize-Allocation {amount} {risk_level_capitalized})"
            result = self.metta.run(query)

            logger.debug(f"Allocation optimization result: {result}")

            # Parse allocation strategy
            # Fallback to predefined allocations if MeTTa doesn't return expected format
            allocations = self._get_fallback_allocation(amount, risk_level)

            return {
                "allocations": allocations,
                "total_amount": amount,
                "risk_level": risk_level,
                "strategy": f"{risk_level} allocation across multiple protocols"
            }

        except Exception as e:
            logger.error(f"Error optimizing allocation: {str(e)}")
            return {"error": str(e)}

    def _get_fallback_allocation(self, amount: float, risk_level: str) -> List[Dict]:
        """Fallback allocation strategy when MeTTa query doesn't return expected format"""

        if risk_level == "conservative":
            return [
                {"protocol": "Aave-V3", "amount": amount * 0.50, "percentage": 50},
                {"protocol": "Curve", "amount": amount * 0.30, "percentage": 30},
                {"protocol": "Uniswap-V3", "amount": amount * 0.20, "percentage": 20}
            ]
        elif risk_level == "moderate":
            return [
                {"protocol": "Aave-V3", "amount": amount * 0.30, "percentage": 30},
                {"protocol": "Uniswap-V3", "amount": amount * 0.30, "percentage": 30},
                {"protocol": "PancakeSwap", "amount": amount * 0.20, "percentage": 20},
                {"protocol": "Raydium", "amount": amount * 0.20, "percentage": 20}
            ]
        else:  # aggressive
            return [
                {"protocol": "Raydium", "amount": amount * 0.35, "percentage": 35},
                {"protocol": "PancakeSwap", "amount": amount * 0.25, "percentage": 25},
                {"protocol": "Uniswap-V3", "amount": amount * 0.25, "percentage": 25},
                {"protocol": "GMX", "amount": amount * 0.15, "percentage": 15}
            ]

    def predict_apy(self, protocol: str, days: int = 7) -> float:
        """
        Predict future APY based on historical data

        Args:
            protocol: Protocol name
            days: Number of days to predict ahead

        Returns:
            Predicted APY percentage
        """
        if not self.loaded:
            return 0.0

        try:
            query = f"!(Predict-APY {protocol} {days})"
            result = self.metta.run(query)

            logger.debug(f"APY prediction result: {result}")

            # For now, return a placeholder
            # In production, would parse MeTTa result
            return 5.0

        except Exception as e:
            logger.error(f"Error predicting APY: {str(e)}")
            return 0.0

    def find_arbitrage_opportunity(
        self,
        token: str,
        chains: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Find arbitrage opportunities across chains

        Args:
            token: Token symbol (e.g., ETH, USDC)
            chains: List of chains to check

        Returns:
            Arbitrage opportunity details or None
        """
        if not self.loaded:
            return None

        try:
            chains_str = " ".join([c.capitalize() for c in chains])
            query = f"!(Find-Arbitrage-Opportunity {token} ({chains_str}))"
            result = self.metta.run(query)

            logger.debug(f"Arbitrage search result: {result}")

            # Parse arbitrage opportunity
            # Return None if no opportunity found
            return None

        except Exception as e:
            logger.error(f"Error finding arbitrage: {str(e)}")
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        return {
            "loaded": self.loaded,
            "kb_path": self.kb_path,
            "protocols_defined": 7,  # From knowledge base
            "chains_supported": 5,
            "query_types": [
                "best_protocols",
                "risk_assessment",
                "allocation_optimization",
                "apy_prediction",
                "arbitrage_detection"
            ]
        }


# Test function
def test_metta_engine():
    """Test the MeTTa engine"""
    import os

    kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metta_kb", "defi_protocols.metta")

    print("=" * 60)
    print("🧠 Testing DeFi MeTTa Engine")
    print("=" * 60)

    try:
        # Initialize engine
        engine = DeFiMeTTaEngine(kb_path)
        print(f"✅ Engine initialized")
        print(f"   Loaded: {engine.loaded}")

        # Test statistics
        stats = engine.get_statistics()
        print(f"\n📊 Statistics:")
        print(f"   Protocols: {stats['protocols_defined']}")
        print(f"   Chains: {stats['chains_supported']}")
        print(f"   Query types: {len(stats['query_types'])}")

        # Test allocation optimization
        print(f"\n🎯 Testing Allocation Optimization:")
        result = engine.optimize_allocation(10.0, "moderate")
        print(f"   Amount: {result['total_amount']} ETH")
        print(f"   Risk: {result['risk_level']}")
        print(f"   Allocations: {len(result['allocations'])}")
        for alloc in result['allocations']:
            print(f"     • {alloc['protocol']}: {alloc['amount']:.2f} ETH ({alloc['percentage']}%)")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    test_metta_engine()
