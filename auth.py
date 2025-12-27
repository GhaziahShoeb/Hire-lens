import time
from playwright.sync_api import sync_playwright

def capture_session():
    with sync_playwright() as p:
        # Launch browser - headless=False is required to log in manually
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Action: Opening LinkedIn. Please log in manually...")
        page.goto("https://www.linkedin.com/login")

        print("---")
        print("IMPORTANT: After logging in, click 2-3 jobs on your feed.")
        print("This ensures 'Deep Cookies' are saved.")
        print("---")
        
        input("Press ENTER here ONLY after you are fully logged in and see your feed: ")

        # Save the session state to your laptop
        context.storage_state(path="state.json")
        print("Success: 'state.json' saved. You can now close the browser.")
        browser.close()

if __name__ == "__main__":
    capture_session()