def create_groupchat(coder, reviewer, max_rounds=10):
    from autogen import GroupChat
    return GroupChat(
        agents=[coder, reviewer],
        messages=[],
        max_round=max_rounds,
        speaker_selection_method="round_robin"
    )


def create_manager(groupchat, llm_config):
    from autogen import GroupChatManager
    return GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )