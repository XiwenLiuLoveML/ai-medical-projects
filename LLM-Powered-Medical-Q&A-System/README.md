# 🩺 LLM-Powered Medical Q&A System (Demo Project)

This project demonstrates the core architecture of a **Large Language Model (LLM)** powered **medical intelligent Q&A backend**, built with **FastAPI** and designed for scalable deployment.

> ✅ This repository is intended for **showcasing structure and capability only**.  
> 🔒 Core logic and proprietary components are stored in a private repo [`ai-private-core`] and available upon request.

---

## 🚀 What This Project Shows

- 🌐 **REST API for Medical Q&A**: powered by LLMs like ChatGPT, GLM, etc.
- 🔁 **Streaming Response (SSE)**: for real-time chatbot interactions
- 🧠 **Session Management**: multi-turn conversations supported
- 🔧 **Production-style FastAPI backend**: cleanly separated modules for middleware, routers, and logging
- 🏥 **Healthcare Application Scenario**: designed for clinical decision support and patient education
- 🛡️ **System Management Modules**: emulating a real-world multi-role backend system for hospitals or research labs

---

## 📂 Project Structure

```
LLM-Powered-Medical-Q&A-System/
├── README.md # Project overview and documentation
├── requirements.txt # Python dependencies for the system
├── main.py # FastAPI application entry point
├── core/
│ └── registrar.py # Middleware, routers, and logging registration
├── config/
│ └── settings.py # Global environment configuration (simplified public version)
├── dataclass/
│ └── common.py # Shared data objects (e.g., IP info, token result, request context)
├── app/
│ ├── router.py # Root route registry
│ ├── schema/
│ │ ├── token.py # Token response model schema (pydantic)
│ │ └── login_log.py # Login log schema definitions
│ ├── service/
│ │ └── auth_service.py # Auth logic (token generation, refresh, login logs)
│ └── admin/
│ ├── api/
│ │ ├── llm.py # Chat, stream, session APIs for LLM interaction
│ │ ├── knowledge.py # Knowledge base APIs (public version)
│ │ ├── auth.py # Authentication routes (simplified)
│ │ ├── login_log.py # User login activity tracking
│ │ ├── opera_log.py # Operation history logging (e.g., updates, deletions)
│ │ ├── sys_config.py # System-wide configs like user protocols and site info
│ │ ├── sys_dept.py # Department (e.g. medical units) management
│ │ ├── sys_dict_data.py # Dictionary entries (e.g. disease stages, genders)
│ │ ├── sys_dict_type.py # Dictionary categories (grouping dictionary items)
│ │ ├── sys_menu.py # Sidebar/menu configuration
│ │ ├── sys_role.py # Role management and permissions
│ │ └── sys_user.py # User profile, password, role, and permission APIs
```

---

## 👩‍⚕️ Sample Use Case 

> Imagine a hospital integrating an internal AI assistant to answer staff or patient questions such as:
> - “What are the side effects of metformin?”
> - “Can I take ibuprofen after surgery?”
> - “Summarize this lab report.”

This project is a simplified backend simulating that assistant.

---

## 📌 Keywords

`LLM`, `Healthcare AI`, `Chatbot`, `FastAPI`, `Streaming`, `SSE`, `Medical NLP`, `Python Backend`, `Scalable Architecture`, `Singapore AI Talent`

---

## 🙋 About the Author

This project was created by an AI engineer and strategist with hands-on experience in deploying LLM-powered systems in real-world healthcare and industrial settings.

For business collaboration or detailed technical review, please feel free to [connect on LinkedIn](https://www.linkedin.com/in/liuxiwen/) or [request access to `ai-private-core`].
