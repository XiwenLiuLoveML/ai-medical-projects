# 🤖 Agent Module for Medical Q&A System

This folder contains **agent-level logic** for our medical Q&A system. These agents manage tasks such as **query interpretation**, **keyword extraction**, and **knowledge base retrieval orchestration**.

> ❗️Note:  
> This project is designed for **offline medical environments**.  
> It does **not perform any web search or internet-based retrieval**, ensuring that all answers are derived from trusted medical sources.

---

## 📂 Contents

| File | Purpose |
|------|---------|
| `keywords_extract.py` | Identifies whether a user question requires retrieval and extracts search-friendly keywords for internal knowledge lookup. |
| `rag_agent.py`        | Core RAG (Retrieval-Augmented Generation) workflow. Judges if a question is answerable by the knowledge base, retrieves documents, and generates final response. |

---

## ❌ What This Agent **Does Not** Do

- ❌ No internet search (e.g., Google/Bing, crawl-based lookups)
- ❌ No external API data sourcing (unless explicitly whitelisted and medically validated)
- ❌ No general-purpose LLM-based guessing

---

## ✅ Medical-Grade Answer Sources

All agents here rely on:

- Internal document parsing (e.g., clinical PDFs, guidelines)
- Private vector databases (e.g., Milvus or FAISS)
- Structured medical knowledge APIs

---

## 💡 Design Philosophy

To support **safe, explainable, and domain-controlled medical Q&A**, all responses are grounded in:

- Internal hospital knowledge bases  
- Expert-verified documents  
- Traceable document snippets used in RAG outputs  

---

Feel free to explore or extend these agents to suit different internal workflows, such as clinical triage, post-op tracking, or medical education.

