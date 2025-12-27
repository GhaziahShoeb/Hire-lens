import time
import random
import os
from playwright.sync_api import sync_playwright

def scrape_hire_lens(search_url):
    if not os.path.exists("raw_data"):
        os.makedirs("raw_data")

    with sync_playwright() as p:
        # 1. Launch & Stealth Setup
        browser = p.chromium.launch(headless=False)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        # Load the saved state.json
        context = browser.new_context(
            storage_state="state.json", 
            user_agent=user_agent,
            viewport={'width': 1280, 'height': 800}
        )
        
        page = context.new_page()
        # Hide the webdriver flag from LinkedIn's bot detection
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"Opening Hire-Lens search: {search_url}")
        page.goto(search_url)
        
        # 2. Wait and Handle Modals
        time.sleep(5) 
        try:
            # Press Escape to dismiss simple pop-ups
            page.keyboard.press("Escape")
            # Look for specific 'Dismiss' buttons
            dismiss_btn = page.locator("button[aria-label='Dismiss'], button.modal__dismiss")
            if dismiss_btn.is_visible():
                dismiss_btn.click()
                print("Modal dismissed.")
        except:
            pass

        # 3. Identify Job Cards
        # We use a list of common selectors for both logged-in and public views
        selectors = [
            ".job-card-list__title", 
            "h3.base-search-card__title", 
            ".job-card-container__link"
        ]
        
        active_selector = None
        for sel in selectors:
            if page.locator(sel).count() > 0:
                active_selector = sel
                break

        if not active_selector:
            print("Failed to find job cards. Saving 'debug_view.png' for inspection.")
            page.screenshot(path="debug_view.png")
            browser.close()
            return

        job_links = page.locator(active_selector).all()
        print(f"Found {len(job_links)} jobs. Starting scrape...")

        # 4. Extraction Loop
        for i, link in enumerate(job_links[:10]): # Start with 10 for testing
            try:
                link.scroll_into_view_if_needed()
                link.click()
                
                # Randomized sleep to mimic human reading behavior
                time.sleep(random.uniform(4, 7)) 
                
                # Extract Description: Try several common containers
                description_selectors = ["#job-details", ".jobs-description", ".description__text"]
                html_content = ""
                
                for desc_sel in description_selectors:
                    if page.locator(desc_sel).is_visible():
                        html_content = page.locator(desc_sel).inner_html()
                        break
                
                if html_content:
                    file_path = f"raw_data/job_{i+1}.html"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    print(f"Saved: {file_path}")
                else:
                    print(f"Job {i+1} clicked, but description was empty.")
                    
            except Exception as e:
                print(f"Skipping job {i+1} due to error: {e}")

        print("\nPhase 1 Complete! Check your 'raw_data' folder.")
        browser.close()

if __name__ == "__main__":
    # You can change the 'keywords' and 'location' in the URL below
    url = "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&location=United%20States"
    scrape_hire_lens(url)