"""
Script to display all agent addresses and endpoints for local communication
Run this to get agent addresses before starting the full system
"""
from uagents import Agent
from utils.config import config

print("=" * 70)
print("YieldSwarm AI - Local Agent Addresses")
print("=" * 70)
print("\nGenerating agent addresses from seeds...\n")

# Create agents with same seeds as in actual agent files
agents_config = [
    ("Portfolio Coordinator", "yieldswarm-coordinator", config.COORDINATOR_SEED, config.COORDINATOR_PORT),
    ("Chain Scanner", "yieldswarm-scanner", config.SCANNER_SEED, config.SCANNER_PORT),
    ("MeTTa Knowledge", "yieldswarm-metta", config.METTA_SEED, config.METTA_PORT),
    ("Strategy Engine", "yieldswarm-strategy", config.STRATEGY_SEED, config.STRATEGY_PORT),
    ("Execution Agent", "yieldswarm-execution", config.EXECUTION_SEED, config.EXECUTION_PORT),
    ("Performance Tracker", "yieldswarm-tracker", config.TRACKER_SEED, config.TRACKER_PORT),
]

agent_info = []

for display_name, name, seed, port in agents_config:
    # Create temporary agent just to get address
    temp_agent = Agent(
        name=name,
        seed=seed,
        port=port,
        endpoint=[f"http://127.0.0.1:{port}/submit"]
    )

    agent_info.append({
        "name": display_name,
        "address": temp_agent.address,
        "port": port,
        "endpoint": f"http://127.0.0.1:{port}/submit",
        "inspector": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{port}&address={temp_agent.address}"
    })

# Display in table format
for info in agent_info:
    print(f"📍 {info['name']}")
    print(f"   Address:   {info['address']}")
    print(f"   Port:      {info['port']}")
    print(f"   Endpoint:  {info['endpoint']}")
    print(f"   Inspector: {info['inspector']}")
    print()

print("=" * 70)
print("CONFIGURATION FOR .env FILE")
print("=" * 70)
print("\n# Add these to your .env file if you want to hardcode addresses:")
print()
for info in agent_info:
    config_name = info['name'].upper().replace(" ", "_")
    print(f"{config_name}_ADDRESS={info['address']}")

print("\n" + "=" * 70)
print("AGENT COMMUNICATION")
print("=" * 70)
print("\nFor agents to communicate locally:")
print("1. Each agent runs on its own port with an endpoint")
print("2. Agents send messages using: await ctx.send(AGENT_ADDRESS, message)")
print("3. NO Almanac registration required for local communication")
print("4. Use Agent Inspector URL to monitor each agent in real-time")
print("\nExample:")
print("  # Chain Scanner sends to Strategy Engine")
print(f"  await ctx.send('{agent_info[3]['address']}', opportunity_data)")

print("\n" + "=" * 70)
print("NEXT STEPS")
print("=" * 70)
print("\n1. Run each agent in a separate terminal:")
print("   python agents/chain_scanner.py")
print("   python agents/strategy_engine.py")
print("   python agents/execution_agent.py")
print("   python agents/performance_tracker.py")
print("   python agents/metta_knowledge.py")
print("   python agents/portfolio_coordinator.py")
print()
print("2. Open Agent Inspector in browser to monitor any agent")
print()
print("3. Use test_local_interaction.py to test agent communication")
print()
