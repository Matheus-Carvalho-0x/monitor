from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from time import sleep


class BossStore:

    def __init__(self):
        # Driver config
        self.options = webdriver.ChromeOptions()
        self.options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(300)

        self.wait = WebDriverWait(self.driver, 10)
        self.env_names = []
        self.env_data = []
        self.formatted_data = {}

    def _resetIFramePosition(self, layers=3):
        """
        Docstring for _resetIFramePosition

        :param layers: Each line is a layer so you dont need to go from
        default_content all the way to iframe 'bodytab' by default it
        executes all the lines;

        Necessary in various moments where we need to reset the iframe to
        the default one so we can access some 'deep-nested' iframe;
        """
        match layers:
            case 3:
                self.driver.switch_to.default_content()
                self.wait.until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, "body")))
                self.wait.until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, "bodytab")))
            case 2:
                self.driver.switch_to.default_content()
                self.wait.until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, "body")))
            case 1:
                self.driver.switch_to.default_content()
        sleep(2)

    def _retrieveEnvNames(self):
        """
        Docstring for retrieveEnvNames

        Get all enviroments names (used after filtering the 'cong' in the menu)
        """
        names = self.wait.until(EC.visibility_of_any_elements_located(
            (By.XPATH, "//div[@id='devices']//th[@style='white-space:normal;']")))

        for i in names:
            self.env_names.append(i.text)

    def _formatData(self):
        """
        Docstring for formatData

        This method is responsible for formatting all the extracted data
        as a nested dict so later we can parse it into json type.
        """
        data = dict(zip(self.env_names, self.env_data))
        for x in data.keys():
            data[x] = dict(data[x])
        self.formatted_data[f'{self.store_name}'] = data

    def loginFunction(self, url, login, password):
        """
        Docstring for loginFunction

        After the driver being initiated we need to access URL and
        Log-in, also, built-in confirmation to access some pages;
        """
        self.driver.get(url)

        # Built-in confirmation that some pages need
        try:
            first_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[@id='details-button']")))
            first_button.click()
            second_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[@id='proceed-link']")))
            second_button.click()
        except Exception as _:
            pass

        input_login = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='txtUser']")))
        input_login.send_keys(login)
        input_password = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='txtPassword']")))
        input_password.send_keys(password)
        login_button = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='btn btn-primary form-control']")))
        login_button.click()

    def extractData(self, search_list, timer=None):
        """
        Docstring for extractData

        :param search_list: list of tags to be typed in the search bar;
        :param timer: this is an optional parameter, the number passed here is
        the number of the iteration that will be skipped in the env loop;
        """
        # By default we use fullscreen in order to work properly without bugs
        sleep(2)
        self.driver.fullscreen_window()
        self._resetIFramePosition()

        search_bar = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@class='form-control']")))
        search_bar.send_keys('cong')
        sleep(2)

        # Necessary to be here after the filter 'cong' before the loop start
        self._retrieveEnvNames()

        # ====!!! Filter specific to remove enviroments that are not supposed to be showing after 'cong'
        flag = False
        if 'IR 33 77 - UC Congelados' in self.env_names:
            self.env_names.remove('IR 33 77 - UC Congelados')
            flag = True

        # ======================= BEGINNING OF LOOP FOR EACH ENVIROMENT =======================
        for i in range(len(self.env_names) if not flag else len(self.env_names) + 1):
            if flag:
                if i == timer:
                    continue

            enviroment = self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//div[@class='col-xs-12 col-sm-12 col-md-4 col-lg-4 btn nopadding']")))
            enviroment[i].click()

            self._resetIFramePosition(2)

            # Open variable tab
            var_tab = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[@id='tab_2']")))
            var_tab.click()

            self._resetIFramePosition()

            # ======================= BEGINNING OF LOOP FOR EACH PARAMETER =======================
            try:
                temp = []
                for tag in search_list:
                    search_bar = self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//input[@id='txtFilter']")))
                    search_bar.send_keys(tag)
                    sleep(2)

                    if (tag == 'Degelo') or (tag == 'Defrost'):
                        wait = WebDriverWait(self.driver, 10)
                        try:
                            wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//span[@class='boss icon-led color-0']")))
                            defrost = 'OFF'
                        except Exception as _:
                            wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//span[@class='boss icon-led color-1']")))
                            defrost = 'ON'
                        except Exception as _:
                            defrost = "Data Not Found"
                        finally:
                            if defrost == 'ON':
                                defrost = True
                            elif defrost == 'OFF':
                                defrost = False
                            else:
                                defrost = '***'
                            temp.append((tag, defrost))
                            search_bar.clear()
                    else:
                        # Tag treatment so the final result gets more legible
                        evap = ['tEu', 'TpEvap']
                        suct = ['tGs', 'TpSuccao']
                        env_temp = ['SrG', 's_pr1', 'TpAmbiente']
                        def_temp = ['d/1', 'd/', 'Temp degelo']

                        if tag in evap:
                            tag = 'Evaporação'
                        elif tag in suct:
                            tag = 'Sucção'
                        elif tag in env_temp:
                            tag = 'Temp. Ambiente'
                        elif tag in def_temp:
                            tag = 'Temp. Degelo'

                        value = self.wait.until(EC.presence_of_element_located(
                            (By.XPATH, "//tbody[@id='LWCtDataName1']/tr/td/following-sibling::td/following-sibling::td")))

                        out = 0
                        while not value:
                            value = self.wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//tbody[@id='LWCtDataName1']/tr/td/following-sibling::td/following-sibling::td")))
                            out += 1
                            if out == 10:
                                break
                        value = value.text[:-3]
                        temp.append((tag, float(value)))
                        search_bar.clear()
                self.env_data.append(temp)
            except Exception as e:
                print(e)

            # ========================= print for test only =========================
            # print(temp)
            # =======================================================================
            # ======================= END OF LOOP FOR EACH PARAMETER =======================

            # close and back to the init
            self._resetIFramePosition(1)
            home = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='hidden-xs hidden-sm btn btn-lg nopadding novpadding']")))
            home.click()
            sleep(2)
            self.driver.fullscreen_window()
            self._resetIFramePosition()
            search_bar = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//input[@class='form-control']")))
            search_bar.send_keys('cong')
            sleep(2)
        # ======================= END OF LOOP FOR EACH ENVIROMENT =======================
        self._formatData()
        self.env_names = []
        self.env_data = []
        self.driver.close()

    def getData(self):
        return self.formatted_data

    def setStoreName(self, name):
        self.store_name = name
