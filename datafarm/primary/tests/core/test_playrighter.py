import requests

from primary.core import web

from playwright.sync_api import sync_playwright
import os


def load_chrome_extension(extension_path, user_data_dir):
    """
    Launches Chromium with a specified Chrome extension loaded.

    Args:
        extension_path (str): The path to the unpacked Chrome extension directory.
        user_data_dir (str): The path to a user data directory for the browser.
                              This is important for persistent contexts.
    """

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",  # Or "chromium"
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )

        page = browser_context.new_page()
        page.goto("https://www.bilibili.com/video/BV1L3411J7Yc/")  # Replace with your desired URL

        # Interact with the extension (example: get the background page)
        background_page = browser_context.background_pages[0] if browser_context.background_pages else None
        if background_page:
            print("Background page URL:", background_page.url)
            # You can interact with the background page here

        # Example: Interact with the page and check if the extension is working
        # (This depends on what your extension does)
        # Example: Check if the extension modifies the page content
        # if "some_text_from_extension" in page.content():
        #     print("Extension is working!")

        # Keep the browser open for a while (for demonstration purposes)
        page.wait_for_timeout(5000)

        browser_context.close()


def test_load_chrome_extension():
    # Replace with the actual path to your unpacked Chrome extension
    extension_path = "/path/to/your/extension"
    # Replace with a directory for the user data
    user_data_dir = "/tmp/test-user-data-dir"

    load_chrome_extension(extension_path, user_data_dir)

def test_yt_dlp_dowload_subtitle():
  content = requests.get("https://api.bilibili.tv/intl/gateway/web/v2/subtitle?s_locale=id_ID&platform=web&episode_id=12662281")
  print(content.text)