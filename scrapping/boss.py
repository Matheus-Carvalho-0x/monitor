from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# Settings
load_dotenv()

URL_LOGIN1 = os.getenv("SCRAPPING_TARGET_URL1")
USER_LOGIN1 = os.getenv("SCRAPPING_LOGIN1")
PASSWORD_LOGIN1 = os.getenv("SCRAPPING_PASSWORD1")

def run_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto(URL_LOGIN1)

        # --- LOGIN ---
        try:
            page.locator("button[@id='details-button']").click()
            page.locator("a[@id='proceed-link']").click()
        except Exception as _:
            page.locator("input[name='txtUser']").fill(USER_LOGIN1)
            page.locator("input[name='txtPassword']").fill(PASSWORD_LOGIN1)
            page.get_by_role("button", name="Login").click()
            input('')
            context.close()
            browser.close()

if __name__ == "__main__":
    run_automation()
