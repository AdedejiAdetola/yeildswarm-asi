/**
 * API client for communicating with YieldSwarm AI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export interface AgentStatus {
  name: string;
  status: 'online' | 'busy' | 'offline';
  icon: string;
  lastActivity: string;
  tasksCompleted: number;
}

export interface ChatResponse {
  success: boolean;
  response: string;
}

export interface InvestmentRequest {
  userId: string;
  amount: number;
  currency: string;
  riskLevel: 'conservative' | 'moderate' | 'aggressive';
  chains: string[];
}

export interface PortfolioStats {
  totalValue: number;
  totalInvested: number;
  totalPnl: number;
  avgApy: number;
}

export interface Position {
  protocol: string;
  chain: string;
  amount: number;
  apy: number;
  value: number;
  pnl: number;
}

export interface Portfolio {
  userId: string;
  stats: PortfolioStats;
  positions: Position[];
  lastUpdated: string;
}

export interface Opportunity {
  protocol: string;
  chain: string;
  apy: number;
  tvl: number;
  riskScore: number;
  category: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    return this.request('/api/health');
  }

  async getAgentStatuses(): Promise<AgentStatus[]> {
    return this.request('/api/agents/status');
  }

  async sendChatMessage(text: string, userId: string): Promise<ChatResponse> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ text, user_id: userId }),
    });
  }

  async createInvestment(request: InvestmentRequest): Promise<any> {
    return this.request('/api/invest', {
      method: 'POST',
      body: JSON.stringify({
        user_id: request.userId,
        amount: request.amount,
        currency: request.currency,
        risk_level: request.riskLevel,
        chains: request.chains,
      }),
    });
  }

  async getPortfolio(userId: string): Promise<Portfolio> {
    return this.request(`/api/portfolio/${userId}`);
  }

  async getOpportunities(): Promise<{ success: boolean; opportunities: Opportunity[] }> {
    return this.request('/api/opportunities');
  }

  // WebSocket connection for real-time updates
  connectWebSocket(userId: string, onMessage: (data: any) => void): WebSocket {
    const wsUrl = this.baseUrl.replace('http', 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/${userId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return ws;
  }
}

export const api = new ApiClient();
export default api;
