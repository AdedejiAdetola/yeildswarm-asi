"""
Local Agent Testing Script
Test agents without needing the cloud-based Agent Inspector
"""
import requests
import json
from datetime import datetime

def test_agent(port, agent_name):
    """Test if agent is running and accessible"""
    url = f"http://localhost:{port}"

    print(f"\n{'='*60}")
    print(f"Testing {agent_name} on port {port}")
    print(f"{'='*60}")

    try:
        # Test root endpoint
        response = requests.get(url, timeout=2)
        print(f"✅ Agent is responding on port {port}")
        print(f"   Status Code: {response.status_code}")

        # Try to get agent info
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}")

        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Agent not running on port {port}")
        return False
    except requests.exceptions.Timeout:
        print(f"⏱️  Agent timeout on port {port}")
        return False
    except Exception as e:
        print(f"❌ Error testing agent: {str(e)}")
        return False


def test_agent_submit_endpoint(port, agent_address, agent_name):
    """Test the /submit endpoint that agents use for communication"""
    url = f"http://localhost:{port}/submit"

    print(f"\n📨 Testing {agent_name} /submit endpoint...")

    # Create a simple test message
    test_message = {
        "sender": "test-agent",
        "target": agent_address,
        "protocol": "test",
        "message": {"type": "ping", "timestamp": datetime.now().isoformat()}
    }

    try:
        response = requests.post(url, json=test_message, timeout=2)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200] if response.text else 'No response body'}")
        return True
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("YieldSwarm AI - Local Agent Testing")
    print("=" * 60)
    print("\nThis script tests agents locally without needing Agent Inspector")

    agents = [
        (8000, "agent1q0432az04qafuj9qja7dtrf03n25dp0mmv5kjldjnuxyqllpjf0c22n7z0f", "Portfolio Coordinator"),
        (8001, "agent1qw9dz27z0ydhm7g5d2k022wg3q32zjcr009p833ag94w9udgqfx9u746ck9", "Chain Scanner"),
        (8002, "agent1q29zr74zz6q3052glhefcuyv7n24c78lcrjd9lpav7npw48wx8k0k9xa4rh", "MeTTa Knowledge"),
        (8003, "agent1qtf787vn9h78j6quv4fs0axl4xw3s3r39el93rv88jlwz3uvugt02u4tsjy", "Strategy Engine"),
        (8004, "agent1qd0av377w59qnel53yrjf29s2syy43ef4ld6haput6z020jqfjdwqysurfy", "Execution Agent"),
        (8005, "agent1qg8chd6dzhpl6hfvgtqvx7q0yhmyx9phyewe6dus3lal8s67qa0sje3k0fk", "Performance Tracker"),
    ]

    running_agents = []

    for port, address, name in agents:
        if test_agent(port, name):
            running_agents.append((port, address, name))
            test_agent_submit_endpoint(port, address, name)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\n✅ Running Agents: {len(running_agents)}/{len(agents)}")

    for port, address, name in running_agents:
        print(f"   • {name} (Port {port})")

    not_running = [name for p, a, name in agents if (p, a, name) not in running_agents]
    if not_running:
        print(f"\n❌ Not Running: {len(not_running)}")
        for name in not_running:
            print(f"   • {name}")

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)

    if len(running_agents) < len(agents):
        print("\nTo start agents, run in separate terminals:")
        for port, address, name in agents:
            if (port, address, name) not in running_agents:
                agent_file = name.lower().replace(" ", "_").replace("metta_knowledge", "metta_knowledge")
                print(f"   python agents/{agent_file}.py")
    else:
        print("\n✅ All agents are running!")
        print("\nYou can now test agent communication:")
        print("   python test_local_interaction.py")


if __name__ == "__main__":
    main()
