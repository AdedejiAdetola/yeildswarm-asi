; YieldSwarm AI - DeFi Protocol Knowledge Base
; MeTTa Knowledge Graph for Symbolic AI Reasoning

; ===== TYPE DEFINITIONS =====
(: Protocol Type)
(: Chain Type)
(: Risk Type)
(: APY Type)
(: TVL Type)

; ===== PROTOCOL DEFINITIONS =====

; Aave V3 - Leading lending protocol
(= (Protocol Aave-V3)
   (Chains Ethereum Polygon Arbitrum)
   (Type Lending)
   (Risk-Score 2.5)
   (Historical-APY 4.2)
   (TVL 5000000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk None))

; Uniswap V3 - Leading DEX
(= (Protocol Uniswap-V3)
   (Chains Ethereum Polygon Arbitrum)
   (Type DEX)
   (Risk-Score 3.5)
   (Historical-APY 12.5)
   (TVL 3200000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk High))

; Curve - Stablecoin DEX
(= (Protocol Curve)
   (Chains Ethereum Polygon)
   (Type DEX-Stablecoin)
   (Risk-Score 2.1)
   (Historical-APY 6.8)
   (TVL 2800000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk Low))

; Compound V3 - Lending protocol
(= (Protocol Compound-V3)
   (Chains Ethereum Polygon Arbitrum)
   (Type Lending)
   (Risk-Score 2.8)
   (Historical-APY 3.9)
   (TVL 2100000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk None))

; Raydium - Solana DEX
(= (Protocol Raydium)
   (Chains Solana)
   (Type DEX)
   (Risk-Score 6.0)
   (Historical-APY 18.5)
   (TVL 450000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk High))

; Solend - Solana Lending
(= (Protocol Solend)
   (Chains Solana)
   (Type Lending)
   (Risk-Score 5.5)
   (Historical-APY 8.2)
   (TVL 280000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk None))

; PancakeSwap - BSC DEX
(= (Protocol PancakeSwap)
   (Chains BSC)
   (Type DEX)
   (Risk-Score 5.0)
   (Historical-APY 15.2)
   (TVL 1200000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk High))

; Venus - BSC Lending
(= (Protocol Venus)
   (Chains BSC)
   (Type Lending)
   (Risk-Score 4.8)
   (Historical-APY 6.5)
   (TVL 680000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk None))

; GMX - Arbitrum perpetuals
(= (Protocol GMX)
   (Chains Arbitrum)
   (Type Perpetuals)
   (Risk-Score 5.5)
   (Historical-APY 16.0)
   (TVL 420000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk None))

; Balancer - Ethereum DEX
(= (Protocol Balancer)
   (Chains Ethereum Polygon Arbitrum)
   (Type DEX-Weighted)
   (Risk-Score 3.8)
   (Historical-APY 9.5)
   (TVL 980000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk Medium))

; QuickSwap - Polygon DEX
(= (Protocol QuickSwap)
   (Chains Polygon)
   (Type DEX)
   (Risk-Score 4.0)
   (Historical-APY 9.75)
   (TVL 350000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk High))

; Yearn Finance - Yield Aggregator
(= (Protocol Yearn-Finance)
   (Chains Ethereum Polygon Arbitrum)
   (Type Yield-Aggregator)
   (Risk-Score 3.2)
   (Historical-APY 7.8)
   (TVL 1500000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk Low))

; Convex Finance - Curve Booster
(= (Protocol Convex)
   (Chains Ethereum)
   (Type Yield-Booster)
   (Risk-Score 3.5)
   (Historical-APY 8.5)
   (TVL 2300000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk Low))

; Maker DAO - Stablecoin Protocol
(= (Protocol MakerDAO)
   (Chains Ethereum)
   (Type Lending-Stablecoin)
   (Risk-Score 2.0)
   (Historical-APY 3.5)
   (TVL 6800000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk None))

; Lido - Liquid Staking
(= (Protocol Lido)
   (Chains Ethereum Polygon Solana)
   (Type Liquid-Staking)
   (Risk-Score 2.3)
   (Historical-APY 4.5)
   (TVL 14000000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk None))

; Rocket Pool - ETH Staking
(= (Protocol Rocket-Pool)
   (Chains Ethereum)
   (Type Liquid-Staking)
   (Risk-Score 2.6)
   (Historical-APY 4.2)
   (TVL 2100000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk None))

; Stargate - Bridge Protocol
(= (Protocol Stargate)
   (Chains Ethereum Polygon Arbitrum BSC)
   (Type Bridge-Liquidity)
   (Risk-Score 4.5)
   (Historical-APY 11.5)
   (TVL 680000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk Medium))

