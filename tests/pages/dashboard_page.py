# tests/pages/dashboard_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def load(self):
        self.driver.get(self.base_url + "/dashboard")

    def click_add(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='student/add'], .btn-add")))
        self.driver.find_element(By.CSS_SELECTOR, "a[href*='student/add'], .btn-add").click()

    def get_rows(self):
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.students-table")))
        return self.driver.find_elements(By.CSS_SELECTOR, "table.students-table tbody tr")

    def search(self, q):
        search = self.driver.find_element(By.NAME, "q")
        search.clear()
        search.send_keys(q)
        search.submit()
