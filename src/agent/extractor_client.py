import json
import httpx
from .config import EXTRACTOR_MODEL_API_URL, EXTRACTOR_MODEL_NAME, EXTRACTOR_MODEL_API_KEY
from .prompts.extractor import system_prompt

class Extractor:
    async def extract(self, prompt: str) -> dict:
        headers = {
            "Authorization": f"Bearer {EXTRACTOR_MODEL_API_KEY}",
            "Content-Type": "application/json"
        }

        system_instruction = {
            "role": "system",
            "content": system_prompt
        }
        
        payload = {
            "model": EXTRACTOR_MODEL_NAME,
            "max_tokens" : 2000,
            "top_p" : 1,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "temperature" : 0.0,
            "messages": [
                system_instruction,
                {"role": "user", "content": prompt}
            ]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(EXTRACTOR_MODEL_API_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
        content = (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "{}")
        )

        return self.normalize_response(json.loads(content))

    def normalize_response(self, data: dict) -> dict:
        if not data:
            return {}

        address = data.get("address", {})

        if not address:
            return {}

        return address