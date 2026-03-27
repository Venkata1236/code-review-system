"""
🤖 Agent Factory - Coder & Reviewer Definitions
=============================================
GPT-4o-mini configs + termination logic (APPROVED).
Secrets handling: Streamlit/CLI unified.
Pro prompts: Structured feedback + code blocks.
Future: Add UserProxy for human-in-loop.
v1.0 - Venkata's AI code review agents.
"""



import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    try:
        import streamlit as st
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def get_llm_config():
    return {
        "config_list": [
            {
                "model": "gpt-4o-mini",
                "api_key": get_api_key()
            }
        ],
        "temperature": 0.3,
        "cache_seed": None
    }


def create_coder_agent():
    from autogen import AssistantAgent
    return AssistantAgent(
        name="Coder",
        system_message="""You are an expert software engineer.
Your job is to write clean, efficient, well-commented code.

When given code to review or fix:
- Fix all bugs and issues mentioned by the reviewer
- Improve code quality and readability
- Add proper error handling where missing
- Add docstrings and comments
- Always return the COMPLETE updated code in a code block

Follow best practices and write production-ready code.
""",
        llm_config=get_llm_config()
    )


def create_reviewer_agent():
    from autogen import AssistantAgent
    return AssistantAgent(
        name="Reviewer",
        system_message="""You are a senior code reviewer with 15+ years of experience.
Review code thoroughly and provide structured feedback.

When reviewing:
1. Check for bugs and logical errors
2. Check for security vulnerabilities
3. Review readability and naming conventions
4. Check for proper error handling
5. Look for performance improvements

Your feedback format:
✅ STRENGTHS: [what is good]
❌ ISSUES: [specific problems]
💡 SUGGESTIONS: [improvements]

If code is high quality and all issues fixed, end with:
"The code looks great. APPROVED."

Only say APPROVED when truly satisfied with the code quality.
""",
        llm_config=get_llm_config(),
        is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper()
    )


def create_user_proxy():
    from autogen import UserProxyAgent
    return UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper(),
        code_execution_config=False
    )