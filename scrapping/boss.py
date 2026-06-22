from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# ===== Settings ======
load_dotenv()

URL_LOGIN1 = os.getenv("SCRAPPING_TARGET_URL1")
URL_LOGIN2 = os.getenv("SCRAPPING_TARGET_URL2")
URL_LOGIN3 = os.getenv("SCRAPPING_TARGET_URL3")
URL_LOGIN4 = os.getenv("SCRAPPING_TARGET_URL4")
URL_LOGIN5 = os.getenv("SCRAPPING_TARGET_URL5")
URL_LOGIN6 = os.getenv("SCRAPPING_TARGET_URL6")

USER_LOGIN1 = os.getenv("SCRAPPING_LOGIN1")
PASSWORD_LOGIN1 = os.getenv("SCRAPPING_PASSWORD1")
USER_LOGIN2 = os.getenv("SCRAPPING_LOGIN2")
PASSWORD_LOGIN2 = os.getenv("SCRAPPING_PASSWORD2")
USER_LOGIN3 = os.getenv("SCRAPPING_LOGIN3")
PASSWORD_LOGIN3 = os.getenv("SCRAPPING_PASSWORD3")

SEARCH_LIST1 = os.getenv("SEARCH_LIST1", "").split(",")
SEARCH_LIST2 = os.getenv("SEARCH_LIST2", "").split(",")
SEARCH_LIST3 = os.getenv("SEARCH_LIST3", "").split(",")

login_info = [
    (URL_LOGIN1, USER_LOGIN1, PASSWORD_LOGIN1, SEARCH_LIST1),
    (URL_LOGIN2, USER_LOGIN1, PASSWORD_LOGIN1, SEARCH_LIST1),
    (URL_LOGIN3, USER_LOGIN3, PASSWORD_LOGIN3, SEARCH_LIST1),
    (URL_LOGIN4, USER_LOGIN1, PASSWORD_LOGIN1, SEARCH_LIST2),
    (URL_LOGIN5, USER_LOGIN3, PASSWORD_LOGIN3, SEARCH_LIST3),
    (URL_LOGIN6, USER_LOGIN3, PASSWORD_LOGIN3, SEARCH_LIST3),
]

# ===== SETUP IF-ELSE =====
cong_name_list = ['Congelados', 'Cong', 'congelados', 'cong']
def_name_list = ['Degelo', 'degelo', 'Defrost', 'defrost']
exception_list = ['IR 33 77 - UC Congelados', 'CPCO 8 - Eco2Pack L3 - Master - Exp Congelados']

def run_automation(url, login, password, search_list):
    # ====== Playwright Settings ======
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto(url)

        # ====== Login ======
        try:
            page.locator("button[id='details-button']").click()
            page.locator("a[id='proceed-link']").click()
        except Exception as _:
            page.locator("input[name='txtUser']").fill(login)
            page.locator("input[name='txtPassword']").fill(password)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("networkidle")

            # ====== Data Extracted ======
            store_name = page.locator("div[id='DateTime'] > div.nopadding > b").inner_text()
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
                    cong_flag = False
                    for t in cong_name_list:
                        if env_txt not in exception_list:
                            if t in env_txt:
                                cong_flag = True
                    if cong_flag:
                        e.click()
                        page.wait_for_load_state("networkidle")
                        iframe_father.locator("li[data-original-title='Variáveis'] > a").click()
                        page.wait_for_load_state("networkidle")
                        
                        env_data = []
                        for i in search_list:
                            search_bar = iframe_child.locator("input[id='txtFilter']")
                            search_bar.fill(f'{i}')
                            search_bar.press('Enter')

                            if i in def_name_list:
                                # Exception VM Belvedere
                                if store_name in ['12041 Verdemar Belvedere', 'Verdemar Padaria Cataguases', 
                                                  '12016 Superluna Palmeiras', '12025 Superluna Cachoeira']:
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
                                page.wait_for_load_state("networkidle")
                                success = True
                            else:
                                if store_name in ['12016 Superluna Palmeiras', '12025 Superluna Cachoeira']:
                                    # SL Palmeiras & Cachoeira Exception
                                    search = iframe_child.locator(f"tbody > tr:first-of-type > td:has-text('{i}')").last
                                    search = search.locator("xpath=following-sibling::td").last
                                    search = search.inner_text()
                                else:
                                    search = iframe_child.locator(f"tbody > tr > td:has-text('{i}')").last
                                    search = search.locator("xpath=following-sibling::td").last
                                    search = search.inner_text()
                                try:
                                    search = float(search[:-3])
                                    env_data.append((i, search))

                                    search_bar.clear()

                                except Exception as exc:
                                    if '*' in search:
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
    for url, user, password, search_list in login_info:
        run_automation(url, user, password, search_list)
