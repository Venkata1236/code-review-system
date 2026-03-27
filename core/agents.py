import os
from autogen import AssistantAgent, UserProxyAgent
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
        "temperature": 0.3
    }


def create_coder_agent():
    """
    Coder Agent — writes and fixes code based on feedback.
    """
    return AssistantAgent(
        name="Coder",
        system_message="""You are an expert software engineer and coder.
Your job is to write clean, efficient, well-commented code.

When given code to review:
- Fix any bugs or issues mentioned by the reviewer
- Improve code quality, readability, and efficiency
- Add proper error handling where missing
- Add docstrings and comments where needed
- Always return the COMPLETE updated code

When writing new code:
- Follow best practices for the language
- Write clean, readable, production-ready code
- Include error handling and edge cases
- Add helpful comments and docstrings

Always wrap your code in proper markdown code blocks.
""",
        llm_config=get_llm_config(),
        is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper()
    )


def create_reviewer_agent():
    """
    Reviewer Agent — reviews code and gives structured feedback.
    """
    return AssistantAgent(
        name="Reviewer",
        system_message="""You are a senior code reviewer with 15+ years of experience.
Your job is to review code thoroughly and provide structured feedback.

When reviewing code:
1. Check for bugs and logical errors
2. Check for security vulnerabilities
3. Review code readability and naming conventions
4. Check for proper error handling
5. Look for performance improvements
6. Verify best practices are followed

Your feedback format:
✅ STRENGTHS: [what is good]
❌ ISSUES: [specific problems found]
💡 SUGGESTIONS: [concrete improvements]

If the code is good quality and all issues are fixed:
- Say "APPROVED" clearly in your response
- Example: "The code looks great. APPROVED."

If issues remain:
- List them clearly
- Do NOT say APPROVED until all issues are resolved

Be constructive but thorough.
""",
        llm_config=get_llm_config(),
        is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper()
    )


def create_user_proxy():
    """
    UserProxy — initiates conversation, runs autonomously.
    """
    return UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper(),
        code_execution_config=False
    )