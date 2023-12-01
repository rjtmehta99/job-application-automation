from helpers import selenium_helper, constants
from selenium.webdriver.common.by import By
import keyring
from selenium.webdriver.common.keys import Keys

URL = 'https://jobs.smartrecruiters.com/oneclick-ui/company/HitachiSolutions/publication/c83eaee0-aaa4-49a9-b380-7259c05fe178?dcr_ci=HitachiSolutions'

selenium = selenium_helper.Selenium(url=URL)

# Send first name
first_name = keyring.get_password('scraper', 'first_name')
selenium.send_keys_by_id(id_='first-name-input', key=first_name)

# Send last name
last_name = keyring.get_password('scraper', 'last_name')
selenium.send_keys_by_id(id_='last-name-input', key=last_name)

# Send email id
candidate_email = keyring.get_password('scraper', 'email')
selenium.send_keys_by_id(id_='email-input', key=candidate_email)
selenium.send_keys_by_id(id_='confirm-email-input', key=candidate_email)

# Upload resume, ensure absolute path
file_input = selenium.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
file_input.send_keys(constants.RESUME_PATH)

# Send LI URL
candidate_linkedin = keyring.get_password('scraper', 'linkedin-url')
selenium.send_keys_by_id(id_='linkedin-input', value=candidate_linkedin)

# Click on checkbox
selenium.click_by_id(id_='SINGLE')