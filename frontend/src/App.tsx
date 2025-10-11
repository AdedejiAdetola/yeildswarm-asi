import { useState } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'
import PortfolioDashboard from './components/PortfolioDashboard'
import AgentStatus from './components/AgentStatus'

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'portfolio'>('chat')

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🐝 YieldSwarm AI</h1>
          <p>Autonomous DeFi Yield Optimizer</p>
        </div>
        <nav className="header-nav">
          <button
            className={activeTab === 'chat' ? 'active' : ''}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            className={activeTab === 'portfolio' ? 'active' : ''}
            onClick={() => setActiveTab('portfolio')}
          >
            📊 Portfolio
          </button>
        </nav>
      </header>

      <main className="app-main">
        <div className="main-content">
          {activeTab === 'chat' ? (
            <ChatInterface />
          ) : (
            <PortfolioDashboard />
          )}
        </div>

        <aside className="sidebar">
          <AgentStatus />
        </aside>
      </main>

      <footer className="app-footer">
        <p>🏆 ASI Alliance Hackathon 2025 | Innovation Lab</p>
      </footer>
    </div>
  )
}

export default App
