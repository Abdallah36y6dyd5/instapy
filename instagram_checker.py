import requests
import json
import string
from itertools import product
import random

# Replace with your Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = "7366706613:AAHx8fkIiGabXMpSXGh1vQS1FFQ8UH97NuY"
TELEGRAM_CHAT_ID = "5022119245"

def send_telegram_message(message):
    """
    Sends a message to a Telegram bot.

    Args:
        message (str): The message to send.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if not data.get("ok"):
            print(f"Failed to send Telegram message: {data.get('description')}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")

def check_instagram_availability(username):
    """
    Checks if an Instagram username is available.

    Args:
        username (str): The Instagram username to check.

    Returns:
        bool: True if the username is available, False otherwise.
    """
    url = f"https://www.instagram.com/api/v1/users/check_username/?username={username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("available")
    except requests.exceptions.RequestException as e:
        print(f"Error checking username '{username}': {e}")
        return False

def generate_and_check_usernames(count=1):
    """
    Generates and checks the availability of four-letter Instagram usernames and sends available ones to Telegram.

    Args:
        count (int): The number of unique available usernames to find.

    Returns:
        list: A list of unique, available four-letter Instagram usernames.
    """
    available_usernames = set()
    alphabet = string.ascii_lowercase + string.digits  # Consider lowercase and digits

    print("Searching for available four-letter Instagram usernames...")

    while len(available_usernames) < count:
        # Generate a random four-character username
        random_chars = random.choices(alphabet, k=4)
        username = "".join(random_chars)

        if username not in available_usernames:
            if check_instagram_availability(username):
                available_usernames.add(username)
                print(f"Found available username: {username} ({len(available_usernames)}/{count})")
                send_telegram_message(f"✨ Found available Instagram username: {username} ✨")

    return list(available_usernames)

if __name__ == "__main__":
    num_usernames_to_find = 1
    found_usernames = generate_and_check_usernames(num_usernames_to_find)

    if found_usernames:
        print("\nFound the following unique, available four-letter Instagram usernames:")
        for username in found_usernames:
            print(username)
    else:
        print("\nCould not find any available four-letter Instagram usernames at this time.")