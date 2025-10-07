"""
YieldSwarm AI - Quick Test Script
Run this to verify all agents can be imported and initialized
"""
import sys

def test_imports():
    """Test that all dependencies can be imported"""
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)

    errors = []

    # Test core dependencies
    try:
        import uagents
        print("✅ uagents imported successfully")
    except ImportError as e:
        errors.append(f"❌ uagents: {e}")

    try:
        from uagents_core.contrib.protocols.chat import ChatMessage
        print("✅ uagents_core imported successfully")
    except ImportError as e:
        errors.append(f"❌ uagents_core: {e}")

    try:
        from hyperon import MeTTa
        print("✅ hyperon (MeTTa) imported successfully")
    except ImportError as e:
        errors.append(f"❌ hyperon: {e}")

    # Test other dependencies
    try:
        import web3
        print("✅ web3 imported successfully")
    except ImportError as e:
        errors.append(f"❌ web3: {e}")

    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError as e:
        errors.append(f"❌ pydantic: {e}")

    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        errors.append(f"❌ python-dotenv: {e}")

    print("\n" + "=" * 60)

    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  {error}")
        print("\n💡 Install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed correctly!")
        return True


def test_agent_imports():
    """Test that all agent modules can be imported"""
    print("\n" + "=" * 60)
    print("Testing agent imports...")
    print("=" * 60)

    errors = []

    try:
        from utils.config import config
        print(f"✅ Config loaded (Environment: {config.ENVIRONMENT})")
    except Exception as e:
        errors.append(f"❌ Config: {e}")

    try:
        from utils.models import InvestmentRequest, Strategy
        print("✅ Models imported successfully")
    except Exception as e:
        errors.append(f"❌ Models: {e}")

    # Don't actually create agents (they'll try to start), just import
    agent_modules = [
        "agents.portfolio_coordinator",
        "agents.chain_scanner",
        "agents.metta_knowledge",
        "agents.strategy_engine",
        "agents.execution_agent",
        "agents.performance_tracker",
    ]

    for module_name in agent_modules:
        try:
            __import__(module_name)
            agent_name = module_name.split('.')[-1].replace('_', ' ').title()
            print(f"✅ {agent_name} can be imported")
        except Exception as e:
            errors.append(f"❌ {module_name}: {e}")

    print("\n" + "=" * 60)

    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✅ All agents can be imported!")
        return True


def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("\n1. Configure environment variables:")
    print("   cp .env.example .env")
    print("   # Edit .env with your configuration")

    print("\n2. Run agents locally (6 terminals):")
    print("   Terminal 1: python agents/portfolio_coordinator.py")
    print("   Terminal 2: python agents/chain_scanner.py")
    print("   Terminal 3: python agents/metta_knowledge.py")
    print("   Terminal 4: python agents/strategy_engine.py")
    print("   Terminal 5: python agents/execution_agent.py")
    print("   Terminal 6: python agents/performance_tracker.py")

    print("\n3. Deploy to Agentverse:")
    print("   - Get mailbox keys from https://agentverse.ai")
    print("   - Update .env with mailbox keys")
    print("   - Run each agent (they auto-register)")
    print("   - Test via ASI:One interface")

    print("\n4. Create demo video (3-5 minutes)")

    print("\n5. Submit to hackathon!")

    print("\n📚 Documentation:")
    print("   - README.md: Complete project overview")
    print("   - SETUP.md: Detailed setup instructions")
    print("   - WINNING_PROJECT_PLAN.md: Full project plan")

    print("\n" + "=" * 60)
    print("🐝 YieldSwarm AI - Ready to optimize DeFi yields!")
    print("=" * 60 + "\n")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("YieldSwarm AI - Setup Verification")
    print("=" * 60 + "\n")

    # Test imports
    imports_ok = test_imports()

    if not imports_ok:
        print("\n⚠️  Please install dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    # Test agent imports
    agents_ok = test_agent_imports()

    if not agents_ok:
        print("\n⚠️  Some agent modules have issues. Check errors above.")
        sys.exit(1)

    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