; Frax Finance - Stablecoin Protocol
(= (Protocol Frax)
   (Chains Ethereum Polygon Arbitrum)
   (Type Stablecoin-Lending)
   (Risk-Score 3.0)
   (Historical-APY 5.5)
   (TVL 1100000000)
   (Smart-Contract-Audited True)
   (Security-Rating High)
   (Impermanent-Loss-Risk Low))

; Trader Joe - Avalanche DEX (extended to Arbitrum)
(= (Protocol Trader-Joe)
   (Chains Arbitrum)
   (Type DEX)
   (Risk-Score 4.8)
   (Historical-APY 13.5)
   (TVL 420000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk High))

; Synapse Protocol - Cross-Chain Bridge
(= (Protocol Synapse)
   (Chains Ethereum Polygon Arbitrum BSC)
   (Type Bridge-Yield)
   (Risk-Score 5.2)
   (Historical-APY 14.0)
   (TVL 380000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk Medium))

; Beefy Finance - Yield Optimizer
(= (Protocol Beefy)
   (Chains Polygon BSC Arbitrum)
   (Type Yield-Optimizer)
   (Risk-Score 4.2)
   (Historical-APY 10.5)
   (TVL 550000000)
   (Smart-Contract-Audited True)
   (Security-Rating Medium)
   (Impermanent-Loss-Risk Medium))

; ===== RISK ASSESSMENT RULES =====

(= (Assess-Risk $Protocol $Risk-Level)
   (match &atomspace
     ((Protocol $Protocol) (Risk-Score $Score))
     (if (<= $Score 3.0)
         (Good-For Conservative Moderate Aggressive)
         (if (<= $Score 5.0)
             (Good-For Moderate Aggressive)
             (Good-For Aggressive)))))

; ===== STRATEGY SELECTION =====

(= (Find-Best-Protocols $Amount $Risk-Level $Chains)
   (match &atomspace
     ((Protocol $P) (Chains $ChainList) (Risk-Score $R) (Historical-APY $A))
     (if (and (Member $Chains $ChainList)
              (Good-For-Risk $R $Risk-Level))
         (Recommend $P $R $A))))

; Conservative: Risk <= 3.0
(= (Good-For-Risk $Score conservative)
   (<= $Score 3.0))

; Moderate: Risk <= 5.0
(= (Good-For-Risk $Score moderate)
   (<= $Score 5.0))

; Aggressive: Risk <= 8.0
(= (Good-For-Risk $Score aggressive)
   (<= $Score 8.0))

; ===== ALLOCATION OPTIMIZATION =====

(= (Optimize-Allocation $Protocols $Risk-Level)
   (case $Risk-Level
     (conservative (Conservative-Split $Protocols))
     (moderate (Moderate-Split $Protocols))
     (aggressive (Aggressive-Split $Protocols))))

; Conservative: Higher allocation to low-risk protocols
(= (Conservative-Split $Protocols)
   (Allocate (50 30 15 5)))

; Moderate: Balanced allocation
(= (Moderate-Split $Protocols)
   (Allocate (35 30 20 15)))

; Aggressive: More even distribution
(= (Aggressive-Split $Protocols)
   (Allocate (40 30 20 10)))

; ===== CHAIN PREFERENCES =====

(= (Chain-Risk Ethereum) 1.0)
(= (Chain-Risk Polygon) 1.2)
(= (Chain-Risk Arbitrum) 1.3)
(= (Chain-Risk BSC) 1.5)
(= (Chain-Risk Solana) 1.8)

; ===== HISTORICAL PERFORMANCE =====

(= (Historical-Performance Aave-V3 2025-01) 4.2)
(= (Historical-Performance Uniswap-V3 2025-01) 12.5)
(= (Historical-Performance Curve 2025-01) 6.8)
(= (Historical-Performance Compound-V3 2025-01) 3.9)
(= (Historical-Performance Raydium 2025-01) 18.5)
(= (Historical-Performance Solend 2025-01) 8.2)
(= (Historical-Performance PancakeSwap 2025-01) 15.2)
(= (Historical-Performance Venus 2025-01) 6.5)
(= (Historical-Performance GMX 2025-01) 16.0)
(= (Historical-Performance Balancer 2025-01) 9.5)

; ===== DIVERSIFICATION RULES =====

; Avoid over-concentration in single protocol type
(= (Diversification-Check $Allocations)
   (let (($dex-count (Count-Type $Allocations DEX))
         ($lending-count (Count-Type $Allocations Lending)))
     (if (> $dex-count 70)
         (Warning Too-Much-DEX-Exposure)
         (if (> $lending-count 70)
             (Warning Too-Much-Lending-Exposure)
             (Pass)))))

