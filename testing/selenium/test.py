import os
import re
import requests
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

CASHNEST = "http://127.0.0.1:5000"

#GECKO = 
DELAY = 7 # time in seconds to delay actions
DATADIR = os.path.join(os.getcwd(), 'data')

class test:
    def __init__(self):
        self.options = Options()
        self.options.add_argument(f"user-data-dir={DATADIR}")
        self.driver = webdriver.Chrome(options=self.options)

        try:
            self.driver.get(CASHNEST)
        except Exception as e:
            print(f"Cashnest Not Running ({CASHNEST})")

    def login(self, driver):
        USERNAME = os.urandom(16).hex()
        PASSWORD = os.urandom(16).hex()

        CSRF = f"{CASHNEST}/login"
        LOGIN = f"{CASHNEST}/auth/login"
        REGISTER = f"{CASHNEST}/auth/register"

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Priority': 'u=0, i',
        })

        login = self.session.get(CSRF)
        
        pattern = r'<input id="csrf_token" name="csrf_token" type="hidden" value="([^"]+)">'
        match = re.search(pattern, login.text)
        if not match:
            return -1
        csrf = match.group(1)

        user = {"csrf_token": csrf, "username": USERNAME, "password": PASSWORD}
        register = self.session.post(REGISTER, data=user)
        
        cookies = self.session.post(LOGIN, data=user).cookies
        if not cookies:
            return -1
        
        for cookie in cookies:
            selenium_cookie = {'name': cookie.name, 'value': cookie.value, 'path': cookie.path, 'domain': cookie.domain, 'secure': cookie.secure, 'expires': cookie.expires}
            self.driver.add_cookie(selenium_cookie)
        
        return USERNAME, PASSWORD

    def refresh(self, driver):
        self.driver.refresh()

    def quit(self):
        self.driver.quit()

class test1:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{CASHNEST}/auth/logout")
        input()

if __name__ == __name__:
    test = test()
    username, password = test.login(test.driver) ; test.refresh(test.driver)

    test1 = test1(test.driver)

    test.quit()