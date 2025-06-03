# 🩺 LLM-Powered Medical Chat & Data Analysis Module

This folder contains the **core conversational interfaces** for doctors and researchers, enabling both medical Q&A and automatic data analysis. It is part of the intelligent backend for a post-operative monitoring system.

---

## 🧑‍⚕️ Use Cases for Doctors

### 1. Medical Q&A (`chat_base.py`)
Doctors can ask questions in natural language such as:

> “Is this discharge prescription appropriate?”  
> “What are the key precautions after TAVI surgery?”

The system responds instantly with LLM-powered answers, optionally using:
- Internal clinical knowledge base
- External web search (optional for future expansion)

---

### 2. Data Analysis on Patient Excel Files (`analysis_chat.py`)
Doctors can upload structured data (e.g., `.csv` or `.xlsx`) and ask:

> “What is the average hospital stay for hypertensive patients?”  
> “Draw a histogram of patient ages”  
> “Extract data for patients with postoperative fever”

The system automatically:
- Parses the data structure
- Generates and executes Python code (Pandas, Matplotlib, etc.)
- Returns results as text summaries, plots, or code (in real time)

🧠 Doctors no longer need to export Excel and analyze it manually.  
📉 This saves time and reduces the workload for medical statistics and reporting.

---

## 🛠 Technical Overview (for developers)

| File | Description |
|------|-------------|
| `chat.py` | Base chat logic using LangGraph + Ollama for medical Q&A |
| `analysis_chat.py` | File upload + AI-powered data understanding & visualization |
| `gen_rag_graph()` | Constructs the LLM workflow graph (RAG-enabled) |
| `ChatOllama` | Interface to LLMs like DeepSeek via local Ollama endpoint |
| `LangGraph` | Node-based workflow engine for streaming output control |

---

## ✅ Key Benefits

- 🩺 Doctor-centric design: No need for technical input, just ask questions
- 📊 Embedded data analysis: Automatic charts and summaries
- 🧩 Modular architecture: Easy integration into frontend or mobile apps
- 🔁 Fully asynchronous: Supports real-time streaming of thoughts, code, results

---

Feel free to expand this module with more specialized agents for triage, diagnostics, or post-discharge education. If needed, we can also provide API endpoints for Excel export or frontend chart rendering.
