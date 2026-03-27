from core.agents import create_coder_agent, create_reviewer_agent, create_user_proxy, get_llm_config
from core.groupchat import create_groupchat, create_manager


def run_code_review(code: str, max_rounds: int = 10):
    """
    Runs the full code review conversation.

    Returns:
        messages: list of all conversation messages
        approved: True if code was approved
    """
    print("\n🚀 Starting Code Review System...")
    print(f"   Max rounds: {max_rounds}")

    # --- Create agents ---
    coder = create_coder_agent()
    reviewer = create_reviewer_agent()
    user_proxy = create_user_proxy()

    # --- Create GroupChat ---
    groupchat = create_groupchat(coder, reviewer, max_rounds=max_rounds)
    manager = create_manager(groupchat, get_llm_config())

    # --- Build initial message ---
    initial_message = f"""Please review the following code and provide detailed feedback.
The Coder will fix any issues you find, and we'll iterate until the code is approved.

Code to Review:
```
{code}
```

Start by reviewing this code thoroughly.
"""

    # --- Start conversation ---
    print("\n💬 Starting conversation...\n")
    user_proxy.initiate_chat(
        manager,
        message=initial_message
    )

    # --- Extract results ---
    messages = groupchat.messages
    approved = any(
        "APPROVED" in msg.get("content", "").upper()
        for msg in messages
    )

    print(f"\n{'✅ Code APPROVED!' if approved else '⚠️ Max rounds reached.'}")
    return messages, approved


def format_messages_for_display(messages: list) -> list:
    """
    Formats GroupChat messages for display in Streamlit or CLI.
    Returns list of dicts with role, name, content.
    """
    formatted = []
    for msg in messages:
        if not msg.get("content"):
            continue

        name = msg.get("name", "Unknown")
        content = msg.get("content", "")
        role = msg.get("role", "assistant")

        formatted.append({
            "name": name,
            "content": content,
            "role": role,
            "is_approved": "APPROVED" in content.upper()
        })

    return formatted