from helpers import selenium_helper, constants
from selenium.webdriver.common.by import By
import keyring
from selenium.webdriver.common.keys import Keys

URL = 'https://jobs.smartrecruiters.com/oneclick-ui/company/HitachiSolutions/publication/c83eaee0-aaa4-49a9-b380-7259c05fe178?dcr_ci=HitachiSolutions'

selenium = selenium_helper.Selenium(url=URL)

file_input = selenium.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
file_input.send_keys(constants.RESUME_PATH)

user_email = keyring.get_password('scraper', 'email')
confirm_email = selenium.driver.find_element(By.ID, "confirm-email-input")
confirm_email.send_keys(user_email)

user_location = keyring.get_password('scraper', 'location')
location = selenium.driver.find_element(by=By.XPATH, value="//input[@class='sr-location-autocomplete element--input element--block']")
location.send_keys(user_location[:-1])
location.send_keys(Keys.DOWN)
location.send_keys(Keys.ENTER)

user_linkedin = keyring.get_password('scraper', 'linkedin-url')
linkedin = selenium.driver.find_element(by=By.ID, value='linkedin-input')
linkedin.send_keys(user_linkedin)

checkbox = selenium.driver.find_element(by=By.ID, value='SINGLE')
checkbox.click()


with open('./data/Resume_Rajat_Mehta.pdf') as f:
    print(f.name)