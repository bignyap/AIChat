"""
Database related operations
"""

import json
import random

def get_recent_messages():
    """
    Get recent messages
    """

    # Define the file name and learn instruction
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content":"You are interviewing the user for a job as retail assistant. Ask sort questions that are relevant to the junior assistant to you. Your name is Veronica. The user called Bignya. Keep your answers short below under words"
    }

    # Initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour"
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question"

    # Append instruction to message
    messages.append(learn_instruction)

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last 5 data
            if data:
                if len(data):
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)

    return messages


# Store messages
def store_messages(request_message, response_message):
    """
    Store the messages
    """

    # Define the filename
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to data
    user_message = {"role":"user", "content":request_message}
    assistant_message = {"role":"system", "content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as f:
        json.dump(messages, f)

# Reset message
def reset_messages():

    # Overwrite the current file
    open("stored_data.json", "w")
