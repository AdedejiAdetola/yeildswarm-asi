"""
Register YieldSwarm Coordinator with ASI:One
This script registers a local or remotely hosted coordinator agent with ASI:One
"""
import os
from dotenv import load_dotenv
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)

# Load environment variables
load_dotenv()

# Configuration
AGENT_NAME = "YieldSwarm AI Coordinator"
COORDINATOR_ADDRESS = "agent1qwumkwejd0rxnxxu64yrl7vj3f29ydvvq85yntvrvjyzpce86unwxhfdz5a"

# For Agentverse hosted agents, use the Agentverse URL
AGENT_URL = f"https://agentverse.ai/agents/details/{COORDINATOR_ADDRESS}"

# For local agents with ngrok or similar, use your public URL
# AGENT_URL = "https://your-ngrok-url.ngrok.io"

def main():
    """Register the coordinator agent with ASI:One"""

    # Check for required environment variables
    agentverse_key = os.getenv("AGENTVERSE_KEY")
    agent_seed = os.getenv("COORDINATOR_SEED", "coordinator-dev-seed-yieldswarm")

    if not agentverse_key:
        print("❌ Error: AGENTVERSE_KEY not found in environment variables")
        print("Please add it to your .env file:")
        print("AGENTVERSE_KEY=your_key_here")
        return

    print(f"📝 Registering agent: {AGENT_NAME}")
    print(f"🔗 Agent URL: {AGENT_URL}")
    print(f"📍 Agent Address: {COORDINATOR_ADDRESS}")

    try:
        # Register the agent
        register_chat_agent(
            AGENT_NAME,
            AGENT_URL,
            active=True,
            credentials=RegistrationRequestCredentials(
                agentverse_api_key=agentverse_key,
                agent_seed_phrase=agent_seed,
            ),
        )

        print("\n✅ Successfully registered agent with ASI:One!")
        print(f"Your agent should now be discoverable on ASI:One")
        print(f"\nTest it by:")
        print(f"1. Going to https://agentverse.ai")
        print(f"2. Finding '{AGENT_NAME}' in the agent list")
        print(f"3. Clicking 'Chat' to interact with it")

    except Exception as e:
        print(f"\n❌ Error registering agent: {e}")
        print("\nTroubleshooting:")
        print("1. Verify AGENTVERSE_KEY is correct")
        print("2. Ensure COORDINATOR_SEED matches your agent")
        print("3. Check that the agent is running and accessible")
        print("4. For local agents, ensure you have a public endpoint (ngrok, etc.)")

if __name__ == "__main__":
    main()
