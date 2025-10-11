# YieldSwarm AI - Startup Guide

## ✅ What Was Fixed

### Problem Identified
The frontend was receiving the same hardcoded response for every request because:
- The system was using `run_backend.py` (v1.0) which had mock/static responses
- There was no real connection between the backend and the Portfolio Coordinator agent
- `run_backend_v2.py` existed but wasn't being used, and lacked proper HTTP endpoints

### Solution Implemented
1. **Created HTTP REST API endpoint** on Portfolio Coordinator agent
   - New file: `agents/portfolio_coordinator_http.py`
   - Provides `/chat` endpoint for HTTP communication
   - Processes messages and returns real-time, context-aware responses

2. **Updated Backend v2** (`run_backend_v2.py`)
   - Modified `RealAgentClient` to call coordinator's `/chat` endpoint
   - Changed from mock chat protocol to proper HTTP REST calls
   - Now successfully communicates with coordinator

3. **Updated Frontend** (`frontend/src/components/ChatInterface.tsx`)
   - Changed from mock `generateResponse()` to real API calls
   - Calls `http://localhost:8080/api/chat`
   - Falls back to mock responses if backend is offline

## 🚀 How to Start The System

You need **3 terminals** running simultaneously:

### Terminal 1: Portfolio Coordinator Agent (Port 8000)
```bash
cd /home/grey/web3/asi_agents
source venv/bin/activate
python agents/portfolio_coordinator_http.py
```

Expected output:
```
============================================================
YieldSwarm AI - Portfolio Coordinator HTTP API
============================================================
HTTP API Port: 8000
Service: HTTP REST API
Environment: development
============================================================

🚀 Starting HTTP API server...

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Backend API v2 (Port 8080)
```bash
cd /home/grey/web3/asi_agents
source venv/bin/activate
python run_backend_v2.py
```

Expected output:
```
============================================================
🚀 YieldSwarm AI Backend v2 - Real Agent Integration
============================================================
📡 Will connect to running agents on:
   - Portfolio Coordinator: localhost:8000
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8080
✅ Connected to Portfolio Coordinator: 200
✅ Backend ready!
```

### Terminal 3: Frontend (Port 5173)
```bash
cd /home/grey/web3/asi_agents/frontend
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## 🧪 Testing The System

### Test 1: Health Checks
```bash
# Check coordinator
curl http://localhost:8000/

# Check backend
curl http://localhost:8080/api/health
```

### Test 2: Direct Chat Test
```bash
# Test investment request
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"Invest 10 ETH with moderate risk","user_id":"test"}'

# Test portfolio query
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"portfolio","user_id":"test"}'

# Test help
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"help","user_id":"test"}'
```

### Test 3: Frontend UI
1. Open browser to `http://localhost:5173`
2. Try these commands in the chat:
   - "Invest 15 ETH with aggressive risk on Solana"
   - "Show my portfolio"
   - "Help"

## ✨ What's Different Now?

### Before (Hardcoded Responses)
- Every request returned the same static response
- No real agent processing
- Responses didn't adapt to user input

### After (Real-Time Agent Responses)
- **Different responses based on user input**:
  - "Invest 10 ETH moderate risk" → Shows 10 ETH, Moderate risk, Ethereum
  - "Invest 20 ETH aggressive Solana" → Shows 20 ETH, Aggressive risk, Ethereum + Solana
  - "portfolio" → Shows portfolio stats
  - "help" → Shows help commands

- **Real agent coordination**:
  - Backend v2 → Coordinator (port 8000)
  - Coordinator parses investment requests
  - Returns context-aware responses

## 📁 Key Files Modified

1. **`agents/portfolio_coordinator_http.py`** (NEW)
   - HTTP REST API version of coordinator
   - Port: 8000
   - Endpoints: `/`, `/chat`

2. **`run_backend_v2.py`**
   - Updated `send_chat_message_to_agent()` method (line 141-181)
   - Changed endpoint from `/submit` to `/chat`
   - Updated payload format

3. **`frontend/src/components/ChatInterface.tsx`**
   - Updated `sendMessage()` method (line 32-81)
   - Added real fetch() call to backend
   - Fallback to mock response if offline

## 🎯 Next Steps (Optional)

### Add More Agents
Currently only the Coordinator is running. To enable full agent swarm:

```bash
# Terminal 4: Chain Scanner (port 8001)
python agents/chain_scanner.py

# Terminal 5: Strategy Engine (port 8002)
python agents/strategy_engine.py

# Terminal 6: MeTTa Knowledge (port 8003)
python agents/metta_knowledge.py
```

### Connect Real Agent Communication
The coordinator currently processes requests internally. To enable real inter-agent communication:
- Implement async request/response handling
- Add message queuing between agents
- Use uAgents protocol for agent-to-agent messaging

## 🐛 Troubleshooting

### "Connection refused" on port 8000
- Coordinator isn't running
- Run: `python agents/portfolio_coordinator_http.py`

### "Connection refused" on port 8080
- Backend v2 isn't running
- Run: `python run_backend_v2.py`

### Frontend shows "Backend offline" warning
- Either port 8000 or 8080 isn't running
- Check both terminals are active

### Backend shows "Cannot connect to Portfolio Coordinator"
- Port 8000 isn't running
- Start coordinator first, then backend

## 📊 Architecture

```
┌─────────────┐
│   Browser   │
│ (port 5173) │
└──────┬──────┘
       │ HTTP
       ↓
┌──────────────────┐
│   Backend v2     │
│   (port 8080)    │
│  run_backend_v2  │
└──────┬───────────┘
       │ HTTP /chat
       ↓
┌────────────────────────┐
│  Portfolio Coordinator │
│      (port 8000)       │
│   portfolio_coord...   │
└────────────────────────┘
```

## 🎉 Success Indicators

1. ✅ All 3 services running (ports 8000, 8080, 5173)
2. ✅ Backend logs show "✅ Connected to Portfolio Coordinator: 200"
3. ✅ Different chat responses for different investment amounts
4. ✅ Portfolio query returns portfolio data
5. ✅ No "Backend offline" warnings in frontend

---

**Last Updated:** 2025-10-11
**Version:** 2.0.0 (Real Agent Integration)
