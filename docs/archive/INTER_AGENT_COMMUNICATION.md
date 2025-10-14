# YieldSwarm AI - Inter-Agent Communication Implementation

## Overview

This document describes the inter-agent communication system implemented for YieldSwarm AI, following the official uAgents framework patterns from the ASI Alliance documentation.

**Date Implemented**: October 11, 2025
**Status**: ✅ Core communication patterns implemented and ready for testing

---

## Architecture

### Message Flow Pattern

```
User (ASI:One)
    ↓ ChatMessage
Portfolio Coordinator (Orchestrator)
    ↓ OpportunityRequest
Chain Scanner
    ↓ OpportunityResponse
Portfolio Coordinator
    ↓ MeTTaQuery
MeTTa Knowledge Agent
    ↓ ProtocolKnowledge
Portfolio Coordinator
    ↓ StrategyRequest
Strategy Engine
    ↓ Strategy
Portfolio Coordinator
    ↓ ChatMessage (response)
User (ASI:One)
```

---

## Implemented Message Types

### 1. OpportunityRequest
**From**: Portfolio Coordinator
**To**: Chain Scanner
**Purpose**: Request DeFi yield opportunities across specified chains

```python
OpportunityRequest(
    request_id: str,
    chains: List[Chain],
    min_apy: float,
    max_risk_score: float
)
```

### 2. OpportunityResponse
**From**: Chain Scanner
**To**: Portfolio Coordinator
**Purpose**: Return discovered opportunities

```python
OpportunityResponse(
    request_id: str,
    opportunities: List[Opportunity],
    timestamp: str,
    chains_scanned: List[Chain]
)
```

### 3. MeTTaQuery
**From**: Portfolio Coordinator / Strategy Engine
**To**: MeTTa Knowledge Agent
**Purpose**: Query symbolic knowledge base

```python
MeTTaQuery(
    query_id: str,
    query_type: str,  # "best_protocols", "assess_risk", "allocation_strategy"
    parameters: dict
)
```

### 4. ProtocolKnowledge
**From**: MeTTa Knowledge Agent
**To**: Requesting Agent
**Purpose**: Return knowledge base results

```python
ProtocolKnowledge(
    query_id: str,
    protocols: List[dict],
    reasoning: str,
    confidence: float
)
```

### 5. StrategyRequest
**From**: Portfolio Coordinator
**To**: Strategy Engine
**Purpose**: Request optimal investment strategy

```python
StrategyRequest(
    request_id: str,
    investment_request: InvestmentRequest,
    opportunities: List[Opportunity],
    metta_knowledge: dict
)
```

### 6. Strategy
**From**: Strategy Engine
**To**: Portfolio Coordinator
**Purpose**: Return optimized allocation strategy

```python
Strategy(
    strategy_id: str,
    user_id: str,
    total_amount: float,
    actions: List[AllocationAction],
    expected_apy: float,
    risk_score: float,
    estimated_gas_cost: float,
    created_at: datetime
)
```

---

## Agent Implementation Details

### Portfolio Coordinator (`agents/portfolio_coordinator.py`)

**Responsibilities**:
- Receive user requests via Chat Protocol
- Orchestrate communication with specialized agents
- Aggregate responses and provide user feedback

**Message Handlers**:
```python
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Parse user request
    # Send OpportunityRequest to Scanner
    # Optionally query MeTTa Knowledge
    # Send StrategyRequest to Strategy Engine
    # Respond to user with results
```

**Sends Messages To**:
- Chain Scanner (OpportunityRequest)
- MeTTa Knowledge (MeTTaQuery)
- Strategy Engine (StrategyRequest)

**Receives Messages From**:
- Users (ChatMessage)
- Chain Scanner (OpportunityResponse)
- MeTTa Knowledge (ProtocolKnowledge)
- Strategy Engine (Strategy)

---

### Chain Scanner (`agents/chain_scanner.py`)

**Responsibilities**:
- Monitor multiple blockchains for DeFi opportunities
- Filter opportunities based on criteria
- Respond to opportunity requests

**Message Handlers**:
```python
@scanner.on_message(model=OpportunityRequest)
async def handle_opportunity_request(ctx: Context, sender: str, msg: OpportunityRequest):
    # Scan requested chains
    # Filter by min_apy and max_risk_score
    # Return OpportunityResponse
```

**Sends Messages To**:
- Portfolio Coordinator (OpportunityResponse)

**Receives Messages From**:
- Portfolio Coordinator (OpportunityRequest)

---

### MeTTa Knowledge Agent (`agents/metta_knowledge.py`)

**Responsibilities**:
- Maintain symbolic knowledge base of DeFi protocols
- Answer queries about protocol characteristics
- Provide allocation recommendations

**Message Handlers**:
```python
@metta_agent.on_message(model=MeTTaQuery)
async def handle_query(ctx: Context, sender: str, msg: MeTTaQuery):
    # Process query based on query_type
    # Query knowledge base
    # Return ProtocolKnowledge
```

**Supported Query Types**:
1. `best_protocols` - Find optimal protocols for risk/chains
2. `assess_risk` - Detailed risk assessment for protocol
3. `allocation_strategy` - Optimal portfolio allocation

**Sends Messages To**:
- Requesting Agent (ProtocolKnowledge)

**Receives Messages From**:
- Portfolio Coordinator (MeTTaQuery)
- Strategy Engine (MeTTaQuery)

---

### Strategy Engine (`agents/strategy_engine.py`)

**Responsibilities**:
- Calculate optimal allocation strategies
- Balance risk vs. return
- Generate executable action plans

