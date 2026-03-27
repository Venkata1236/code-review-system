"""
🚀 AutoGen Code Review System - Streamlit UI
===========================================
Multi-agent workflow: Coder ↔ Reviewer until APPROVED.
Features: Real-time chat, examples, metrics, session state.
v1.0 - Deploy-ready for Streamlit Cloud (2026).
Author: Venkata Reddy Bomnavaram (@Venkata1236)
"""



import streamlit as st
import os
from dotenv import load_dotenv
from core.runner import run_code_review, format_messages_for_display

load_dotenv()

st.set_page_config(
    page_title="Code Review System",
    page_icon="🔍",
    layout="centered"
)

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "approved" not in st.session_state:
    st.session_state.approved = False
if "done" not in st.session_state:
    st.session_state.done = False

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("🔍 Code Review System")
    st.markdown("---")
    st.markdown("### 🤖 Agents")
    st.markdown("🔵 **Coder Agent**")
    st.caption("Writes and fixes code based on feedback")
    st.markdown("🟠 **Reviewer Agent**")
    st.caption("Reviews code and gives structured feedback")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    max_rounds = st.slider("Max Review Rounds", 2, 10, 6)
    st.markdown("---")
    if st.button("🔄 New Review", use_container_width=True):
        st.session_state.messages = []
        st.session_state.approved = False
        st.session_state.done = False
        st.rerun()
    st.markdown("---")
    st.caption(
        "AutoGen multi-agent code review. "
        "Agents converse until code is APPROVED "
        "or max rounds reached."
    )

# ─────────────────────────────────────────
# MAIN — INPUT
# ─────────────────────────────────────────
if not st.session_state.done:

    st.title("🔍 Code Review System")
    st.markdown(
        "Paste your code — **Coder** and **Reviewer** agents "
        "will iterate until the code is approved."
    )
    st.markdown("---")

    code = st.text_area(
        "📝 Paste your code here",
        height=300,
        placeholder="""def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)"""
    )

    st.markdown("**💡 Try these examples:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Buggy Python function", use_container_width=True):
            st.session_state.example = """def divide(a, b):
    return a / b

def get_average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)"""
            st.rerun()
    with col2:
        if st.button("Missing error handling", use_container_width=True):
            st.session_state.example = """def read_file(filename):
    f = open(filename, 'r')
    content = f.read()
    return content

def parse_json(text):
    import json
    return json.loads(text)"""
            st.rerun()

    if "example" in st.session_state:
        code = st.session_state.pop("example")

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start = st.button(
            "🚀 Start Code Review",
            use_container_width=True,
            disabled=not code.strip()
        )

    if start and code.strip():
        st.markdown("---")
        st.markdown("### 🤖 Agents are reviewing your code...")
        st.warning(
            "⏳ Agents are having a conversation — please wait.\n\n"
            "🚫 Do NOT refresh this page."
        )
        with st.spinner("Reviewing..."):
            try:
                messages, approved = run_code_review(
                    code.strip(),
                    max_rounds=max_rounds
                )
                st.session_state.messages = format_messages_for_display(messages)
                st.session_state.approved = approved
                st.session_state.done = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ─────────────────────────────────────────
# MAIN — RESULTS
# ─────────────────────────────────────────
else:
    st.title("🔍 Code Review Complete")
    st.markdown("---")

    if st.session_state.approved:
        st.success("✅ Code has been APPROVED by the Reviewer!")
    else:
        st.warning("⚠️ Max rounds reached. Review the conversation below.")

    st.markdown("---")

    # Stats
    total = len(st.session_state.messages)
    coder_msgs = len([m for m in st.session_state.messages if m["name"] == "Coder"])
    reviewer_msgs = len([m for m in st.session_state.messages if m["name"] == "Reviewer"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Messages", total)
    with col2:
        st.metric("Coder Turns", coder_msgs)
    with col3:
        st.metric("Reviewer Turns", reviewer_msgs)

    st.markdown("---")
    st.subheader("💬 Conversation")

    for i, msg in enumerate(st.session_state.messages):
        if msg["name"] == "Coder":
            with st.chat_message("assistant", avatar="🔵"):
                st.caption("🔵 Coder Agent")
                st.markdown(msg["content"])
        elif msg["name"] == "Reviewer":
            with st.chat_message("assistant", avatar="🟠"):
                st.caption("🟠 Reviewer Agent")
                if msg["is_approved"]:
                    st.success(msg["content"])
                else:
                    st.markdown(msg["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.caption(f"👤 {msg['name']}")
                st.markdown(msg["content"])