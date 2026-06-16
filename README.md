# vuln-rag-001

An intentionally vulnerable RAG application for AI security research.

## Stack

- FastAPI
- LangChain
- ChromaDB
- OpenAI

## Intended Vulnerabilities

### Direct Prompt Injection

No protection against instruction override.

### Indirect Prompt Injection

Malicious documents can alter model behavior.

### System Prompt Leakage

Sensitive information stored in the system prompt.

### Tool Abuse

Unsafe web fetch and file read tools.

### SSRF

Web fetch tool performs unrestricted requests.

### Arbitrary File Read

No path validation.

### RAG Poisoning

Retriever trusts all ingested documents.

### Output Handling Vulnerability

Unsanitized model responses may contain HTML or JavaScript.