import requests
import json
import string
from itertools import product
import random
import time
import os

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = os.environ.get("7366706613:AAHx8fkIiGabXMpSXGh1vQS1FFQ8UH97NuY")
TELEGRAM_CHAT_ID = os.environ.get("5022119245")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Error: Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    exit()

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.82',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148b Safari/604.1',
]

# **Critical Warning Regarding Free Proxies for Production:**
# It is essential to reiterate that **relying on free proxies for a production environment
# is highly discouraged and can lead to significant issues.** Free proxies are inherently:
# 1. **Unstable:** They frequently disconnect, change IPs, and become unavailable without notice.
# 2. **Slow:** Performance is often poor, leading to timeouts and delays in your application.
# 3. **Insecure:** Your data transmitted through free proxies might not be encrypted or could be intercepted.
# 4. **Blocked:** Many free proxies are already blacklisted by websites due to abuse.
# 5. **Unpredictable:** You have no control over their uptime or location.

# **Given the inherent limitations of free proxies for production, the most responsible
# approach is to guide you towards strategies that might offer slightly better free options
# (though still not ideal) and emphasize the necessity of paid solutions for reliability.**

# **Strategy 1: Self-Hosted Proxies (Potentially "Better" but Requires Technical Expertise):**
# Setting up your own proxies using services like VPS (Virtual Private Servers) or cloud instances
# can offer more control and potentially better performance than public free lists.
# This requires technical knowledge in server configuration and management.

# **Strategy 2: Free Proxy Aggregators with Health Checks (Slightly Better but Still Limited):**
# Some websites and tools attempt to aggregate free proxy lists and perform basic health checks
# to identify proxies that are currently online. However, their reliability is still far from guaranteed.
# You would need to find and integrate with such services (often involving web scraping or APIs).

# **Strategy 3: Community-Maintained Free Proxy Lists (Use with Caution and Constant Monitoring):**
# Some online communities maintain lists of free proxies that are reported to be working.
# However, these lists require constant monitoring and updates as proxies become unusable.

# **Example (Conceptual - You would need to implement the logic to fetch and verify):**
#
# def get_potentially_better_free_proxies():
#     proxies = []
#     # Implement logic to fetch from a reliable free proxy aggregator or community list
#     # Example: Scraping a specific website or using a (potentially unreliable) API
#     try:
#         # ... your scraping or API fetching code ...
#         # Example (very basic and likely to break):
#         response = requests.get("SOME_FREE_PROXY_AGGREGATOR_URL", timeout=10)
#         # ... parse the response to extract IPs and ports ...
#         # ... and format them as dictionaries ...
#         proxies = [{'http': '...', 'https': '...'}, ...]
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching potentially better free proxies: {e}")
#     return proxies
#
# proxies = get_potentially_better_free_proxies()
# print(f"Fetched {len(proxies)} potentially better free proxies.")

# **Directly Including a Small, Potentially "Less Bad" Free Proxy List (Still Not Recommended for Production):**
# The following list is a small, randomly selected sample and its reliability can change instantly.
# **Use with extreme caution and for testing and understanding the limitations ONLY.**
proxies = [
    {'http': 'http://167.71.228.170:80', 'https': 'https://167.71.228.170:80'},
    {'http': 'http://144.202.115.250:3128', 'https': 'https://144.202.115.250:3128'},
    {'http': 'http://198.251.84.112:80', 'https': 'https://198.251.84.112:80'},
    {'http': 'http://104.248.116.154:80', 'https': 'https://104.248.116.154:80'},
    {'http': 'http://45.76.179.168:80', 'https': 'https://45.76.179.168:80'},
]

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

def check_instagram_availability(username, max_retries=3):
    """
    Checks if an Instagram username is available with retry and proxy/user-agent rotation.

    Args:
        username (str): The Instagram username to check.
        max_retries (int): Maximum number of retries for a request.

    Returns:
        bool: True if the username is available, False otherwise, None on persistent error.
    """
    url = f"https://www.instagram.com/api/v1/users/check_username/?username={username}"
    headers = {'User-Agent': random.choice(user_agents)}
    proxy = random.choice(proxies) if proxies else None

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("available")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {username} (Proxy: {proxy}): {e}")
            time.sleep(random.uniform(5, 15))  # Increased delay on error
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1} failed to decode JSON for {username}: {e}")
            time.sleep(random.uniform(5, 15))
        except Exception as e:
            print(f"An unexpected error occurred for {username}: {e}")
            time.sleep(random.uniform(10, 30))

    print(f"Failed to check {username} after {max_retries} retries.")
    return None

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
            availability = check_instagram_availability(username)
            if availability is True:
                available_usernames.add(username)
                print(f"Found available username: {username} ({len(available_usernames)}/{count})")
                send_telegram_message(f"✨ Found available Instagram username: {username} ✨")
            elif availability is None:
                print(f"Skipping {username} due to persistent errors.")

            time.sleep(random.uniform(10, 30))  # Increased random delay between checks

    return list(available_usernames)

if __name__ == "__main__":
    num_usernames_to_find = 5  # Example: Find 5 available usernames
    found_usernames = generate_and_check_usernames(num_usernames_to_find)

    if found_usernames:
        print("\nFound the following unique, available four-letter Instagram usernames:")
        for username in found_usernames:
            print(username)
    else:
        print("\nCould not find any available four-letter Instagram usernames at this time.")