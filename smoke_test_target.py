"""Confirm VulnRagTarget forwards a benign prompt to the live server."""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from pyrit.setup import IN_MEMORY, initialize_pyrit_async
from pyrit.models.messages.message import Message
from vuln_rag_target import VulnRagTarget


async def main():
    await initialize_pyrit_async(memory_db_type=IN_MEMORY)
    target = VulnRagTarget(base_url="http://localhost:8000")

    msg = Message.from_prompt(prompt="how do I connect to the vpn?", role="user")
    responses = await target.send_prompt_async(message=msg)

    print("Target replied:")
    print(" ", responses[-1].get_value())


if __name__ == "__main__":
    asyncio.run(main())
