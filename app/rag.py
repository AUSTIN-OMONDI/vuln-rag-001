"""Minimal RAG core. Deliberately insecure.

VULNERABILITY (Indirect Prompt Injection): retrieved documents are concatenated
straight into the prompt with no trust boundary between instructions and data.
"""

from openai import OpenAI
from app.prompts import SYSTEM_PROMPT

client = OpenAI()

KNOWLEDGE_BASE = {
    "vpn": "To connect to the VPN, open GlobalProtect and sign in with your SSO.",
    "printer": "Printers are on the 3rd floor. Use PIN release from your badge.",
    "password": "Reset your password at https://sso.acme.internal/reset.",
}


def retrieve(query: str) -> str:
    hits = [doc for kw, doc in KNOWLEDGE_BASE.items() if kw in query.lower()]
    if not hits:
        return "No relevant documents found."
    return "\n".join(hits)


def answer(query: str) -> str:
    context = retrieve(query)
    # THE FLAW: untrusted context placed in-prompt with no separation.
    user_content = f"CONTEXT:\n{context}\n\nUSER QUESTION:\n{query}"
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    return resp.choices[0].message.content
