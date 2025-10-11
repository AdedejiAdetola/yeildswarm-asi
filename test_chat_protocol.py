"""
Test Chat Protocol functionality for Portfolio Coordinator
Tests ASI:One compatible chat interface
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    StartSessionContent,
    TextContent,
    EndSessionContent,
    chat_protocol_spec,
)
from datetime import datetime, timezone
from uuid import uuid4
from utils.config import config


# Create test user agent (simulates ASI:One)
test_user = Agent(
    name="test-user",
    seed="test-user-chat-2025",
    port=9001
)

# Chat protocol for test user
chat_proto = Protocol(spec=chat_protocol_spec)


def create_chat_message(text: str, include_start: bool = False, include_end: bool = False) -> ChatMessage:
    """Create a chat message"""
    content = []

    if include_start:
        content.append(StartSessionContent(type="start_session"))

    content.append(TextContent(type="text", text=text))

    if include_end:
        content.append(EndSessionContent(type="end_session"))

    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=content
    )


@test_user.on_event("startup")
async def test_chat_flow(ctx: Context):
    """Test complete chat flow with coordinator"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("🧪 TESTING CHAT PROTOCOL")
    ctx.logger.info("=" * 60)

    # Wait for coordinator to be ready
    await asyncio.sleep(2)

    # Test 1: Start session and send investment request
    ctx.logger.info("\n📋 Test 1: Start Session + Investment Request")
    ctx.logger.info("-" * 60)

    investment_msg = create_chat_message(
        text="I want to invest 10 ETH with moderate risk on Ethereum and Polygon",
        include_start=True
    )

    ctx.logger.info(f"📤 Sending to coordinator: {config.COORDINATOR_ADDRESS}")
    ctx.logger.info(f"   Message: Investment request")

    try:
        await ctx.send(config.COORDINATOR_ADDRESS, investment_msg)
        ctx.logger.info("✅ Message sent successfully")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send: {str(e)}")

    # Test 2: Help request
    await asyncio.sleep(3)

    ctx.logger.info("\n📋 Test 2: Help Request")
    ctx.logger.info("-" * 60)

    help_msg = create_chat_message(text="help")

    try:
        await ctx.send(config.COORDINATOR_ADDRESS, help_msg)
        ctx.logger.info("✅ Help request sent")
    except Exception as e:
        ctx.logger.error(f"❌ Failed: {str(e)}")

    # Test 3: Portfolio status
    await asyncio.sleep(3)

    ctx.logger.info("\n📋 Test 3: Portfolio Status")
    ctx.logger.info("-" * 60)

    status_msg = create_chat_message(text="show my portfolio")

    try:
        await ctx.send(config.COORDINATOR_ADDRESS, status_msg)
        ctx.logger.info("✅ Status request sent")
    except Exception as e:
        ctx.logger.error(f"❌ Failed: {str(e)}")

    # Test 4: End session
    await asyncio.sleep(3)

    ctx.logger.info("\n📋 Test 4: End Session")
    ctx.logger.info("-" * 60)

    end_msg = create_chat_message(
        text="Thanks for your help!",
        include_end=True
    )

    try:
        await ctx.send(config.COORDINATOR_ADDRESS, end_msg)
        ctx.logger.info("✅ End session sent")
    except Exception as e:
        ctx.logger.error(f"❌ Failed: {str(e)}")

    ctx.logger.info("\n" + "=" * 60)
    ctx.logger.info("✅ ALL CHAT PROTOCOL TESTS COMPLETED")
    ctx.logger.info("=" * 60)


# Handle responses from coordinator
@chat_proto.on_message(ChatMessage)
async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat responses from coordinator"""
    ctx.logger.info("\n" + "=" * 60)
    ctx.logger.info("📥 RECEIVED RESPONSE FROM COORDINATOR")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"From: {sender}")
    ctx.logger.info(f"Message ID: {msg.msg_id}")
    ctx.logger.info(f"Timestamp: {msg.timestamp}")
    ctx.logger.info(f"Content items: {len(msg.content)}")

    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Print message content
    for i, item in enumerate(msg.content, 1):
        if isinstance(item, TextContent):
            ctx.logger.info(f"\nMessage {i}:")
            ctx.logger.info("-" * 40)
            ctx.logger.info(item.text)
            ctx.logger.info("-" * 40)
        elif isinstance(item, StartSessionContent):
            ctx.logger.info("Session started by coordinator")
        elif isinstance(item, EndSessionContent):
            ctx.logger.info("Session ended by coordinator")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements"""
    ctx.logger.info(f"✅ Coordinator acknowledged message {msg.acknowledged_msg_id}")


# Include chat protocol
test_user.include(chat_proto)


if __name__ == "__main__":
    print("\n🧪 YieldSwarm AI - Chat Protocol Test")
    print("=" * 60)
    print("\nThis script tests the Chat Protocol with Portfolio Coordinator")
    print("\nTests:")
    print("1. Start session + Investment request")
    print("2. Help command")
    print("3. Portfolio status query")
    print("4. End session")
    print("\nMake sure Portfolio Coordinator is running on port 8000")
    print("\nStarting test...\n")

    test_user.run()
