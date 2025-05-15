import os, sys, re, signal, random
from time import sleep
import requests
import logging
from threading import Thread
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) # this will only work for unix
from app import create_app, db
from app.models import Transactions, User
from config import TestConfig

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

DELAY = 0.8
CASHNEST = "http://127.0.0.1:1234"

#DATADIR = os.path.join(os.getcwd(), 'data')

class test:
    def __init__(self, private):
        
        self.options = Options()
        if private:
            self.options.add_argument(f"--incognito")
        #self.options.add_argument(f"user-data-dir={DATADIR}")
        self.driver = webdriver.Chrome(options=self.options)

        try:
            self.driver.set_window_size(1920, 1080) # Set Size       
        except Exception as e:
            print(f"{e}")

    def startapp(self):
        self.app = create_app(TestConfig)
        self.log = logging.getLogger('werkzeug')
        self.log.disabled = True
        self.app.config['WTF_CSRF_ENABLED'] = True
        def webserver():
            with self.app.app_context():
                db.create_all()
                self.app.run(host=CASHNEST.split("://")[1].split(":")[0], port=CASHNEST.split("://")[1].split(":")[1], use_reloader=False) # use flask wsgi without reload
        self.thread = Thread(target=webserver)
        self.thread.start()

    def logout(self, driver):
        self.driver.get(f"{CASHNEST}/auth/logout")

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

        test_username = os.urandom(8).hex()
        test_password = os.urandom(8).hex()
        test_newpassword = os.urandom(8).hex()

        self.driver.find_element(By.ID, "userDropdown").click() ; sleep(DELAY)
        self.driver.find_element(By.LINK_TEXT, "Login").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "username").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "username").send_keys(test_username) ; sleep(DELAY)
        self.driver.find_element(By.ID, "password").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "password").send_keys(test_password) ; sleep(DELAY)
        self.driver.find_element(By.ID, "signup-button").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".fa-user-circle").click() ; sleep(DELAY)
        self.driver.find_element(By.LINK_TEXT, "Settings").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "new_password").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "new_password").send_keys(test_newpassword) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-dark").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "userDropdown").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) > .dropdown-item").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".fa-user-circle").click() ; sleep(DELAY)
        self.driver.find_element(By.LINK_TEXT, "Login").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "username").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "username").send_keys(test_username) ; sleep(DELAY)
        self.driver.find_element(By.ID, "password").send_keys(test_newpassword) ; sleep(DELAY)
        self.driver.find_element(By.ID, "login-button").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".fa-user-circle").click() ; sleep(DELAY)
        self.driver.find_element(By.LINK_TEXT, "Settings").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger").click() ; sleep(DELAY)
        assert self.driver.switch_to.alert.text == "Are you sure you want to delete your account? This action cannot be undone." ; sleep(DELAY)
        self.driver.switch_to.alert.accept() ; sleep(DELAY)
 
class TestData:
    def __init__(self, driver):
        self.driver = driver

        test_income = random.randint(1, 100000)

        test_food_budget = random.randint(1, 10000)
        test_rent_budget = random.randint(1, 10000)
        test_utilities_budget = random.randint(1, 10000)
        test_shopping_budget = random.randint(1, 10000)
        test_entertainment_budget = random.randint(1, 10000)
        test_other_budget = random.randint(1, 10000)
        test_goal1_budget = random.randint(1, 10000)
        test_goal2_budget = random.randint(1, 10000)
        test_goal3_budget = random.randint(1, 10000)

        test_transaction0_name = os.urandom(8).hex()
        test_transaction0_amount = random.randint(1, 1000)

        test_transaction1_name = os.urandom(8).hex()
        test_transaction1_amount = random.randint(1, 1000)

        test_transaction2_name = os.urandom(8).hex()
        test_transaction2_amount = random.randint(1, 1000)

        self.driver.find_element(By.LINK_TEXT, "Data").click() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "income") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).click_and_hold().perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "income") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "income") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).release().perform() ; sleep(DELAY)
        self.driver.find_element(By.ID, "income").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "income").send_keys(test_income) ; sleep(DELAY)
        self.driver.find_element(By.ID, "food_budget").send_keys(test_food_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "rent_budget").send_keys(test_rent_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "utilities_budget").send_keys(test_utilities_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "shopping_budget").send_keys(test_shopping_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "entertainment_budget").send_keys(test_entertainment_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "other_budget").send_keys(test_other_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "goal1_budget").send_keys(test_goal1_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "goal2_budget").send_keys(test_goal2_budget) ; sleep(DELAY)
        self.driver.find_element(By.ID, "goal3_budget").send_keys(test_goal3_budget) ; sleep(DELAY)
        driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, "submit")) ; sleep(DELAY)
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.ID, "name").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "name").send_keys(test_transaction0_name) ; sleep(DELAY)
        dropdown = self.driver.find_element(By.ID, "category") ; sleep(DELAY)
        dropdown.find_element(By.XPATH, "//option[. = 'Shopping']").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").send_keys(test_transaction0_amount) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".col-auto > #submit").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "name").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "name").send_keys(test_transaction1_name) ; sleep(DELAY)
        dropdown = self.driver.find_element(By.ID, "category") ; sleep(DELAY)
        dropdown.find_element(By.XPATH, "//option[. = 'Goal 3']").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(9)").click() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "amount") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).click_and_hold().perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "amount") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "amount") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).release().perform() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").send_keys(test_transaction1_amount) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".col-auto > #submit").click() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "name") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).click_and_hold().perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "name") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).perform() ; sleep(DELAY)
        element = self.driver.find_element(By.ID, "name") ; sleep(DELAY)
        actions = ActionChains(self.driver) ; sleep(DELAY)
        actions.move_to_element(element).release().perform() ; sleep(DELAY)
        self.driver.find_element(By.ID, "name").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "name").send_keys(test_transaction1_name) ; sleep(DELAY)
        dropdown = self.driver.find_element(By.ID, "category") ; sleep(DELAY)
        dropdown.find_element(By.XPATH, "//option[. = 'Shopping']").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, "option:nth-child(4)").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "amount").send_keys(test_transaction2_amount) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".col-auto > #submit").click() ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".col-auto > #submit").click() ; sleep(DELAY)
        driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) .btn")) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) .btn").click() ; sleep(DELAY)

