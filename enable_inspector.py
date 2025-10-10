"""
Enable Agent Inspector Access
Updates agent endpoints from localhost to network IP
"""
import subprocess
import sys

def get_local_ip():
    """Get local network IP address"""
    try:
        result = subprocess.run(
            ["hostname", "-I"],
            capture_output=True,
            text=True
        )
        ip = result.stdout.strip().split()[0]
        return ip
    except:
        try:
            result = subprocess.run(
                ["ip", "-4", "addr", "show"],
                capture_output=True,
                text=True
            )
            # Parse output for IP
            for line in result.stdout.split('\n'):
                if 'inet' in line and '127.0.0.1' not in line:
                    ip = line.strip().split()[1].split('/')[0]
                    return ip
        except:
            return None

def update_agent_endpoints(ip_address):
    """Update all agent files to use network IP"""
    agents = [
        ('agents/chain_scanner.py', 8001),
        ('agents/strategy_engine.py', 8003),
        ('agents/execution_agent.py', 8004),
        ('agents/performance_tracker.py', 8005),
        ('agents/metta_knowledge.py', 8002),
        ('agents/portfolio_coordinator.py', 8000),
    ]

    print(f"\n🔄 Updating agents to use IP: {ip_address}\n")

    for agent_file, port in agents:
        old_endpoint = f'endpoint=["http://127.0.0.1:{port}/submit"]'
        new_endpoint = f'endpoint=["http://{ip_address}:{port}/submit"]'

        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            if old_endpoint in content:
                content = content.replace(old_endpoint, new_endpoint)
                with open(agent_file, 'w') as f:
                    f.write(content)
                print(f"✅ Updated {agent_file}")
            else:
                print(f"⏭️  {agent_file} already using network IP or different format")

        except Exception as e:
            print(f"❌ Error updating {agent_file}: {e}")

    print("\n" + "=" * 70)
    print("UPDATED INSPECTOR URLS")
    print("=" * 70 + "\n")

    from utils.config import config

    # Re-import agents to get updated addresses
    from uagents import Agent

    agents_config = [
        ("Portfolio Coordinator", "yieldswarm-coordinator", config.COORDINATOR_SEED, config.COORDINATOR_PORT),
        ("Chain Scanner", "yieldswarm-scanner", config.SCANNER_SEED, config.SCANNER_PORT),
        ("MeTTa Knowledge", "yieldswarm-metta", config.METTA_SEED, config.METTA_PORT),
        ("Strategy Engine", "yieldswarm-strategy", config.STRATEGY_SEED, config.STRATEGY_PORT),
        ("Execution Agent", "yieldswarm-execution", config.EXECUTION_SEED, config.EXECUTION_PORT),
        ("Performance Tracker", "yieldswarm-tracker", config.TRACKER_SEED, config.TRACKER_PORT),
    ]

    for display_name, name, seed, port in agents_config:
        temp_agent = Agent(
            name=name,
            seed=seed,
            port=port,
            endpoint=[f"http://{ip_address}:{port}/submit"]
        )

        inspector_url = f"https://agentverse.ai/inspect/?uri=http%3A//{ip_address}%3A{port}&address={temp_agent.address}"
        print(f"📍 {display_name}")
        print(f"   {inspector_url}\n")


def revert_to_localhost():
    """Revert all agents back to localhost"""
    agents = [
        ('agents/chain_scanner.py', 8001),
        ('agents/strategy_engine.py', 8003),
        ('agents/execution_agent.py', 8004),
        ('agents/performance_tracker.py', 8005),
        ('agents/metta_knowledge.py', 8002),
        ('agents/portfolio_coordinator.py', 8000),
    ]

    print("\n🔄 Reverting agents to localhost...\n")

    for agent_file, port in agents:
        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            # Find any IP-based endpoint and replace with localhost
            import re
            pattern = rf'endpoint=\["http://[\d.]+:{port}/submit"\]'
            replacement = f'endpoint=["http://127.0.0.1:{port}/submit"]'

            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                with open(agent_file, 'w') as f:
                    f.write(content)
                print(f"✅ Reverted {agent_file} to localhost")
            else:
                print(f"⏭️  {agent_file} already using localhost")

        except Exception as e:
            print(f"❌ Error reverting {agent_file}: {e}")


def main():
    print("=" * 70)
    print("Agent Inspector Access - Configuration Tool")
    print("=" * 70)

    if len(sys.argv) > 1 and sys.argv[1] == "revert":
        revert_to_localhost()
        print("\n✅ Reverted to localhost mode")
        print("   Agents will NOT be accessible to cloud Inspector")
        print("   Use console logs for monitoring\n")
        return

    ip_address = get_local_ip()

    if not ip_address:
        print("❌ Could not detect local IP address")
        print("   Please manually update agent endpoints")
        return

    print(f"\n📍 Detected IP Address: {ip_address}")
    print("\nThis will update all agents to use this IP instead of 127.0.0.1")
    print("Agent Inspector will then be able to connect.\n")

    print("⚠️  WARNING:")
    print("   - Your agents will be accessible on your network")
    print("   - Only do this in trusted networks")
    print("   - Anyone on your network can send messages to agents\n")

    response = input("Continue? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\n❌ Cancelled. Agents remain on localhost.")
        return

    update_agent_endpoints(ip_address)

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Restart any running agents for changes to take effect")
    print("2. Open the Inspector URLs above in your browser")
    print("3. Agents will now be visible in the cloud Inspector")
    print("\nTo revert to localhost:")
    print("   python enable_inspector.py revert\n")


if __name__ == "__main__":
    main()
