"""
YieldSwarm AI - HTTP Chat Test
Tests the HTTP endpoint that the backend uses
"""

import requests
import json

def test_coordinator_health():
    """Test coordinator health endpoint"""
    print("\n" + "=" * 60)
    print("🏥 Testing Coordinator Health")
    print("=" * 60)

    try:
        response = requests.get("http://localhost:8000/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_backend_to_coordinator():
    """Test backend sending message to coordinator"""
    print("\n" + "=" * 60)
    print("💬 Testing Backend → Coordinator Chat")
    print("=" * 60)

    # Check if backend is running
    try:
        backend_health = requests.get("http://localhost:8080/")
        print(f"✅ Backend is running: {backend_health.json()}")
    except Exception as e:
        print(f"⚠️  Backend not running: {str(e)}")
        print("Start backend with: cd backend && ./start_backend.sh")
        return False

    # Send chat message through backend
    try:
        print("\n📤 Sending chat message through backend...")

        chat_message = {
            "text": "I want to invest 10 ETH with moderate risk. Please analyze opportunities on Ethereum and Solana.",
            "user_id": "test-user-123"
        }

        response = requests.post(
            "http://localhost:8080/chat",
            json=chat_message,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("\n✅ Message sent successfully!")
            print("\n📊 Check logs to see agent orchestration:")
            print("   tail -f logs/coordinator.log")
            print("   tail -f logs/scanner.log")
            print("   tail -f logs/metta.log")
            print("   tail -f logs/strategy.log")
            return True
        else:
            print(f"\n❌ Failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_all_agent_endpoints():
    """Test all agent health endpoints"""
    print("\n" + "=" * 60)
    print("🔍 Testing All Agent Endpoints")
    print("=" * 60)

    agents = {
        "Coordinator": 8000,
        "Scanner": 8001,
        "MeTTa": 8002,
        "Strategy": 8003,
        "Execution": 8004,
        "Tracker": 8005
    }

    results = {}
    for name, port in agents.items():
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=2)
            status = "✅ ONLINE" if response.status_code == 200 else f"⚠️  Status {response.status_code}"
            results[name] = status
            print(f"{name:15} (:{port}): {status}")
        except Exception as e:
            results[name] = "❌ OFFLINE"
            print(f"{name:15} (:{port}): ❌ OFFLINE - {str(e)}")

    return results


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 YieldSwarm AI - HTTP Integration Test")
    print("=" * 60)
    print("\nThis test will:")
    print("  1. Check all agent health endpoints")
    print("  2. Test coordinator health")
    print("  3. Send chat message through backend")
    print("  4. Verify full orchestration flow")
    print("\nMake sure agents are running:")
    print("  ./start_all_agents.sh")
    print("\nAnd backend is running:")
    print("  cd backend && ./start_backend.sh")
    print("=" * 60)

    # Run tests
    print("\n" + "=" * 60)
    print("STEP 1: Check Agent Endpoints")
    print("=" * 60)
    agent_status = test_all_agent_endpoints()

    print("\n" + "=" * 60)
    print("STEP 2: Test Coordinator Health")
    print("=" * 60)
    coordinator_ok = test_coordinator_health()

    print("\n" + "=" * 60)
    print("STEP 3: Test Backend → Coordinator Chat")
    print("=" * 60)
    backend_ok = test_backend_to_coordinator()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    all_agents_online = all(v == "✅ ONLINE" for v in agent_status.values())

    print(f"\nAgent System: {'✅ ALL ONLINE' if all_agents_online else '⚠️  SOME OFFLINE'}")
    print(f"Coordinator Health: {'✅ PASS' if coordinator_ok else '❌ FAIL'}")
    print(f"Backend Integration: {'✅ PASS' if backend_ok else '❌ FAIL'}")

    if all_agents_online and coordinator_ok:
        print("\n🎉 System is ready for testing!")
        print("\nNext steps:")
        print("  1. Open frontend: http://localhost:3000")
        print("  2. Send a message through the chat interface")
        print("  3. Watch the agent orchestration in logs")
    else:
        print("\n⚠️  System needs attention")
        if not all_agents_online:
            print("  Run: ./start_all_agents.sh")
        if not backend_ok:
            print("  Run: cd backend && ./start_backend.sh")

    print("=" * 60 + "\n")
