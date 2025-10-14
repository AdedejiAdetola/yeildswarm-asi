# YieldSwarm AI - Quick Start Guide

## 🚀 Running the Application

### Step 1: Start Backend API

```bash
cd /home/grey/web3/asi_agents
source venv/bin/activate
python run_backend.py
```

Expected output:
```
🚀 Starting YieldSwarm AI Backend...
🤖 AgentClient initialized
✅ AgentClient started
✅ Backend ready!
INFO:     Uvicorn running on http://0.0.0.0:8080
```

### Step 2: Start Frontend (New Terminal)

```bash
cd /home/grey/web3/asi_agents/frontend
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in XXX ms
➜  Local:   http://localhost:5173/
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5173**

You should see the YieldSwarm AI interface with:
- 💬 Chat tab - Interact with AI agents
- 📊 Portfolio tab - View your portfolio
- Right sidebar - Live agent status

## 🧪 Testing the Backend

```bash
# Health check
curl http://localhost:8080/api/health

# Get agent statuses
curl http://localhost:8080/api/agents/status

# Send chat message
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","user_id":"test123"}'

# Get portfolio
curl http://localhost:8080/api/portfolio/test123
```

## 📁 File Structure

```
asi_agents/
├── run_backend.py          # ← Backend API (all-in-one file)
├── frontend/               # ← React frontend
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── styles/
│   │   └── services/api.ts
│   └── package.json
├── agents/                 # ← uAgents (6 agents)
├── utils/                  # ← Config, MeTTa engine
└── docs/                   # ← Documentation

```

## ✅ System Requirements

- Python 3.10+ with venv activated
- Node.js 18+ with npm
- All dependencies installed:
  - Backend: fastapi, uvicorn, httpx, pydantic
  - Frontend: react, typescript, vite

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
source venv/bin/activate
pip install fastapi uvicorn[standard] httpx pydantic
python run_backend.py
```

### Frontend won't start

**Error**: `Cannot find module 'react'`

**Solution**:
```bash
cd frontend
npm install
npm run dev
```

### Port already in use

**Error**: `Address already in use: 8080`

**Solution**:
```bash
# Find and kill the process
lsof -i :8080
kill -9 <PID>

# Or use a different port
uvicorn run_backend:app --port 8081
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/health` | GET | Detailed health status |
| `/api/agents/status` | GET | Get all agent statuses |
| `/api/chat` | POST | Send chat message |
| `/api/invest` | POST | Create investment request |
| `/api/portfolio/{user_id}` | GET | Get user portfolio |
| `/api/opportunities` | GET | Get DeFi opportunities |
| `/ws/{user_id}` | WebSocket | Real-time updates |

## 🎯 Next Steps

1. **Test the system**: Try all features in the UI
2. **Connect real agents**: Link backend to actual uAgents
3. **Add real data**: Integrate real DeFi protocols
4. **Deploy**: Deploy to production

---

**Need help?** Check the docs/ folder for detailed documentation.
