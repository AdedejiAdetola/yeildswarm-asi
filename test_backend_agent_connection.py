"""
Test backend to agent connection
"""
import asyncio
import httpx

async def test_backend_chat():
    """Test sending chat through backend"""
    print("\n" + "=" * 60)
    print("🧪 Testing Backend → Coordinator Integration")
    print("=" * 60)

    # Test message
    message = {
        "text": "Invest 15 ETH with aggressive risk on Ethereum and Solana",
        "user_id": "test-user-12345"
    }

    print(f"\n📤 Sending test message to backend...")
    print(f"   Message: {message['text']}")
    print(f"   User: {message['user_id']}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8080/api/chat",
                json=message
            )

            print(f"\n📥 Backend Response:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")

            if response.status_code == 200:
                print(f"\n✅ Message sent successfully!")
                print(f"\n👀 Now check the logs to see agent orchestration:")
                print(f"   tail -f logs/coordinator.log")
                print(f"   tail -f logs/scanner.log")
                print(f"   tail -f logs/metta.log")
                print(f"   tail -f logs/strategy.log")
            else:
                print(f"\n⚠️  Unexpected status code")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_backend_chat())
