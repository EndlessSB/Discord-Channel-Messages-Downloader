import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Save the messages to the file
def save_to_file(message, filename):
    """Save the provided message to a file called dataset.txt."""
    with open(f"{filename}.txt", "a", encoding="utf-8") as file:  
        file.write(message + "\n")  # Ensures each message is on a new line [some may be multiline so look for the username]

# The actual method to get the messages
def get_messages(token, channel_id, total_messages=10):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    all_messages = []
    last_message_id = None  # Store last message ID for pagination
    remaining = total_messages  # Number of messages still needed

    while remaining > 0:
        limit = min(100, remaining)  # Discord allows max 100 per request
        params = {"limit": limit}
        if last_message_id:
            params["before"] = last_message_id  # Get older messages

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch messages: {response.status_code} - {response.text}")
            break

        messages = response.json()
        if not messages:
            break  # Stop if there are no more messages

        for msg in messages:
            formatted_msg = f"[{msg['author']['username']}] {msg['content']}"
            print(formatted_msg)
            save_to_file(formatted_msg, channel_id)

        all_messages.extend(messages)
        last_message_id = messages[-1]["id"]  # Update last message ID for pagination
        remaining -= len(messages)  # Reduce the count

        time.sleep(1)  # Prevent rate limits

    print(f"Fetched {len(all_messages)} messages successfully.")

if __name__ == "__main__":
    token = os.getenv("token")
    # Ensures there is a token set
    if not token:
        print("Error: Token not found. Make sure to set it in the .env file.")
        exit(1)
    # Ensures the token is actually a token and not just the deault preset
    if token == "put your discord token here [not a bot token]":
        print("Please Replace the token to your actual tokeen :)")
        exit(1)

    # server_id = input("Enter Server ID: ")  - Not currently used and not needed here incase api changes
    channel_id = input("Enter Channel ID: ")
    limit = input("Enter number of messages to fetch (default 10): ")
    limit = int(limit) if limit.isdigit() else 10
    
    get_messages(token, channel_id, limit)
