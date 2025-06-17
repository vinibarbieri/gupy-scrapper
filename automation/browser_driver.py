from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from .web_driver import WebAutomationDriver


class BrowserDriver(WebAutomationDriver):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def open_url(self, url: str):
        self.driver.get(url)
        time.sleep(2)

    def click(self, selector: str, by="css"):
        if by == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
        elif by == "xpath":
            element = self.driver.find_element(By.XPATH, selector)
        else:
            raise ValueError("Unsupported selector type. Use 'css' or 'xpath'.")
        element.click()
        time.sleep(1)


    def type(self, selector: str, text: str):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.clear()
        element.send_keys(text)
        time.sleep(1)

    def upload_file(self, selector: str, file_path: str):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.send_keys(file_path)
        time.sleep(1)

    def get_text(self, selector: str) -> str:
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        return element.text

    def close(self):
        self.driver.quit()

    def wait_and_click(self, selector: str, by="css", timeout=10):
        if by == "css":
            locator = (By.CSS_SELECTOR, selector)
        elif by == "xpath":
            locator = (By.XPATH, selector)
        else:
            raise ValueError("Unsupported selector type. Use 'css' or 'xpath'.")

        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        time.sleep(1)
