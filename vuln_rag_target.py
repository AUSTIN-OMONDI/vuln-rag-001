"""
Custom PyRIT PromptTarget for vuln-rag-001.

Forwards each prompt to the local FastAPI /chat endpoint instead of calling an
LLM provider directly. Once you can wrap an arbitrary HTTP endpoint as a
PromptTarget, PyRIT can attack ANY target you can reach over HTTP.

Interface verified via inspect.signature:
  - implement ONE abstract method: _send_prompt_to_target_async
  - it receives  normalized_conversation: list[Message]  (current msg last)
  - it returns   list[Message]
  - read text with  message.get_value()
  - build reply with  Message.from_prompt(prompt=..., role="assistant")
"""

import httpx
from pyrit.prompt_target import PromptTarget
from pyrit.models.messages.message import Message


class VulnRagTarget(PromptTarget):
    """PyRIT target that POSTs prompts to vuln-rag-001's /chat endpoint."""

    def __init__(self, *, base_url: str = "http://localhost:8000", verbose: bool = False):
        super().__init__(verbose=verbose)
        self._chat_url = f"{base_url.rstrip('/')}/chat"

    async def _send_prompt_to_target_async(
        self, *, normalized_conversation: list[Message]
    ) -> list[Message]:
        current = normalized_conversation[-1]
        prompt_text = current.get_value()

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(self._chat_url, json={"message": prompt_text})
            resp.raise_for_status()
            answer = resp.json()["response"]

        return [Message.from_prompt(prompt=answer, role="assistant")]

    def _validate_request(self, *, normalized_conversation: list[Message]) -> None:
        current = normalized_conversation[-1]
        if len(current.message_pieces) != 1:
            raise ValueError("VulnRagTarget supports exactly one message piece.")
