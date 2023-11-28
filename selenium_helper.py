from __future__ import annotations
import time
import constants
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


class Selenium():
    def __init__(self, url: str, headless: bool = False) -> None:
        self.url = url
        options = webdriver.FirefoxOptions()
        options.headless = headless
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        self.driver.get(url)
        self.sleep()

    def wait_by_class(self, value: str) -> None:
        """
        Wait for element to be loaded.
        Element to be found using class attribute.
        """
        try:
            WebDriverWait(self.driver, constants.ELEMENT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        except:
            print('[ERROR] Element not loaded error')

    def wait_by_id(self, value: str) -> None:
        """
        Wait for element to be loaded.
        Element to be found using id attribute.
        """
        try:
            WebDriverWait(self.driver, constants.ELEMENT_TIMEOUT).until(EC.presence_of_element_located((By.ID, value)))
        except:
            print('[ERROR] Element not loaded error')

    def sleep(self, duration: float = 2.0):
        time.sleep(duration)

    def click_btn_by_text(self, text: str) -> None:
        btn = self.driver.find_element(by=By.LINK_TEXT, value=text)
        btn.click()
        self.sleep()        

    def click_by_xpath(self, xpath: str) -> None:
        btn = self.driver.find_element(by=By.XPATH, value=xpath)
        btn.click()
    
    def click_by_id(self, id_: str) -> None:
        btn = self.driver.find_element(by=By.ID, value=id_)
        btn.click()
        self.sleep()

    def element_by_class(self, class_: str, selected_element: WebDriver = None) -> FirefoxWebElement:
        if selected_element:
            element = selected_element.find_element(by=By.CLASS_NAME, value=class_)
        else:
            element = self.driver.find_element(by=By.CLASS_NAME, value=class_)
        return element

    def elements_by_class(self, class_: str, selected_element: WebDriver = None) -> list[FirefoxWebElement]:
        if selected_element:
            elements = selected_element.find_elements(by=By.CLASS_NAME, value=class_)
        else:
            elements = self.driver.find_elements(by=By.CLASS_NAME, value=class_)
        return elements
    
    def element_by_tag(self, tag: str, selected_element: WebDriver = None) -> FirefoxWebElement:
        if selected_element:
            element = selected_element.find_element(by=By.TAG_NAME, value=tag)
        else:
            element = self.driver.find_element(by=By.TAG_NAME, value=tag)
        return element
    
    def element_by_xpath(self, xpath: str, selected_element: WebDriver = None) -> FirefoxWebElement:
        if selected_element:
            element = selected_element.find_element(by=By.XPATH, value=xpath)
        else:
            element = self.driver.find_element(by=By.XPATH, value=xpath)
        return element

    def quit_driver(self) -> None:
        self.driver.quit()