import { useState, useRef, useEffect } from 'react'
import '../styles/ChatInterface.css'
import AllocationChart from './AllocationChart'

interface Message {
  id: string
  text: string
  sender: 'user' | 'agent'
  timestamp: Date
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '👋 Welcome to YieldSwarm AI! I\'m your autonomous DeFi yield optimizer powered by 6 specialized AI agents.\n\nTell me how much you want to invest and your risk tolerance (conservative/moderate/aggressive).\n\nExample: "Invest 10 ETH with moderate risk on Ethereum"',
      sender: 'agent',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const userInput = input
    setInput('')
    setIsLoading(true)

    try {
      // Call the real backend API (via Vite proxy)
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userInput,
          user_id: 'frontend-user-' + Date.now()
        })
      })

      const data = await response.json()

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.success ? data.response : 'Error: ' + (data.error || 'Unknown error'),
        sender: 'agent',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      // Show actual error if backend is down
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `❌ Unable to connect to backend.\n\nPlease ensure:\n1. Backend is running on port 8080\n2. Portfolio Coordinator is running on port 8000\n\nError: ${error instanceof Error ? error.message : 'Connection failed'}\n\nRun: python run_backend_v2.py`,
        sender: 'agent',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, agentMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const generateResponse = (userInput: string): string => {
    const lower = userInput.toLowerCase()

    if (lower.includes('invest') || lower.includes('eth') || lower.includes('usdc')) {
      return `✅ Investment Request Parsed!\n\n🔄 Coordinating my agent swarm:\n• 📡 Chain Scanner - Scanning opportunities...\n• 🧠 MeTTa Knowledge - Analyzing protocols...\n• ⚙️ Strategy Engine - Optimizing allocation...\n\nExpected APY: 8-12%\nRisk Score: Moderate (4.5/10)\n\n💡 In production, I would execute across Ethereum, Polygon, and Arbitrum with MEV protection!`
    }

    if (lower.includes('help') || lower.includes('how')) {
      return `🤖 YieldSwarm AI Commands:\n\n💰 Investment: "Invest [amount] [currency] with [risk] risk"\n📊 Portfolio: "Show my portfolio"\n📈 Status: "What's the best strategy?"\n\nRisk Levels: conservative, moderate, aggressive\nChains: Ethereum, Solana, BSC, Polygon, Arbitrum\n\nMy 6 agents:\n• Chain Scanner - 24/7 monitoring\n• MeTTa Knowledge - DeFi intelligence\n• Strategy Engine - Optimization\n• Execution Agent - Safe execution\n• Performance Tracker - Analytics`
    }

    if (lower.includes('portfolio') || lower.includes('status') || lower.includes('performance')) {
      return `📊 Portfolio Status:\n\nTotal Value: 12.45 ETH\nP&L 24h: +0.58 ETH (+4.87%)\nRealized APY: 11.2%\n\nActive Positions:\n• Aave V3 (Ethereum): 5 ETH @ 4.2% APY\n• Uniswap V3 (Polygon): 4 ETH @ 12.5% APY\n• Raydium (Solana): 3.45 ETH @ 18.3% APY\n\nGas Spent: 0.02 ETH\n\n✨ Beating market average by 15%!`
    }

    return `I understand you're interested in DeFi yield optimization! Try:\n\n• "Invest 10 ETH with moderate risk"\n• "Show my portfolio"\n• "Help"\n\nI coordinate 6 specialized agents to maximize your returns across 5 blockchains! 🐝`
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 Chat with YieldSwarm AI</h2>
        <span className="status-badge">🟢 Online</span>
      </div>

      <div className="messages-container">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            <div className="message-content">
              <div className="message-avatar">
                {msg.sender === 'agent' ? '🐝' : '👤'}
              </div>
              <div className="message-bubble">
                <p className="message-text">{msg.text}</p>
                <span className="message-time">
                  {msg.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message agent">
            <div className="message-content">
              <div className="message-avatar">🐝</div>
              <div className="message-bubble loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me to optimize your DeFi yields..."
          rows={2}
          disabled={isLoading}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? '⏳' : '🚀'} Send
        </button>
      </div>

      <div className="quick-actions">
        <button onClick={() => setInput('Invest 10 ETH with moderate risk')}>
          💰 Quick Invest
        </button>
        <button onClick={() => setInput('Show my portfolio')}>
          📊 My Portfolio
        </button>
        <button onClick={() => setInput('Help')}>
          ❓ Help
        </button>
      </div>

      {/* Show allocation chart if there are investment messages */}
      {messages.some(m => m.text.toLowerCase().includes('invest') && m.sender === 'agent') && (
        <AllocationChart />
      )}
    </div>
  )
}
