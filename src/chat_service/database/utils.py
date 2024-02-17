"""
Some database utilites functions
"""

import random


def get_random_system_prompt():
    """
    Randomly choose the prompt from a preselected prompts
    """
    learn_instruction = {
        "role": "system",
        "content":"You are interviewing the user for a job as retail assistant. Ask sort questions that are relevant to the junior assistant to you. Your name is Veronica. The user called Bignya. Keep your answers short below under words"
    }
    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour"
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question"

    return learn_instruction