class TestExpenditure:
    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element(By.LINK_TEXT, "Tracking").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "submit").click() ; sleep(DELAY)

class TestBudget:
    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element(By.LINK_TEXT, "Budget").click() ; sleep(DELAY)
        driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.CSS_SELECTOR, ".animate__fadeInLeft .card-action")) ; sleep(DELAY)

class TestShare:
    def __init__(self, driver, shareuser):
        self.driver = driver
        
        self.shareuser = shareuser
        test_message = os.urandom(8).hex()
        self.driver.refresh() ; sleep(DELAY)

        self.driver.find_element(By.LINK_TEXT, "Budget").click() ; sleep(DELAY)
        sleep(5) # Slow Loading Page
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.CSS_SELECTOR, ".goal-container:nth-child(1) .share-button")) ; sleep(DELAY)
        sleep(5) # Slow Loading Page
        self.driver.find_element(By.CSS_SELECTOR, ".goal-container:nth-child(1) .share-button").click() ; sleep(DELAY)
        sleep(5) # Slow Loading Page
        self.driver.find_element(By.ID, "username").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "username").send_keys(self.shareuser) ; sleep(DELAY)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, "message"))
        sleep(2) # Slow Loading Page
        self.driver.find_element(By.ID, "message").click() ; sleep(DELAY)
        self.driver.find_element(By.ID, "message").send_keys(test_message) ; sleep(DELAY)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click() ; sleep(DELAY)
        self.driver.switch_to.alert.accept() ; sleep(DELAY)
        #element = self.driver.find_element(By.CSS_SELECTOR, ".btn-primary") ; sleep(DELAY)
        #actions = ActionChains(self.driver) ; sleep(DELAY)
        #actions.move_to_element(element).perform() ; sleep(DELAY)
        #element = self.driver.find_element(By.CSS_SELECTOR, "body") ; sleep(DELAY)
        #actions = ActionChains(self.driver) ; sleep(DELAY)
        #actions.move_to_element(element, 0, 0).perform() ; sleep(DELAY)


class TestShareView: # this is part of the prior test, just the different user
    def __init__(self, driver):
        self.driver = driver

        self.driver.find_element(By.LINK_TEXT, "Budget").click() ; sleep(DELAY)
        sleep(5) # Slow Loading Page
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.CSS_SELECTOR, ".goal-container:nth-child(1) .share-button")) ; sleep(DELAY)
        sleep(5) # Slow Loading Page
        self.driver.find_element(By.CSS_SELECTOR, ".goal-container:nth-child(1) .share-button").click() ; sleep(DELAY); sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-sm").click() ; sleep(DELAY)
        #self.driver.switch_to.alert.accept() ; sleep(DELAY)
    
if __name__ == "__main__":
    print(f"Initialising Tests... (Sleeping 7)")
    user = test(False) ; user.startapp()
    sleep(5)
    user.refresh(user.driver) ; sleep(2)

    print(f"Test 1: Account Functionality")
    try:
        TestAccount(user.driver)
        print(f"Test Passed")
    except Exception as e:
        print(f"Test Failed ({e})")
    
    print(f"Injecting Persistent Session for Remaining Tests... (Sleeping 5)")
    username, password = user.login(user.driver) ; user.refresh(user.driver)
    sleep(5)

    print(f"Test 2: Data Entry")
    try:
        TestData(user.driver)
        print(f"Test Passed (Sleeping 3)")
    except Exception as e:
        print(f"Test Failed ({e})")
    user.refresh(user.driver); sleep(3)

    print(f"Test 3: Expenditure")
    try:
        TestExpenditure(user.driver)
        print(f"Test Passed (Sleeping 3)")
    except Exception as e:
        print(f"Test Failed ({e})")
    user.refresh(user.driver); sleep(3)

    print(f"Test 4: Budget")
    try:
        TestBudget(user.driver)
        print(f"Test Passed (Sleeping 3)")
    except Exception as e:
        print(f"Test Failed ({e})")
    user.refresh(user.driver); sleep(3)
    
    print(f"Test 5: Share")
    
    print(f"Creating Second User to Share (Sleeping 7)")
    usershare = test(True) ; sleep(3)
    usershare.refresh(usershare.driver) ; sleep(2) # current document domain must match set_cookie
    username2, password2 = usershare.login(usershare.driver)
    usershare.refresh(usershare.driver) # ; usershare.quit()
    sleep(2)
    
    try:
        TestShare(user.driver, username2)
        TestShareView(usershare.driver)
        print(f"Test Passed")

    except Exception as e:
        print(f"Test Failed ({e})")
    user.refresh(user.driver)

    print(f"Testing Completed!")
    user.quit() ; usershare.quit()
    pid = os.getpid() # todo: kill thread as part of quit()
    os.kill(pid, signal.SIGTERM)