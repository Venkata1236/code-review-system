# 🔍 Code Review System

> AutoGen multi-agent code review — Coder + Reviewer iterate until APPROVED

![Python](https://img.shields.io/badge/Python-3.11-blue)
![AutoGen](https://img.shields.io/badge/AutoGen-Latest-purple)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)

---

## 📌 What Is This?

A multi-agent code review system built with AutoGen. A Coder agent writes and fixes code, a Reviewer agent reviews and gives feedback. They converse autonomously in a GroupChat until the Reviewer approves the code by saying "APPROVED".

---

## 🗺️ Simple Flow
```
User submits code
        ↓
  [Coder Agent] → writes/fixes code
        ↓
  [Reviewer Agent] → reviews, gives structured feedback
        ↓
  [Coder Agent] → fixes based on feedback
        ↓
  [Reviewer Agent] → approves or requests more changes
        ↓
  Conversation terminates when Reviewer says "APPROVED"
```

---

## 📁 Project Structure
```
code_review_system/
├── app.py
├── streamlit_app.py
├── core/
│   ├── __init__.py
│   ├── agents.py
│   ├── groupchat.py
│   └── runner.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **AssistantAgent** | LLM-powered agent with a system message defining role |
| **UserProxyAgent** | Initiates conversation, runs autonomously |
| **GroupChat** | Multiple agents conversing together |
| **GroupChatManager** | Orchestrates who speaks next |
| **is_termination_msg** | Stops conversation when APPROVED detected |
| **max_round** | Safety limit to prevent infinite loops |

---

## ⚙️ Local Setup
```bash
git clone https://github.com/venkata1236/code-review-system.git
cd code_review_system
pip install -r requirements.txt
```

Add `.env`:
```
OPENAI_API_KEY=your_key_here
```

Add `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_key_here"
```

Run:
```bash
python -m streamlit run streamlit_app.py
python app.py
```

---

## 📦 Tech Stack

- **AutoGen** — AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
- **OpenAI** — GPT-4o-mini
- **Streamlit** — Web UI
- **python-dotenv** — API key management

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)