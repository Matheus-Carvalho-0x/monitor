from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from time import sleep

# Settings
load_dotenv()

URL_LOGIN1 = os.getenv("SCRAPPING_TARGET_URL1")
USER_LOGIN1 = os.getenv("SCRAPPING_LOGIN1")
PASSWORD_LOGIN1 = os.getenv("SCRAPPING_PASSWORD1")

def run_automation():
    # PLAYWRIGHT SETTINGS
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

            # DATA EXTRACTED
            store_name = page.locator("div[id='DateTime'] > div.nopadding > b").inner_text()
            search_for_env = []
            search_for_data = ['tEu', 'tGs', 'SrG', 'd/1', 'Degelo']
            data_extracted = []

            # IFRAMES
            iframe_father = page.frame_locator("#body")
            iframe_child = iframe_father.frame_locator("#bodytab")

            # EXTRACT ALL CARDS
            env = iframe_child.locator("div.row div[class='col-xs-12 col-sm-12 col-md-4 col-lg-4 btn nopadding']").first
            env_txt = env.locator("tr.border-underline th:first-of-type").inner_text()
            # GET ONLY THE 'CONG' ONES
            # GET ALL THE NAMES
            # ACCESS EACH OF THEM AND EXTRACT THE DATA
            
            

        

            # DEBUG
            print('end')
            input('')

            # CLOSING ALL PROPERLY
            context.close()
            browser.close()


if __name__ == "__main__":
    run_automation()
