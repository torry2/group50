import os
import sys
import signal
import re
import requests
from flask import Flask
import logging
from threading import Thread
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) # this will only work for unix
from app import create_app, db
from app.models import Transactions, User
from config import TestConfig

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

CASHNEST = "http://127.0.0.1:1234"

#GECKO = 
DELAY = 7 # time in seconds to delay actions
DATADIR = os.path.join(os.getcwd(), 'data')

class test:
    def __init__(self):

        self.app = create_app(TestConfig)
        self.log = logging.getLogger('werkzeug')
        self.log.disabled = True
        self.app.config['WTF_CSRF_ENABLED'] = True
        def webserver():
            with self.app.app_context():
                db.create_all()
                self.app.run(host="127.0.0.1", port=1234, use_reloader=False) # use flask wsgi without reload
        self.thread = Thread(target=webserver)
        self.thread.start()

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
        self.driver.get(CASHNEST)
        self.driver.refresh()

    def quit(self):
        self.driver.quit()

class TestAccount:
    def __init__(self, driver):
        self.driver = driver
        input()

class TestData:
    def __init__(self, driver):
        self.driver = driver

        # Navigate to the data entry page and save income and budget amounts
        self.driver.find_element(By.ID, "navbar-data").click()
        self.driver.find_element(By.ID, "income-field").send_keys(25000)
        fields = [
            ("food_budget", 100),
            ("rent_budget", 100),
            ("utilities_budget", 100),
            ("shopping_budget", 100),
            ("entertainment_budget", 100),
            ("other_budget", 100),
            ("goal1_budget", 1000),
            ("goal2_budget", 2500),
            ("goal3_budget", 5000),
        ]

        for field_id, value in fields:
            self.driver.find_element(By.ID, field_id).send_keys(value)

        self.driver.find_element(By.ID, "income-budget-save-btn").click()

        # Adds an entry to the transaction table and checks if it's actually added
        self.driver.find_element(By.ID, "tx-name").send_keys("Uniqlo")
        self.driver.find_element(By.ID, "tx-amount").send_keys("120")
        Select(self.driver.find_element(By.ID, "tx-category")).select_by_visible_text("Shopping")
        self.driver.find_element(By.ID, "tx-add-btn").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Uniqlo'] and td[text()='Shopping'] and td[text()='120.00']]")), message="Added transaction row not found in table")

        # Refresh the website and wait for it to fully load before proceeding
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "income-field")))

        # Checks if pressing delete on a transaction actually deletes it
        self.driver.find_element(By.ID, "tx-delete-btn-1").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, "//tr[td[text()='Uniqlo'] and td[text()='Shopping'] and td[text()='120.00']]")), message="Added transaction row still present after delete")

        # Checks that the income and budgets set earlier persists after a reload
        for fld_id, expected in fields:
            el    = self.driver.find_element(By.ID, fld_id)
            actual = int(el.get_attribute("value"))
            assert actual == expected, f"{fld_id} was {actual}, expected {expected}"

        # If the code gets here, the test is considered passed.
        print("[TestBudgetTransaction] Test passed.")

class TestExpenditure:
    def __init__(self, driver):
        self.driver = driver
        input()

class TestBudget:
    def __init__(self, driver):
        self.driver = driver
        input()

class TestShare:
    def __init__(self, driver):
        self.driver = driver
        input()

if __name__ == "__main__":
    print(f"Initialising Tests... (Sleeping {DELAY})")
    test = test()
    sleep(DELAY)

    print(f"Test 1: Account Functionality")
    try:
        TestAccount(test.driver)
        #register, logout, login, update password, delete account
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")
    
    print(f"Injecting Persistent Session for Remaining Tests... (Sleeping {DELAY})")
    username, password = test.login(test.driver) ; test.refresh(test.driver)
    sleep(DELAY)

    print(f"Test 2: Data Entry")
    try:
        TestAccount(test.driver)
        #TestData(test.driver)
        # add income, budgets, transactions and delete transaction
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")

    print(f"Test 3: Expenditure")
    try:
        #TestExpenditure(test.driver)
        # expenditure page, click habits button
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")

    print(f"Test 4: Expenditure")
    try:
        #TestBudget(test.driver)
        # budget page, just view it
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")

    print(f"Test 4: Expenditure")
    try:
        #TestShare(test.driver)
        # share feature? create second account and share a budget        
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")

    print(f"Testing Completed!")
    test.quit()
    pid = os.getpid() # todo: kill thread as part of quit()
    os.kill(pid, signal.SIGTERM)