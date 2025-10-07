"""
YieldSwarm AI - Configuration Management
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration for all agents"""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Agent Seeds
    COORDINATOR_SEED = os.getenv("COORDINATOR_SEED", "coordinator-dev-seed")
    SCANNER_SEED = os.getenv("SCANNER_SEED", "scanner-dev-seed")
    METTA_SEED = os.getenv("METTA_SEED", "metta-dev-seed")
    STRATEGY_SEED = os.getenv("STRATEGY_SEED", "strategy-dev-seed")
    EXECUTION_SEED = os.getenv("EXECUTION_SEED", "execution-dev-seed")
    TRACKER_SEED = os.getenv("TRACKER_SEED", "tracker-dev-seed")

    # Mailbox Keys
    COORDINATOR_MAILBOX_KEY = os.getenv("COORDINATOR_MAILBOX_KEY", "")
    SCANNER_MAILBOX_KEY = os.getenv("SCANNER_MAILBOX_KEY", "")
    METTA_MAILBOX_KEY = os.getenv("METTA_MAILBOX_KEY", "")
    STRATEGY_MAILBOX_KEY = os.getenv("STRATEGY_MAILBOX_KEY", "")
    EXECUTION_MAILBOX_KEY = os.getenv("EXECUTION_MAILBOX_KEY", "")
    TRACKER_MAILBOX_KEY = os.getenv("TRACKER_MAILBOX_KEY", "")

    # RPC Endpoints
    RPC_ENDPOINTS = {
        "ethereum": os.getenv("ETHEREUM_RPC", "https://eth-mainnet.g.alchemy.com/v2/demo"),
        "solana": os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com"),
        "bsc": os.getenv("BSC_RPC", "https://bsc-dataseed.binance.org/"),
        "polygon": os.getenv("POLYGON_RPC", "https://polygon-rpc.com"),
        "arbitrum": os.getenv("ARBITRUM_RPC", "https://arb1.arbitrum.io/rpc"),
    }

    # Testnet RPC Endpoints
    TESTNET_RPC_ENDPOINTS = {
        "sepolia": os.getenv("SEPOLIA_RPC", "https://eth-sepolia.g.alchemy.com/v2/demo"),
        "solana_devnet": os.getenv("SOLANA_DEVNET_RPC", "https://api.devnet.solana.com"),
        "bsc_testnet": os.getenv("BSC_TESTNET_RPC", "https://data-seed-prebsc-1-s1.binance.org:8545/"),
        "mumbai": os.getenv("MUMBAI_RPC", "https://rpc-mumbai.maticvigil.com"),
        "arbitrum_sepolia": os.getenv("ARBITRUM_SEPOLIA_RPC", "https://sepolia-rollup.arbitrum.io/rpc"),
    }

    # Agent Ports
    COORDINATOR_PORT = 8000
    SCANNER_PORT = 8001
    METTA_PORT = 8002
    STRATEGY_PORT = 8003
    EXECUTION_PORT = 8004
    TRACKER_PORT = 8005

    # Agent Addresses (will be set after agent creation)
    COORDINATOR_ADDRESS = ""
    SCANNER_ADDRESS = ""
    METTA_ADDRESS = ""
    STRATEGY_ADDRESS = ""
    EXECUTION_ADDRESS = ""
    TRACKER_ADDRESS = ""

    # DeFi Protocols
    SUPPORTED_PROTOCOLS = [
        "Uniswap",
        "Aave",
        "Compound",
        "PancakeSwap",
        "Raydium",
        "Curve",
        "Balancer",
        "SushiSwap",
    ]

    # Risk Profiles
    RISK_PROFILES = {
        "conservative": {"max_risk_score": 2.0, "min_apy": 2.0},
        "moderate": {"max_risk_score": 5.0, "min_apy": 4.0},
        "aggressive": {"max_risk_score": 8.0, "min_apy": 8.0},
    }

    @classmethod
    def get_rpc_endpoint(cls, chain: str) -> str:
        """Get RPC endpoint for a chain based on environment"""
        if cls.ENVIRONMENT == "testnet":
            return cls.TESTNET_RPC_ENDPOINTS.get(chain, "")
        return cls.RPC_ENDPOINTS.get(chain, "")

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return cls.ENVIRONMENT == "production"

    @classmethod
    def is_testnet(cls) -> bool:
        """Check if running on testnet"""
        return cls.ENVIRONMENT == "testnet"

# Create singleton instance
config = Config()
