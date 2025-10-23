<p align="center">
    <img src="https://github.com/programmerer1/airdrop-eligibility-agent/blob/main/logo.png" width="300" alt="logo">
</p>

# Airdrop Eligibility Checker Agent
This Python-based async agent is designed to swiftly check a given Ethereum Virtual Machine (EVM) address for token airdrop eligibility across multiple blockchain networks and smart contracts simultaneously.

Built using the **Sentient Agent Framework**  
https://github.com/sentient-agi/Sentient-Agent-Framework

## Key Features
- Multi-Chain Support: Easily configured to query eligibility on various EVM-compatible chains (e.g., Arbitrum, Linea) using Etherscan/Arbiscan/Lineascan proxy APIs.

- ABI-Driven Calls

- Asynchronous Performance

- Configuration via YAML: Contract addresses, methods, and ABIs are easily managed in a centralized YAML file (contracts.yml).

```yaml
contracts:
  - evm:
    - name: "Arbitrum Airdrop"
      address: "0x67a24ce4321ab3af51c2d0a4801c3e111d88c9d9"
      method: "claimableTokens"
      params: ["{user_address}"] # {user_address} will be changed to the user's address.
      network: "Arbitrum One"
      chainId: 42161
      ticker: "ARB"
      decimals: 18
      abi:
        - inputs:
            - internalType: "address"
              name: ""
              type: "address"
          name: "claimableTokens"
          outputs:
            - internalType: "uint256"
              name: ""
              type: "uint256"
          stateMutability: "view"
          type: "function"

    - name: "Linea Airdrop"
      address: "0x44b265C958b549913c3795664c94B1eB043c835C"
      method: "calculateAllocation"
      params: ["{user_address}"] # {user_address} will be changed to the user's address.
      network: "Linea Mainnet"
      chainId: 59144
      ticker: LINEA
      decimals: 18
      abi:
        - inputs:
            - internalType: "address"
              name: "_account"
              type: "address"
          name: "calculateAllocation"
          outputs:
            - internalType: "uint256"
              name: "tokenAllocation"
              type: "uint256"
          stateMutability: "view"
          type: "function"
```

## Installation
Clone the repository
```
git clone https://github.com/programmerer1/airdrop-eligibility-agent.git

cd airdrop-eligibility-agent

cp .env.example .env

docker compose -f docker-compose.yml up -d
```

**Example POST request to localhost:8000/assist:**
```bash
{
    "session": 
    {
        "processor_id":"sentient-chat-client",
        "activity_id":"01K6BEMNWZFMP3RMGJTFZBND2N",
        "request_id": "01K6BEPKY12FMR1S19Y3SE01C6",
        "interactions":[]
    }, 
    "query": 
    {
        "id": "01K6BEMZ2QZQ58ADNDCKBPKD51", 
        "prompt": "Check my wallet 0x4abaf7b00248bcf38984477be31fa2aeca6ba1a8",
        "context": ""
    }
}
```