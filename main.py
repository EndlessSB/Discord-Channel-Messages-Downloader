import time
import requests
import os
from dotenv import load_dotenv
import colorama
from colorama import Fore
import pyfiglet
from termcolor import colored


# Load environment variables
load_dotenv()

# Set the console title
def set_console_title(title):
    if os.name == 'nt':  # Windows
        os.system(f'title {title}')
    else:
        print(f"\033]0;{title}\a", end='', flush=True)

# Function to print rainbow ASCII art text
def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    ascii_art = pyfiglet.figlet_format(text)
    for i, line in enumerate(ascii_art.splitlines()):
        print(colored(line, colors[i % len(colors)]))

# Clear the console
def clear_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Mac/Linux
        os.system('clear')

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
            print(f"{force.RED} Failed to fetch messages: {response.status_code} - {response.text}")
            break

        messages = response.json()
        if not messages:
            print(f"{force.RED} No Messages Found! [Please Check The provided informaton]")
            break  # Stop if there are no more messages

        for msg in messages:
            formatted_msg = f"[{msg['author']['username']}] {msg['content']}"
            print(f"{Fore.GREEN} Found New Message! {formatted_msg}")
            save_to_file(formatted_msg, channel_id)

        all_messages.extend(messages)
        last_message_id = messages[-1]["id"]  # Update last message ID for pagination
        remaining -= len(messages)  # Reduce the count

        time.sleep(1)  # Prevent rate limits

    print(f"Fetched {len(all_messages)} messages successfully.")

if __name__ == "__main__":
    token = os.getenv("token")
    clear_console()

    set_console_title("Endless - Discord Message Downloader")

    print_rainbow_text("Endless - Discord Message Downloader")
    
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

    clear_console()

    print_rainbow_text("Fetching Messages - Please Wait!")

    time.sleep(2)
    
    get_messages(token, channel_id, limit)
