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
def get_messages(token, channel_id, limit=10):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        for msg in messages:
            print(f"[{msg['author']['username']}] {msg['content']}")
            save_to_file(f"[{msg['author']['username']}] {msg['content']}", channel_id)
    else:
        print(f"Failed to fetch messages: {response.status_code} - {response.text}")

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
    if limit > 100:
        print("Discord API is currently limited to only letting us grab the last 100 messages. This may change in the future! Keep Posted on the github Repo!")
        exit(1)
    
    get_messages(token, channel_id, limit)
