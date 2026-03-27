"""
⚙️ Core Orchestrator - Runs Agent Conversations
=============================================
Bridges agents/groupchat → full review cycle.
Key: initiate_chat() + APPROVED detection + formatting.
Scalable to more agents/LLMs.
Production: Error-wrapped for Streamlit/CLI.
v1.0 - Heart of code-review-system (2026).
"""



from core.agents import (
    create_coder_agent,
    create_reviewer_agent,
    create_user_proxy,
    get_llm_config
)
from core.groupchat import create_groupchat, create_manager


def run_code_review(code: str, max_rounds: int = 10):
    """
    Runs the full code review conversation.
    Returns messages list and approved boolean.
    """
    print("\n🚀 Starting Code Review System...")

    # Create agents
    coder = create_coder_agent()
    reviewer = create_reviewer_agent()
    user_proxy = create_user_proxy()

    # Create GroupChat
    groupchat = create_groupchat(coder, reviewer, max_rounds=max_rounds)
    manager = create_manager(groupchat, get_llm_config())

    # Initial message
    initial_message = f"""Please review the following code carefully.

Code to Review:
```python
{code}
```

Reviewer — please start by reviewing this code thoroughly.
Coder — fix any issues the reviewer identifies.
Continue until the Reviewer says APPROVED.
"""

    # Start conversation
    user_proxy.initiate_chat(
        manager,
        message=initial_message,
        clear_history=True
    )

    # Extract results
    messages = groupchat.messages
    approved = any(
        "APPROVED" in msg.get("content", "").upper()
        for msg in messages
    )

    print(f"\n{'✅ APPROVED!' if approved else '⚠️ Max rounds reached.'}")
    return messages, approved


def format_messages_for_display(messages: list) -> list:
    formatted = []
    for msg in messages:
        content = msg.get("content", "")
        if not content:
            continue
        name = msg.get("name", "Unknown")
        formatted.append({
            "name": name,
            "content": content,
            "role": msg.get("role", "assistant"),
            "is_approved": "APPROVED" in content.upper()
        })
    return formatted