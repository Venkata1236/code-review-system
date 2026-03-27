from autogen import GroupChat, GroupChatManager


def create_groupchat(coder, reviewer, max_rounds=10):
    """
    Creates GroupChat with Coder and Reviewer agents.
    max_rounds — max conversation turns before forced stop.
    """
    groupchat = GroupChat(
        agents=[coder, reviewer],
        messages=[],
        max_round=max_rounds,
        speaker_selection_method="round_robin"  # alternates Coder → Reviewer → Coder
    )
    return groupchat


def create_manager(groupchat, llm_config):
    """
    GroupChatManager orchestrates who speaks next.
    """
    return GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )