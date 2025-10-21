# 🤖 Portfolio Coordinator Agent

**Address:** `agent1qwumkwejd0rxnxxu64yrl7vj3f29ydvvq85yntvrvjyzpce86unwxhfdz5a`
**Status:** ✅ Production Ready | ASI:One Compatible

## Overview

Central orchestrator and user-facing interface for YieldSwarm AI. Handles natural language requests via ASI:One Chat Protocol and coordinates 3 specialized agents.

## Key Features

- 🗣️ Natural language processing for investment requests
- ✅ Smart input validation (greetings, help, invalid inputs)
- 🔄 Multi-agent orchestration (Scanner → MeTTa → Strategy)
- 💾 Stateless design with base64 context encoding
- 🌐 ASI:One Chat Protocol integration

## Example Usage

**Valid Requests:**
```
"Invest 10 ETH with moderate risk"
"Invest 5 ETH with conservative risk on Ethereum"
```

**Helpful Responses:**
- `"hello"` → Welcome message
- `"help"` → Usage guide
- `"gibberish"` → Examples

## Technical Details

**Configuration (lines 114-116):**
```python
SCANNER_ADDRESS = "agent1qtn2hgpdfl0he2h88xncvrdvyk5vd9xtsruw9vzua8tgnejtxxpzy8suu8r"
METTA_ADDRESS = "agent1qflfh899d98vw3337neylwjkfvc4exx6frsj6vqnaeq0ujwjf6ggcczc5y0"
STRATEGY_ADDRESS = "agent1qwqr4489ww7kplx456w5tpj4548s743wvp7ly3qjd6aurgp04cf4zswgyal"
```

**Message Flow:**
```
User → Coordinator → Scanner → Coordinator
              ↓
         MeTTa Agent → Coordinator
              ↓
      Strategy Engine → Coordinator → User
```

## Deployment

1. Copy `agents_agentverse/0_COORDINATOR.py` to Agentverse
2. Verify agent addresses (lines 114-116)
3. Deploy and enable Chat Protocol
4. Test via ASI:One

---

**More Info:** [Main README](../README.md) | [Testing Guide](../TESTING_GUIDE.md)
