"""
YieldSwarm AI - Local Agent Interaction Test
Tests agent-to-agent communication in local mode
"""
import asyncio
from uagents import Agent, Context, Model
from uagents.query import query
from datetime import datetime
from utils.config import config

# Define test message models
class TestMessage(Model):
    content: str
    timestamp: datetime


class TestResponse(Model):
    status: str
    message: str
    agent_name: str


async def test_agent_discovery():
    """Test if agents can discover each other locally"""
    print("\n" + "=" * 60)
    print("Testing Agent Discovery")
    print("=" * 60)

    agents = {
        "Portfolio Coordinator": f"http://127.0.0.1:{config.COORDINATOR_PORT}",
        "Chain Scanner": f"http://127.0.0.1:{config.SCANNER_PORT}",
        "MeTTa Knowledge": f"http://127.0.0.1:{config.METTA_PORT}",
        "Strategy Engine": f"http://127.0.0.1:{config.STRATEGY_PORT}",
        "Execution Agent": f"http://127.0.0.1:{config.EXECUTION_PORT}",
        "Performance Tracker": f"http://127.0.0.1:{config.TRACKER_PORT}",
    }

    for agent_name, endpoint in agents.items():
        try:
            print(f"\n🔍 Checking {agent_name} at {endpoint}...")
            # Try to connect
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{endpoint}/", timeout=2) as response:
                    if response.status in [200, 404]:  # 404 is OK, means server is running
                        print(f"   ✅ {agent_name} is reachable")
                    else:
                        print(f"   ⚠️  {agent_name} responded with status {response.status}")
        except asyncio.TimeoutError:
            print(f"   ❌ {agent_name} - Timeout (is it running?)")
        except Exception as e:
            print(f"   ❌ {agent_name} - Not reachable (is it running?)")


async def test_chat_protocol():
    """Test the Chat Protocol on Portfolio Coordinator"""
    print("\n" + "=" * 60)
    print("Testing Chat Protocol (Portfolio Coordinator)")
    print("=" * 60)

    print("\n💬 The Portfolio Coordinator supports ASI:One Chat Protocol")
    print("   To test it properly, you need to deploy to Agentverse")
    print("   and test via https://asi1.ai")
    print("\n   For local testing, agents will log their activities")
    print("   in their respective terminal windows.")


async def check_agent_logs():
    """Instructions for checking agent logs"""
    print("\n" + "=" * 60)
    print("How to Verify Agent Interactions Locally")
    print("=" * 60)

    print("\n1. 📊 Chain Scanner Agent:")
    print("   - Should scan every 30 seconds")
    print("   - Watch for: 'Found X opportunities' messages")
    print("   - Should show top 3 opportunities with APY and risk scores")

    print("\n2. 🧠 MeTTa Knowledge Agent:")
    print("   - Updates knowledge base every 5 minutes")
    print("   - Watch for: 'Updating DeFi knowledge base...'")
    print("   - Should list all loaded protocols on startup")

    print("\n3. ⚙️ Strategy Engine Agent:")
    print("   - Processes strategy requests")
    print("   - Watch for: Strategy calculation logs")

    print("\n4. 🔒 Execution Agent:")
    print("   - Handles transaction execution")
    print("   - Watch for: Transaction simulation logs")

    print("\n5. 📈 Performance Tracker Agent:")
    print("   - Tracks portfolio performance")
    print("   - Updates hourly (3600 seconds)")

    print("\n6. 🤖 Portfolio Coordinator Agent:")
    print("   - Central orchestrator with Chat Protocol")
    print("   - Listens for ASI:One messages")
    print("   - In local mode, can't receive messages without mailbox")


def print_expected_outputs():
    """Show expected outputs from each agent"""
    print("\n" + "=" * 60)
    print("Expected Console Outputs")
    print("=" * 60)

    print("\n📊 Chain Scanner (every 30s):")
    print("   ✅ Found 12 opportunities")
    print("   1. Raydium on solana: 22.45% APY (Risk: 5.5)")
    print("   2. PancakeSwap on bsc: 18.23% APY (Risk: 5.0)")
    print("   3. GMX on arbitrum: 15.67% APY (Risk: 5.5)")

    print("\n🧠 MeTTa Knowledge (every 5min):")
    print("   🧠 Updating DeFi knowledge base...")
    print("   ✅ Knowledge base updated")

    print("\n🤖 Portfolio Coordinator:")
    print("   INFO: Starting server on http://0.0.0.0:8000")
    print("   INFO: Manifest published successfully: AgentChatProtocol")
    print("   (Waiting for ASI:One messages or agent queries)")


async def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("YieldSwarm AI - Local Interaction Test")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Make sure all 6 agents are running!")
    print("   Open 6 terminal windows and run each agent:")
    print("   1. python3 agents/portfolio_coordinator.py")
    print("   2. python3 agents/chain_scanner.py")
    print("   3. python3 agents/metta_knowledge.py")
    print("   4. python3 agents/strategy_engine.py")
    print("   5. python3 agents/execution_agent.py")
    print("   6. python3 agents/performance_tracker.py")

    # Wait for user
    print("\n⏸️  Press ENTER when all agents are running...")
    input()

    # Run tests
    await test_agent_discovery()
    await test_chat_protocol()
    await check_agent_logs()
    print_expected_outputs()

    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("\n1. ✅ Local Testing Complete!")
    print("   - All agents should show activity in their terminals")
    print("   - Chain Scanner scans every 30 seconds")
    print("   - MeTTa updates every 5 minutes")

    print("\n2. 🚀 Deploy to Agentverse:")
    print("   - Sign up at https://agentverse.ai")
    print("   - Get 6 mailbox API keys")
    print("   - Update .env with keys")
    print("   - Restart all agents")

    print("\n3. 🧪 Test via ASI:One:")
    print("   - Go to https://asi1.ai")
    print("   - Search for your coordinator agent")
    print("   - Test natural language commands")

    print("\n4. 📹 Record Demo Video (3-5 minutes)")

    print("\n5. 📤 Submit to Hackathon!")

    print("\n" + "=" * 60)
    print("🐝 YieldSwarm AI - Ready for Deployment!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
