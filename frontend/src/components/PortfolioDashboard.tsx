import { useState, useEffect } from 'react'
import '../styles/PortfolioDashboard.css'

interface Position {
  protocol: string
  chain: string
  amount: number
  apy: number
  value: number
  pnl: number
}

export default function PortfolioDashboard() {
  const [positions] = useState<Position[]>([
    {
      protocol: 'Aave V3',
      chain: 'Ethereum',
      amount: 5.0,
      apy: 4.2,
      value: 5.12,
      pnl: 0.12
    },
    {
      protocol: 'Uniswap V3',
      chain: 'Polygon',
      amount: 4.0,
      apy: 12.5,
      value: 4.28,
      pnl: 0.28
    },
    {
      protocol: 'Raydium',
      chain: 'Solana',
      amount: 3.45,
      apy: 18.3,
      value: 3.63,
      pnl: 0.18
    }
  ])

  const totalValue = positions.reduce((sum, pos) => sum + pos.value, 0)
  const totalPnL = positions.reduce((sum, pos) => sum + pos.pnl, 0)
  const avgAPY = positions.reduce((sum, pos) => sum + pos.apy, 0) / positions.length

  return (
    <div className="portfolio-dashboard">
      <div className="dashboard-header">
        <h2>📊 Your Portfolio</h2>
        <button className="refresh-button">🔄 Refresh</button>
      </div>

      <div className="portfolio-stats">
        <div className="stat-card total">
          <div className="stat-icon">💎</div>
          <div className="stat-content">
            <span className="stat-label">Total Value</span>
            <span className="stat-value">{totalValue.toFixed(2)} ETH</span>
            <span className="stat-sub">${(totalValue * 2500).toFixed(2)}</span>
          </div>
        </div>

        <div className="stat-card pnl">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <span className="stat-label">24h P&L</span>
            <span className="stat-value positive">+{totalPnL.toFixed(2)} ETH</span>
            <span className="stat-sub">+{((totalPnL / totalValue) * 100).toFixed(2)}%</span>
          </div>
        </div>

        <div className="stat-card apy">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <span className="stat-label">Avg APY</span>
            <span className="stat-value">{avgAPY.toFixed(1)}%</span>
            <span className="stat-sub">Across {positions.length} positions</span>
          </div>
        </div>

        <div className="stat-card gas">
          <div className="stat-icon">⛽</div>
          <div className="stat-content">
            <span className="stat-label">Gas Spent</span>
            <span className="stat-value">0.02 ETH</span>
            <span className="stat-sub">$50.00</span>
          </div>
        </div>
      </div>

      <div className="positions-table">
        <h3>Active Positions</h3>
        <table>
          <thead>
            <tr>
              <th>Protocol</th>
              <th>Chain</th>
              <th>Amount</th>
              <th>APY</th>
              <th>Value</th>
              <th>P&L</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((pos, idx) => (
              <tr key={idx}>
                <td>
                  <strong>{pos.protocol}</strong>
                </td>
                <td>
                  <span className={`chain-badge ${pos.chain.toLowerCase()}`}>
                    {pos.chain}
                  </span>
                </td>
                <td>{pos.amount.toFixed(2)} ETH</td>
                <td className="apy-cell">{pos.apy.toFixed(1)}%</td>
                <td>{pos.value.toFixed(2)} ETH</td>
                <td className={pos.pnl >= 0 ? 'positive' : 'negative'}>
                  {pos.pnl >= 0 ? '+' : ''}{pos.pnl.toFixed(2)} ETH
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="performance-chart">
        <h3>Performance Overview</h3>
        <div className="chart-placeholder">
          <div className="chart-bars">
            {positions.map((pos, idx) => (
              <div key={idx} className="chart-bar">
                <div
                  className="bar-fill"
                  style={{ height: `${(pos.apy / 20) * 100}%` }}
                />
                <span className="bar-label">{pos.protocol.split(' ')[0]}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="dashboard-actions">
        <button className="action-button primary">
          💰 Add Funds
        </button>
        <button className="action-button">
          🔄 Rebalance
        </button>
        <button className="action-button">
          📥 Withdraw
        </button>
        <button className="action-button">
          📄 Export Report
        </button>
      </div>
    </div>
  )
}
