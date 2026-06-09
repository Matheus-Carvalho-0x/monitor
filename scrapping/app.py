import os
from dotenv import load_dotenv
from bossModule import *
from data_manager import data_manager

# Settings
load_dotenv()

URL_LOGIN = os.getenv("SCRAPPING_TARGET_URL")
USER_LOGIN = os.getenv("SCRAPPING_LOGIN")
PASSWORD_LOGIN = os.getenv("SCRAPPING_PASSWORD")

# ===================================================
curr_store = BossStore()
failed_stores = []
# ===================================================
try:
    curr_store.setStoreName('Verdemar Prado')
    curr_store.loginFunction(URL_LOGIN, USER_LOGIN, PASSWORD_LOGIN)
    curr_store.extractData(('tEu', 'tGs', 'SrG', 'd/1', 'Degelo'))
    data_manager(curr_store.getData())
except Exception as e:
    print(e)
    failed_stores.append('VM Prado')
# ===================================================