**Message Handlers**:
```python
@strategy_engine.on_message(model=StrategyRequest)
async def generate_strategy(ctx: Context, sender: str, msg: StrategyRequest):
    # Analyze opportunities
    # Calculate optimal allocations
    # Generate action plan
    # Return Strategy
```

**Sends Messages To**:
- Portfolio Coordinator (Strategy)

**Receives Messages From**:
- Portfolio Coordinator (StrategyRequest)

---

## Agent Addresses

All agents use deterministic addresses generated from seeds defined in `utils/config.py`:

```python
COORDINATOR_ADDRESS = "agent1qd3gddfekqpp562kwpvkedgdd8sjrasje85vr9pdav08y22ahyvykq6frz5"
SCANNER_ADDRESS = "agent1qdvd6cc4eafn92740d7afkjfx9uucetgjpqw3rg7npnqf5qg5zn7vr40plp"
METTA_ADDRESS = "agent1q0nwxnu6dhws86gxqd7sv5ywv57nnsncfhxcgnxkxkh5mshgze9kuvztx0t"
STRATEGY_ADDRESS = "agent1q0v38te45h3ns2nas9pluajdzguww6t99t37x9lp7an5e3pcckpxkgreypz"
EXECUTION_ADDRESS = "agent1q290kzkwzuyzjkft35jz9ul2jjjh7rskp9525grnz0xrn6hnhnwfs4vqua5"
TRACKER_ADDRESS = "agent1qt9xt0jdshxrnfu9xvxa5rscfqenupldrkxm7egtd0xrn6hnhnwfs4vqua5"
```

---

## Testing

### Test Script

A comprehensive test script has been created: `test_inter_agent_comm.py`

**What it tests**:
1. Coordinator → Scanner (OpportunityRequest)
2. Scanner → Coordinator (OpportunityResponse)
3. Coordinator → Strategy Engine (StrategyRequest)
4. Strategy Engine → Coordinator (Strategy)

**How to run**:

```bash
# Terminal 1: Start Chain Scanner
source venv/bin/activate
python agents/chain_scanner.py

# Terminal 2: Start Strategy Engine
source venv/bin/activate
python agents/strategy_engine.py

# Terminal 3: Run Test
source venv/bin/activate
python test_inter_agent_comm.py
```

**Expected Output**:
- Test agent sends OpportunityRequest to Scanner
- Scanner logs receiving request and responds
- Test agent receives OpportunityResponse
- Test agent sends StrategyRequest to Strategy Engine
- Strategy Engine logs receiving request and responds
- Test confirms successful communication

---

## Implementation Patterns

### Message Handler Pattern (Official uAgents)

```python
from uagents import Agent, Context
from protocols.messages import YourMessageModel

agent = Agent(name="your-agent", seed="your-seed", port=8000)

@agent.on_message(model=YourMessageModel)
async def handle_message(ctx: Context, sender: str, msg: YourMessageModel):
    """
    Handle incoming messages

    Args:
        ctx: Agent context for logging and sending messages
        sender: Address of the sending agent
        msg: The message object (Pydantic model)
    """
    ctx.logger.info(f"Received message from {sender}")

    # Process message
    result = process(msg)

    # Send response
    response = YourResponseModel(...)
    await ctx.send(sender, response)
```

### Sending Messages Pattern

```python
from utils.config import config

# Send to specific agent
await ctx.send(config.SCANNER_ADDRESS, your_message)

# Log the action
ctx.logger.info(f"📤 Sent message to Scanner")
```

---

## Next Steps

### Phase 3: Complete Full Orchestration (Days 3-4)

1. **Add Response Handlers to Portfolio Coordinator**
   - Handle OpportunityResponse from Scanner
   - Handle ProtocolKnowledge from MeTTa
   - Handle Strategy from Strategy Engine

2. **Implement Request Tracking**
   - Track request IDs
   - Match responses to original requests
   - Handle timeouts

3. **Add Async Orchestration**
   - Wait for all responses before proceeding
   - Implement timeout handling
   - Error recovery mechanisms

4. **Complete MeTTa Integration**
   - Install hyperon library
   - Load defi_protocols.metta
   - Implement real MeTTa queries

### Phase 4: Execution Agent Integration (Days 5-6)

1. Add ApprovedStrategy message type
2. Implement transaction execution handlers
3. Connect Execution Agent to Strategy Engine
4. Add MEV protection logic

### Phase 5: Performance Tracking (Days 7-8)

1. Add ExecutionReport message type
2. Implement portfolio tracking
3. Add PerformanceUpdate messages
4. Create rebalancing triggers

---

## Official Documentation References

All patterns follow official ASI Alliance documentation:

- **uAgent Creation**: https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- **Agent Communication**: https://innovationlab.fetch.ai/resources/docs/agent-communication/uagent-uagent-communication
- **Chat Protocol**: https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents

---

## Status Summary

✅ **Completed**:
- Agent address generation
- Message models defined (protocols/messages.py)
- Chain Scanner message handlers
- MeTTa Knowledge message handlers
- Strategy Engine message handlers
- Portfolio Coordinator sending logic
- Test script created

⏳ **In Progress**:
- Full async orchestration in Coordinator
- MeTTa Python integration (hyperon)

📋 **Pending**:
- Response handlers in Coordinator
- Execution Agent integration
- Performance Tracker integration
- Frontend API connection
- End-to-end testing

---

**Last Updated**: October 11, 2025
**Contributors**: YieldSwarm AI Development Team
**License**: Apache 2.0
