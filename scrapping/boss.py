from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# ===== Settings ======
load_dotenv()

URL_LOGIN1 = os.getenv("SCRAPPING_TARGET_URL1")
USER_LOGIN1 = os.getenv("SCRAPPING_LOGIN1")
PASSWORD_LOGIN1 = os.getenv("SCRAPPING_PASSWORD1")
URL_LOGIN2 = os.getenv("SCRAPPING_TARGET_URL2")
USER_LOGIN2 = os.getenv("SCRAPPING_LOGIN2")
PASSWORD_LOGIN2 = os.getenv("SCRAPPING_PASSWORD2")
URL_LOGIN3 = os.getenv("SCRAPPING_TARGET_URL3")
USER_LOGIN3 = os.getenv("SCRAPPING_LOGIN3")
PASSWORD_LOGIN3 = os.getenv("SCRAPPING_PASSWORD3")

login_info = [
    (URL_LOGIN1, USER_LOGIN1, PASSWORD_LOGIN1),
    (URL_LOGIN2, USER_LOGIN2, PASSWORD_LOGIN2),
    (URL_LOGIN3, USER_LOGIN3, PASSWORD_LOGIN3),
]

def run_automation(url, login, password):
    # ====== Playwright Settings ======
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto(url)

        # ====== Login ======
        try:
            # adjust
            page.locator("button[@id='details-button']").click()
            page.locator("a[@id='proceed-link']").click()
        except Exception as _:
            page.locator("input[name='txtUser']").fill(login)
            page.locator("input[name='txtPassword']").fill(password)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("networkidle")

            # ====== Data Extracted ======
            store_name = page.locator("div[id='DateTime'] > div.nopadding > b").inner_text()
            search_for_data = ['tEu', 'tGs', 'SrG', 'd/1', 'Degelo']
            data_extracted = []

            # ====== Iframes ======
            iframe_father = page.frame_locator("#body")
            iframe_child = iframe_father.frame_locator("#bodytab")

            # ====== Env List ======
            # Here I get all the envs, and while i filter the 'cong' ones i save the env name,
            # extract all the env data.
            env_list = iframe_child.locator("div.row div[class='col-xs-12 col-sm-12 col-md-4 col-lg-4 btn nopadding']").all()
            for e in env_list:
                success = False
                err = 0
                while not success:
                    env_txt = e.locator("tr.border-underline th:first-of-type").inner_text()
                    if ('Congelados' in env_txt) or ('Cong' in env_txt):
                        e.click()
                        page.wait_for_load_state("networkidle")
                        iframe_father.locator("li[data-original-title='Variáveis'] > a").click()
                        page.wait_for_load_state("networkidle")
                        
                        env_data = []
                        for i in search_for_data:
                            search_bar = iframe_child.locator("input[id='txtFilter']")
                            search_bar.fill(f'{i}')
                            search_bar.press('Enter')

                            if i == 'Degelo':
                                # Exception VM Belvedere
                                if 'Belvedere' in store_name:
                                    search = iframe_child.locator(f"tbody > tr:first-of-type > td:has-text('{i}')").last
                                else:
                                    search = iframe_child.locator(f"tbody > tr:last-of-type > td:has-text('{i}')").last

                                search = search.locator("xpath=following-sibling::td").last   
                                search = search.locator("span[class^='boss icon-led color-']")
                                search = search.get_attribute("class")
                                if int(search[-1]):
                                    search = True
                                else:
                                    search = False

                                # This is here because the 'Degelo' will always be the last info extracted
                                # ====== Save Env Data ======
                                env_data.append((i, search))
                                data_extracted.append((env_txt, env_data))

                                page.locator("div[class='hidden-xs hidden-sm btn btn-lg nopadding novpadding']").click()
                                success = True
                            else:
                                search = iframe_child.locator(f"tbody > tr > td:has-text('{i}')").last
                                search = search.locator("xpath=following-sibling::td").last
                                search = search.inner_text()

                                try:
                                    search = float(search[:-3])
                                    env_data.append((i, search))

                                    search_bar.clear()

                                except Exception as exc:
                                    if '***' in search:
                                        if err < 10:
                                            err += 1
                                            page.locator("div[class='hidden-xs hidden-sm btn btn-lg nopadding novpadding']").click()
                                        else:
                                            print("CRITICAL ERROR! INFINITE LOOP!")
                                            context.close()
                                            browser.close()
                                    else:
                                        print(exc)
                                        context.close()
                                        browser.close()
                    else:     
                        success = True

            print((store_name, data_extracted))

            # CLOSING ALL PROPERLY
            context.close()
            browser.close()


if __name__ == "__main__":
    for url, user, password in login_info:
        run_automation(url, user, password)
