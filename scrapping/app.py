import os
from dotenv import load_dotenv
from bossModule import *
from data_manager import data_manager

# Settings
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

# ===================================================
failed_stores = []
# ===================================================
try:
    curr_store = BossStore()
    curr_store.setStoreName('Verdemar Prado')
    curr_store.loginFunction(URL_LOGIN1, USER_LOGIN1, PASSWORD_LOGIN1)
    curr_store.extractData(('tEu', 'tGs', 'SrG', 'd/1', 'Degelo'))
    print(curr_store.getData())
    print("======================================")
    data_manager(curr_store.getData())
except Exception as e:
    print(e)
    failed_stores.append('VM Prado')
# ===================================================
try:
    curr_store = BossStore()
    curr_store.setStoreName('Verdemar Cidade Nova')
    curr_store.loginFunction(URL_LOGIN2, USER_LOGIN2, PASSWORD_LOGIN2)
    curr_store.extractData(('tEu', 'tGs', 'SrG', 'd/1', 'Degelo'))
    print(curr_store.getData())
    print("======================================")
    data_manager(curr_store.getData())
except Exception as e:
    print(e)
    failed_stores.append('VM Cidade Nova')
# ===================================================
try:
    curr_store = BossStore()
    curr_store.setStoreName('Verdemar Belvedere')
    curr_store.loginFunction(URL_LOGIN3, USER_LOGIN3, PASSWORD_LOGIN3)
    curr_store.extractData(('tEu', 'tGs', 'SrG', 'd/1', 'Degelo'))
    print(curr_store.getData())
    print("======================================")
    data_manager(curr_store.getData())
except Exception as e:
    print(e)
    failed_stores.append('VM Belvedere')
# ===================================================
print(failed_stores)
