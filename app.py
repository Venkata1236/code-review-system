"""
🔥 Code Review CLI - AutoGen Powered
===================================
Console version: Paste code → END → See full agent convo.
Handles loops, errors, .env keys gracefully.
Bonus: Infinite review mode for batch testing.
v1.0 - CLI companion to Streamlit app (Mar 2026).
"""



import os
import sys
from dotenv import load_dotenv
from core.runner import run_code_review, format_messages_for_display

load_dotenv()


def print_separator():
    print("\n" + "=" * 60 + "\n")


def print_welcome():
    print_separator()
    print("🔍  CODE REVIEW SYSTEM — CLI MODE")
    print("    Powered by AutoGen + OpenAI GPT-4o-mini")
    print_separator()
    print("How it works:")
    print("  1. Paste your code")
    print("  2. Coder agent reviews + fixes it")
    print("  3. Reviewer agent gives feedback")
    print("  4. They iterate until APPROVED")
    print_separator()


def get_code_input():
    print("📝 Paste your code below.")
    print("When done, type 'END' on a new line and press Enter.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def run_cli():
    print_welcome()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in .env")
        sys.exit(1)

    while True:
        code = get_code_input()

        if not code:
            print("⚠️ No code provided. Try again.\n")
            continue

        try:
            messages, approved = run_code_review(code, max_rounds=10)
            formatted = format_messages_for_display(messages)

            print_separator()
            print("📜 CONVERSATION HISTORY:")
            print_separator()

            for msg in formatted:
                icon = "🔵" if msg["name"] == "Coder" else "🟠"
                print(f"{icon} {msg['name']}:")
                print(msg["content"])
                print_separator()

            if approved:
                print("✅ Code has been APPROVED!")
            else:
                print("⚠️ Max rounds reached without approval.")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        again = input("\nReview another code? (yes/no): ").strip().lower()
        if again != "yes":
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    run_cli()