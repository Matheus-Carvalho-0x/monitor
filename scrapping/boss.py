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
            # adjust
            page.locator("button[@id='details-button']").click()
            page.locator("a[@id='proceed-link']").click()
        except Exception as _:
            page.locator("input[name='txtUser']").fill(USER_LOGIN1)
            page.locator("input[name='txtPassword']").fill(PASSWORD_LOGIN1)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("networkidle")

            # EXTRACT
            search_for_data = ['tEu', 'tGs', 'SrG', 'd/1', 'Degelo']
            search_for_env = []
            data_extracted = []

            # IFRAMES
            iframe_father = page.frame_locator("#body")
            iframe_child = iframe_father.frame_locator("#bodytab")

            search_box = iframe_child.locator("input.form-control")
            search_box.fill("cong")
            search_box.press("Enter")

            # pegar o nome da loja, ambientes e valores

            # DEBUG
            print('end')
            input('')

            # CLOSING ALL PROPERLY
            context.close()
            browser.close()

if __name__ == "__main__":
    run_automation()
