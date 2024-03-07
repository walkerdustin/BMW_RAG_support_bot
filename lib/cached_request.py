import hashlib
import os
import requests
import random
import time
import logging


def delayed_requests_get_with_cache(url, use_cache=True):
    # Ensure logging is configured (e.g., basic configuration for console output)
    logging.basicConfig(level=logging.ERROR)

    # Calculate cache file path
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    cache_dir = "./data/cache"
    cache_path = os.path.join(cache_dir, f"{url_hash}.txt")

    # Check cache
    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as file:
                return file.read()
        except IOError as e:
            logging.error(f"Failed to read cache file: {e}")

    # Delay before making a new request
    wait_time = random.random() * 10
    time.sleep(wait_time)

    # Fetch data from URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        html_content = response.text

        # Ensure cache directory exists
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)

        # Cache the response
        try:
            # Open the file with newline='' to prevent Python from translating '\n' to os.linesep
            with open(cache_path, "w", encoding="utf-8", newline="") as file:
                file.write(html_content)
        except IOError as e:
            logging.error(f"Failed to write to cache file: {e}")

        return html_content
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None  # Or handle the failure differently


if __name__ == "__main__":
    url = "https://www.bimmerforums.com/forum/showthread.php?2484316-m20b25-swap-e21-323i-trans"
    html_content = delayed_requests_get_with_cache(url)
    print(html_content)
