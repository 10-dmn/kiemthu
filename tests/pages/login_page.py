# tests/pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def load(self):
        self.driver.get(self.base_url + "/login")

    def login(self, username, password):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_flash(self):
        try:
            return WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash"))).text
        except:
            return ""
