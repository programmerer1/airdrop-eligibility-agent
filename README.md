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

<p align="center">
    <img src="https://github.com/programmerer1/airdrop-eligibility-agent/blob/main/yaml.png" alt="yaml">
</p>

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