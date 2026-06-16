from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# ===== Settings ======
load_dotenv()

URL_LOGIN1 = os.getenv("SCRAPPING_TARGET_URL1")
USER_LOGIN1 = os.getenv("SCRAPPING_LOGIN1")
PASSWORD_LOGIN1 = os.getenv("SCRAPPING_PASSWORD1")

def run_automation():
    # ====== Playwright Settings ======
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto(URL_LOGIN1)

        # ====== Login ======
        try:
            # adjust
            page.locator("button[@id='details-button']").click()
            page.locator("a[@id='proceed-link']").click()
        except Exception as _:
            page.locator("input[name='txtUser']").fill(USER_LOGIN1)
            page.locator("input[name='txtPassword']").fill(PASSWORD_LOGIN1)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("networkidle")

            # ====== Data Extracted ======
            store_name = page.locator("div[id='DateTime'] > div.nopadding > b").inner_text()
            env_names_list = []
            search_for_data = ['tEu', 'tGs', 'SrG', 'd/1']
            data_extracted = []

            # ====== Iframes ======
            iframe_father = page.frame_locator("#body")
            iframe_child = iframe_father.frame_locator("#bodytab")

            # ====== Env List ======
            # Here I get all the envs, and while i filter the 'cong' ones i save the env name,
            # extract all the env data.
            env_list = iframe_child.locator("div.row div[class='col-xs-12 col-sm-12 col-md-4 col-lg-4 btn nopadding']").all()
            for e in env_list:
                env_txt = e.locator("tr.border-underline th:first-of-type").inner_text()
                # Improve the if-else
                if 'Congelados' in env_txt:
                    env_names_list.append(env_txt)
                
                    e.click()
                    page.wait_for_load_state("networkidle")
                    iframe_father.locator("li[data-original-title='Variáveis'] > a").click()
                    page.wait_for_load_state("networkidle")
                    
                    env_data = []
                    for i in search_for_data:
                        search_bar = iframe_child.locator("input[id='txtFilter']")
                        search_bar.fill(f'{i}')
                        search_bar.press('Enter')

                        search = iframe_child.locator(f"tbody > tr > td:has-text('{i}')").last
                        search = search.locator("xpath=following-sibling::td").last
                        search = search.inner_text()

                        # clean the data (degelo pending)
                        if not i == 'Degelo':
                            search = float(search[:-3])
                        env_data.append((i, search))

                        search_bar.clear()

                    # ====== Save Env Data ======
                    data_extracted.append((env_txt, env_data))

                    page.locator("div[class='hidden-xs hidden-sm btn btn-lg nopadding novpadding']").click()

            print((store_name, data_extracted))

            # CLOSING ALL PROPERLY
            context.close()
            browser.close()


if __name__ == "__main__":
    run_automation()
