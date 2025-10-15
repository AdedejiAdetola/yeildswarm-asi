# CRITICAL: Agentverse is Stateless!

## The Fundamental Problem Discovered

After extensive debugging, we've discovered that **Agentverse runs each message handler with a FRESH agent instance**:

```
Storage attempt 1: Agent object ID: 139807038451776
Retrieval attempt 2: Agent object ID: 139776932817792  ← DIFFERENT!
```

This means:
- Module-level variables are reset
- Agent object attributes are reset
- `ctx.storage` times out (not working properly)
- **NO STATE PERSISTS between handlers**

## The Only Solution: Stateless Message Passing

We must **embed ALL context in the messages themselves** and pass it through the chain:

```
User → Coordinator → Scanner → Coordinator → MeTTa → Coordinator → Strategy → Coordinator → User
         ↓             ↓           ↓            ↓          ↓             ↓          ↓
      (request)    (+ sender)  (+ sender)  (+ sender)  (+ sender)   (+ sender) (response)
                   (+ amount)  (+ amount)  (+ amount)  (+ amount)
                   (+ risk)    (+ risk)    (+ risk)    (+ opportunities)
```

## Required Changes

### 1. Update Scanner Agent (1_chain_scanner.py)

The Scanner must include the context it received in its response:

```python
@scanner.on_message(model=OpportunityRequest)
async def handle_scan_request(ctx: Context, sender: str, msg: OpportunityRequest):
    # ... scan for opportunities ...

    response = OpportunityResponse(
        request_id=msg.request_id,
        opportunities=opportunities,
        timestamp=datetime.now(timezone.utc).isoformat(),
        chains_scanned=msg.chains,
        # ADD THESE:
        sender=sender,  # Pass the coordinator address forward
        amount=None,  # Will be extracted from request_id or separate field
        risk_level=None  # Needs to be added to OpportunityRequest
    )
```

### 2. Add Context to OpportunityRequest

```python
class OpportunityRequest(BaseModel):
    request_id: str
    chains: List[Chain]
    min_apy: float = 0.0
    max_risk_score: float = 10.0
    # ADD THESE:
    sender: str  # Original user who made the request
    amount: float
    currency: str = "ETH"
    risk_level: str
```

### 3. Update MeTTa Agent (2_metta_knowledge.py)

Similar changes - pass context forward in MeTTaQueryResponse.

### 4. Update Strategy Agent (3_strategy_engine.py)

Similar changes - pass context forward in StrategyResponse.

## Alternative: Simplified Single-Agent Approach

Given Agentverse's stateless limitations, consider consolidating into a SINGLE agent that:
1. Receives user request
2. Scans opportunities (internal function)
3. Analyzes with MeTTa (internal function)
4. Generates strategy (internal function)
5. Responds to user

This avoids the state management issue entirely.

## Current Status

The coordinator has been updated to expect context in responses, but **the other agents need updates** to pass context forward.

**IMMEDIATE ACTION REQUIRED:**
1. Update Scanner to include `sender`, `amount`, `risk_level` in OpportunityResponse
2. Update MeTTa to include full context in MeTTaQueryResponse
3. Update Strategy to include full context in StrategyResponse

OR

**Simpler approach**: Merge all agents into one coordinator file for Agentverse deployment.