; Prefer protocols with high TVL for large amounts
(= (TVL-Safety-Check $Amount $Protocol)
   (match &atomspace
     ((Protocol $Protocol) (TVL $TVL))
     (if (> $Amount (/ $TVL 100))
         (Warning High-Amount-For-Pool)
         (Pass))))

; ===== REASONING FUNCTIONS =====

(= (Explain-Choice $Protocol $Risk-Level)
   (match &atomspace
     ((Protocol $Protocol) (Risk-Score $R) (Historical-APY $A) (TVL $T))
     (Reasoning
       (Protocol-Name $Protocol)
       (Risk-Appropriate $R $Risk-Level)
       (Expected-Return $A)
       (Liquidity-Depth $T)
       (Smart-Contract-Security High))))

; Generate reasoning for protocol selection
(= (Generate-Reasoning $Protocols $Risk-Level)
   (concat
     (Risk-Level-Explanation $Risk-Level)
     (Protocol-Justifications $Protocols)
     (Diversification-Rationale $Protocols)))

(= (Risk-Level-Explanation conservative)
   "Conservative strategy prioritizes capital preservation with lower-risk protocols like Aave and Curve.")

(= (Risk-Level-Explanation moderate)
   "Moderate strategy balances risk and reward with a mix of lending protocols and established DEXes.")

(= (Risk-Level-Explanation aggressive)
   "Aggressive strategy maximizes potential returns with higher-risk, higher-yield opportunities across multiple chains.")

; ===== CROSS-CHAIN OPTIMIZATION =====

; Prefer single-chain deployments for small amounts (gas efficiency)
(= (Chain-Optimization $Amount $Chains)
   (if (< $Amount 5.0)
       (Single-Chain-Preferred $Chains)
       (Multi-Chain-Allowed $Chains)))

; Suggest bridging if significantly better opportunities exist
(= (Bridge-Opportunity-Check $Amount $CurrentChain $TargetChain)
   (let (($current-apy (Best-APY $CurrentChain))
         ($target-apy (Best-APY $TargetChain))
         ($bridge-cost (Estimate-Bridge-Cost $Amount)))
     (if (> (- $target-apy $current-apy) 3.0)
         (Recommend-Bridge $TargetChain $bridge-cost)
         (Stay-On-Current-Chain))))

; ===== PROTOCOL CORRELATION =====

; Protocols on same chain have higher correlation
(= (Protocol-Correlation $Protocol1 $Protocol2)
   (match &atomspace
     ((Protocol $Protocol1) (Chains $Chains1))
     ((Protocol $Protocol2) (Chains $Chains2))
     (if (Has-Common-Chain $Chains1 $Chains2)
         (Correlation High)
         (Correlation Low))))

; ===== GAS ESTIMATION =====

(= (Estimate-Gas-Cost $Chain $Protocol $Action)
   (case $Chain
     (Ethereum (Ethereum-Gas $Protocol $Action))
     (Polygon (Polygon-Gas $Protocol $Action))
     (Arbitrum (Arbitrum-Gas $Protocol $Action))
     (BSC (BSC-Gas $Protocol $Action))
     (Solana (Solana-Gas $Protocol $Action))))

; Ethereum gas costs (in ETH)
(= (Ethereum-Gas $Protocol deposit) 0.015)
(= (Ethereum-Gas $Protocol swap) 0.020)
(= (Ethereum-Gas $Protocol withdraw) 0.012)

; Polygon gas costs (in MATIC, converted to ETH equivalent)
(= (Polygon-Gas $Protocol deposit) 0.0001)
(= (Polygon-Gas $Protocol swap) 0.0002)
(= (Polygon-Gas $Protocol withdraw) 0.0001)

; Arbitrum gas costs
(= (Arbitrum-Gas $Protocol deposit) 0.0008)
(= (Arbitrum-Gas $Protocol swap) 0.0012)
(= (Arbitrum-Gas $Protocol withdraw) 0.0007)

; BSC gas costs
(= (BSC-Gas $Protocol deposit) 0.0002)
(= (BSC-Gas $Protocol swap) 0.0003)
(= (BSC-Gas $Protocol withdraw) 0.0002)

; Solana gas costs
(= (Solana-Gas $Protocol deposit) 0.00001)
(= (Solana-Gas $Protocol swap) 0.00002)
(= (Solana-Gas $Protocol withdraw) 0.00001)

; ===== END OF KNOWLEDGE BASE =====
