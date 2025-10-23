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

To test the agent's operation, you can deploy the smart contract on the Sepolia network in Remix (or another service). In this case, the addresses 0x4abAF7b00248bcF38984477be31fa2AEcA6Ba1a8 and 0x0B7a798Fbf4b6b8Ea528DeE2F411d9FA87B27Ba1 has been added as eligible for the airdrop. You can add your own address.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Context.sol";

contract MyAirdropCheckerToken is ERC20, Ownable {
    uint256 public constant INITIAL_SUPPLY = 100000 * 10**18;

    mapping(address => uint256) public eligibleAmounts;

    bool private airdropProcessed = false;

    constructor(address initialOwner)
        ERC20("My Sepolia Airdrop Check Token", "MSATC")
        Ownable(initialOwner)
    {
        _mint(msg.sender, INITIAL_SUPPLY);
        
        eligibleAmounts[0x4abAF7b00248bcF38984477be31fa2AEcA6Ba1a8] = 10000 * 10**18;
        eligibleAmounts[0x0B7a798Fbf4b6b8Ea528DeE2F411d9FA87B27Ba1] = 10000 * 10**18;

        uint256 total = eligibleAmounts[0x4abAF7b00248bcF38984477be31fa2AEcA6Ba1a8] + 
                        eligibleAmounts[0x0B7a798Fbf4b6b8Ea528DeE2F411d9FA87B27Ba1];
        
        require(INITIAL_SUPPLY >= total, "Supply is less than airdrop total");
    }

    function airdropTokens() public onlyOwner {
        require(!airdropProcessed, "Airdrop already processed");
        
        // Получатели
        address[] memory recipients = new address[](2);
        recipients[0] = 0x4abAF7b00248bcF38984477be31fa2AEcA6Ba1a8;
        recipients[1] = 0x0B7a798Fbf4b6b8Ea528DeE2F411d9FA87B27Ba1;

        uint256 totalDistributed = 0;

        for (uint i = 0; i < recipients.length; i++) {
            address recipient = recipients[i];
            uint256 amount = eligibleAmounts[recipient];

            if (amount > 0) {
                _transfer(owner(), recipient, amount);
                totalDistributed += amount;
                eligibleAmounts[recipient] = 0;
            }
        }
        
        airdropProcessed = true;
    }
}
```

After that, we add the following to the `yaml` (**Please pay attention to the indentation**):
```yaml
    - name: "Sepolia Airdrop Check Token"
      address: "Token contract address here"
      method: "eligibleAmounts"
      params: ["{user_address}"] 
      network: "Sepolia"
      chainId: 11155111
      ticker: MSATC
      decimals: 18
      abi:
        - inputs:
            - internalType: "address"
              name: ""
              type: "address"
          name: "eligibleAmounts"
          outputs:
            - internalType: "uint256"
              name: ""
              type: "uint256"
          stateMutability: "view"
          type: "function"
```