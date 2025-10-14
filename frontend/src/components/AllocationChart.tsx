import { useState, useEffect } from 'react'
import '../styles/AllocationChart.css'

interface Allocation {
  protocol: string
  chain: string
  amount: number
  percentage: number
  apy: number
  color: string
}

export default function AllocationChart() {
  const [allocations, setAllocations] = useState<Allocation[]>([
    {
      protocol: 'Aave V3',
      chain: 'Ethereum',
      amount: 3.0,
      percentage: 30,
      apy: 5.8,
      color: '#8B5CF6'
    },
    {
      protocol: 'Uniswap V3',
      chain: 'Polygon',
      amount: 3.5,
      percentage: 35,
      apy: 12.5,
      color: '#3B82F6'
    },
    {
      protocol: 'Raydium',
      chain: 'Solana',
      amount: 2.0,
      percentage: 20,
      apy: 18.2,
      color: '#10B981'
    },
    {
      protocol: 'GMX',
      chain: 'Arbitrum',
      amount: 1.5,
      percentage: 15,
      apy: 14.5,
      color: '#F59E0B'
    }
  ])

  const totalAmount = allocations.reduce((sum, a) => sum + a.amount, 0)
  const weightedAPY = allocations.reduce((sum, a) => sum + (a.apy * a.percentage / 100), 0)

  // Generate conic gradient for pie chart
  let gradientStops = []
  let currentPercentage = 0
  for (const alloc of allocations) {
    gradientStops.push(`${alloc.color} ${currentPercentage}%`)
    currentPercentage += alloc.percentage
    gradientStops.push(`${alloc.color} ${currentPercentage}%`)
  }
  const conicGradient = `conic-gradient(${gradientStops.join(', ')})`

  return (
    <div className="allocation-chart">
      <div className="chart-header">
        <h3>📊 Portfolio Allocation</h3>
        <div className="chart-summary">
          <div className="summary-item">
            <span className="label">Total:</span>
            <span className="value">{totalAmount.toFixed(2)} ETH</span>
          </div>
          <div className="summary-item">
            <span className="label">Avg APY:</span>
            <span className="value">{weightedAPY.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      <div className="chart-container">
        <div className="pie-chart" style={{ background: conicGradient }}>
          <div className="pie-center">
            <div className="center-amount">{totalAmount.toFixed(1)}</div>
            <div className="center-label">ETH</div>
          </div>
        </div>
      </div>

      <div className="allocation-legend">
        {allocations.map((alloc, idx) => (
          <div key={idx} className="legend-item">
            <div className="legend-color" style={{ backgroundColor: alloc.color }} />
            <div className="legend-info">
              <div className="legend-name">
                {alloc.protocol}
                <span className="chain-badge">{alloc.chain}</span>
              </div>
              <div className="legend-stats">
                <span>{alloc.amount.toFixed(2)} ETH ({alloc.percentage}%)</span>
                <span className="apy-badge">{alloc.apy}% APY</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="chart-footer">
        <div className="footer-stat">
          <span className="stat-icon">💰</span>
          <div className="stat-details">
            <div className="stat-label">Est. Annual Return</div>
            <div className="stat-value">+{(totalAmount * weightedAPY / 100).toFixed(2)} ETH</div>
          </div>
        </div>
        <div className="footer-stat">
          <span className="stat-icon">⚖️</span>
          <div className="stat-details">
            <div className="stat-label">Risk Score</div>
            <div className="stat-value">4.2/10</div>
          </div>
        </div>
      </div>
    </div>
  )
}
