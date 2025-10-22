import httpx
import json
from .config import MODEL_API_URL, MODEL_NAME, MODEL_API_KEY
from .prompts.formatter import system_prompt, user_prompt_template

class ResponseFormatter:
    async def format(self, result: dict, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {MODEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        system_instruction = {
            "role": "system",
            "content": system_prompt
        }

        user_message = {
            "role": "user",
            "content": user_prompt_template.format(
                user_prompt=user_prompt,
                result=result
            )
        }

        payload = {
            "model": MODEL_NAME,
            "max_tokens" : 8192,
            "top_p" : 1,
            "presence_penalty" : 0,
            "frequency_penalty" : 0,
            "temperature" : 0.0,
            "messages": [
                system_instruction,
                user_message
            ]
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(MODEL_API_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        return (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "Report formatting failed.")
        )
