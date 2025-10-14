import { useState, useEffect } from 'react'
import '../styles/AgentStatus.css'

interface Agent {
  name: string
  status: 'online' | 'busy' | 'offline'
  icon: string
  lastActivity: string
  tasksCompleted: number
}

export default function AgentStatus() {
  const [agents, setAgents] = useState<Agent[]>([
    {
      name: 'Portfolio Coordinator',
      status: 'online',
      icon: '🎯',
      lastActivity: 'Just now',
      tasksCompleted: 47
    },
    {
      name: 'Chain Scanner',
      status: 'busy',
      icon: '📡',
      lastActivity: '2s ago',
      tasksCompleted: 1523
    },
    {
      name: 'MeTTa Knowledge',
      status: 'online',
      icon: '🧠',
      lastActivity: '5s ago',
      tasksCompleted: 289
    },
    {
      name: 'Strategy Engine',
      status: 'busy',
      icon: '⚙️',
      lastActivity: '1s ago',
      tasksCompleted: 156
    },
    {
      name: 'Execution Agent',
      status: 'online',
      icon: '🔒',
      lastActivity: '10s ago',
      tasksCompleted: 78
    },
    {
      name: 'Performance Tracker',
      status: 'online',
      icon: '📊',
      lastActivity: '3s ago',
      tasksCompleted: 234
    }
  ])

  // Fetch real agent status from backend
  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const response = await fetch('/api/agents/status')
        if (response.ok) {
          const data = await response.json()
          // Update agents with real status
          setAgents(prev => prev.map(agent => {
            const realStatus = data[agent.name.toLowerCase().replace(/\s+/g, '_')]
            if (realStatus) {
              return {
                ...agent,
                status: realStatus.online ? 'online' : 'offline',
                lastActivity: realStatus.lastActivity || agent.lastActivity
              }
            }
            return agent
          }))
        }
      } catch (error) {
        // Keep simulated status if backend is unavailable
        console.log('Using simulated agent status')
      }
    }

    // Fetch initially
    fetchAgentStatus()

    // Poll every 5 seconds
    const interval = setInterval(() => {
      fetchAgentStatus()
      // Also simulate activity animation
      setAgents(prev => prev.map(agent => ({
        ...agent,
        status: agent.status === 'offline' ? 'offline' : (Math.random() > 0.7 ? 'busy' : 'online'),
        tasksCompleted: agent.tasksCompleted + (Math.random() > 0.5 ? 1 : 0)
      })))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const onlineCount = agents.filter(a => a.status !== 'offline').length

  return (
    <div className="agent-status">
      <div className="status-header">
        <h3>🐝 Agent Swarm</h3>
        <span className="agent-count">
          {onlineCount}/{agents.length} Online
        </span>
      </div>

      <div className="agents-list">
        {agents.map((agent, idx) => (
          <div key={idx} className={`agent-card ${agent.status}`}>
            <div className="agent-icon">{agent.icon}</div>
            <div className="agent-info">
              <div className="agent-name">{agent.name}</div>
              <div className="agent-meta">
                <span className={`status-dot ${agent.status}`} />
                <span className="agent-activity">{agent.lastActivity}</span>
              </div>
              <div className="agent-stats">
                {agent.tasksCompleted} tasks
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="swarm-stats">
        <div className="swarm-stat">
          <span className="stat-label">Total Tasks</span>
          <span className="stat-value">
            {agents.reduce((sum, a) => sum + a.tasksCompleted, 0)}
          </span>
        </div>
        <div className="swarm-stat">
          <span className="stat-label">Uptime</span>
          <span className="stat-value">99.8%</span>
        </div>
      </div>

      <div className="system-info">
        <div className="info-badge">
          <span>🔗 Agentverse</span>
        </div>
        <div className="info-badge">
          <span>🌐 ASI:One</span>
        </div>
        <div className="info-badge">
          <span>🧠 MeTTa AI</span>
        </div>
      </div>
    </div>
  )
}
