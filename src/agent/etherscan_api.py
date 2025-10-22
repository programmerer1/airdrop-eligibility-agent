import yaml
import asyncio
import aiohttp
import logging
from eth_abi import encode
from eth_utils import keccak
from .config import ETHERSCAN_API_KEY, ETHERSCAN_API_URL, ETHERSCAN_DELAY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class EtherscanApi:
    """
    Checks user eligibility for airdrops by calling read-only contract methods
    (e.g. claimableTokens) via the Etherscan V2 proxy endpoint.
    """

    def __init__(self) -> None:
        """
        Load YAML config on initialization.
        """
        with open("src/agent/contracts.yml", "r") as f:
            data = yaml.safe_load(f)
            self.contracts = data.get("contracts", [])[0].get("evm", [])

    async def _query_contract(self, session: aiohttp.ClientSession, contract: dict, user_address: str) -> dict:
        """
        Query a single contract. If ABI, method, or chainId are missing — skip.
        If response result is empty or 0x — skip without writing to JSON.
        """

        name = contract.get("name", "Unknown")
        address = contract.get("address")
        method = contract.get("method")
        chain_id = contract.get("chainId")
        abi = contract.get("abi")

        # Validation
        if not abi:
            logging.warning(f"[{name}] Missing ABI — skipped.")
            return {"status": "skipped", "contract": name}
        if not method:
            logging.warning(f"[{name}] Missing method — skipped.")
            return {"status": "skipped", "contract": name}
        if not chain_id:
            logging.warning(f"[{name}] Missing chainId — skipped.")
            return {"status": "skipped", "contract": name}

        # Find ABI for the target method
        func_abi = next((item for item in abi if item.get("name") == method and item.get("type") == "function"), None)
        if not func_abi:
            logging.warning(f"[{name}] Method '{method}' not found in ABI — skipped.")
            return {"status": "skipped", "contract": name}

        # Extract input types from ABI
        input_types = [i["type"] for i in func_abi.get("inputs", [])]
        raw_params = contract.get("params", [])

        # Normalize params (replace {user_address} and cast types)
        try:
            processed_params = [
                self._normalize_param(user_address if p == "{user_address}" else p, t)
                for p, t in zip(raw_params, input_types)
            ]
        except Exception as e:
            logging.warning(f"[{name}] Parameter normalization error: {e}")
            return {"status": "skipped", "contract": name}

        # Check params count
        if len(input_types) != len(processed_params):
            logging.warning(f"[{name}] Params mismatch (expected {len(input_types)}, got {len(processed_params)}) — skipped.")
            return {"status": "skipped", "contract": name}

        # Encode function call
        data = self._prepare_call_data(method, input_types, processed_params)

        # Build Etherscan API query
        params = {
            "chainid": chain_id,
            "module": "proxy",
            "action": "eth_call",
            "to": address,
            "data": data,
            "tag": "latest",
            "apikey": ETHERSCAN_API_KEY
        }
        url = f"{ETHERSCAN_API_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

        # Execute request
        async with session.get(url, timeout=30) as resp:
            result = await resp.json()

        if ETHERSCAN_DELAY > 0:
            await asyncio.sleep(ETHERSCAN_DELAY)

        # Parse response
        hex_result = result.get("result")
        if not hex_result or hex_result == "0x":
            logging.info(f"[{name}] Returned empty or zero result — skipped.")
            return {"status": "skipped", "contract": name}

        eligible = int(hex_result, 16)

        return {
            "status": "ok",
            "contract": name,
            "eligible": eligible
        }

    @staticmethod
    def _prepare_call_data(method_name: str, input_types: list, processed_params: list) -> str:
        """
        Prepare the data field for eth_call (selector + encoded args).
        """
        function_signature = f"{method_name}({','.join(input_types)})"
        selector = keccak(text=function_signature)[:4]
        encoded_args = encode(input_types, processed_params)
        return "0x" + (selector + encoded_args).hex()

    @staticmethod
    def _normalize_param(value: str, param_type: str):
        """
        Normalize and cast parameter values based on ABI type.
        """
        if param_type.startswith("uint") or param_type.startswith("int"):
            return int(value, 0)  # auto-handles 0x-prefixed numbers
        if param_type == "address":
            return value.lower()
        if param_type == "bool":
            return value.lower() in ("true", "1")
        return value

    async def check_eligibility(self, user_address: str) -> dict:
        """
        Public method: checks eligibility for all configured EVM contracts.
        Returns only non-skipped results.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._query_contract(session, c, user_address) for c in self.contracts]
            results = await asyncio.gather(*tasks)

        # Filter out skipped results (to avoid "0x" noise)
        results = [r for r in results if r.get("status") == "ok"]

        return {"wallet": user_address, "results": results}
