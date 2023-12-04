from __future__ import annotations
import re
import yaml
from helpers import selenium_helper, constants
from notifications import notifier
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from cv_resume_generator.render_cover_letter import render_cover_letter


with open(constants.CANDIDATE_DATA, 'r') as file:
    candidate_data = yaml.safe_load(file)

URL = 'https://jobs.smartrecruiters.com/HitachiSolutions/743999948479923-machine-learning-ai-engineer-m-w-d-'

selenium = selenium_helper.Selenium(url=URL)

# Click on apply / jetzt bewerben
selenium.click_by_id('st-apply')

# Reject Cookies
try:
    selenium.click_by_id(id_='onetrust-reject-all-handler')
except NoSuchElementException:
    pass

# Upload resume, ensure absolute path
selenium.upload_file_by_css(css_selector="input[type='file']", file_path=constants.RESUME_PATH)

# Send first name
selenium.clear_by_id(id_='first-name-input')
selenium.send_keys_by_id(id_='first-name-input', key=candidate_data['first_name'])

# Send last name
selenium.clear_by_id(id_='last-name-input')
selenium.send_keys_by_id(id_='last-name-input', key=candidate_data['last_name'])

# Send email id
selenium.clear_by_id(id_='email-input')
selenium.send_keys_by_id(id_='email-input', key=candidate_data['email_id'])
selenium.clear_by_id(id_='confirm-email-input')
selenium.send_keys_by_id(id_='confirm-email-input', key=candidate_data['email_id'])

# Send current location
selenium.clear_by_xpath(xpath='//input[@class="sr-location-autocomplete element--input element--block"]')
selenium.send_keys_by_xpath(xpath='//input[@class="sr-location-autocomplete element--input element--block"]',
                            keys=[candidate_data['location'][:-1], Keys.DOWN, Keys.ENTER])

# Send contact number
selenium.clear_by_id(id_='phone-number-input')
selenium.send_keys_by_id(id_='phone-number-input', key=candidate_data['mobile_number'])

# Remove drafted information boxes for experience and education info from resume
while True:
    try:
        selenium.click_by_xpath('//button[(@data-test="experience-cancel")]')
    except NoSuchElementException:
        break

# Remove experience and education info from resume
while True:
    try:
        selenium.click_by_xpath(xpath='//button[@aria-label="See options"]')
        selenium.click_by_xpath('//button[@data-test="entry-delete"]')
        selenium.click_by_xpath('//button[(text()="Yes") or (text()="Ja")]')
    except NoSuchElementException:
        break

# Add work experience
for work_ex in candidate_data['work_experiences']:
    selenium.click_by_xpath(xpath='//button[@data-test="add-experience"]')

    # Send job title
    selenium.send_keys_by_xpath(xpath='//input[@data-test="job-title-autocomplete"]', 
                                keys=[work_ex['position']])
    # Send company name
    selenium.send_keys_by_xpath(xpath='//input[@data-test="company-autocomplete"]', 
                                keys=[work_ex['company'], Keys.ESCAPE])
    # Send job location
    selenium.send_keys_by_xpath(xpath='(//input[@class="sr-location-autocomplete element--input element--block"])[2]', 
                                keys=[work_ex['location'], Keys.DOWN, Keys.ENTER])

    selenium.send_keys_by_xpath(xpath='//textarea[@data-test="experience-description"]',
                                keys=[work_ex['job_description']])
    
    start_date = {'month': str(work_ex['start_month']),
                  'year': str(work_ex['start_year'])}
    end_date = {'month': str(work_ex['end_month']),
                'year': str(work_ex['end_year'])}
    selenium.add_dates_smartr(category='experience', 
                              start=start_date,
                              end=end_date)

    # Save work experience
    selenium.click_by_xpath(xpath='//button[@data-test="experience-save"]')

    selenium.sleep(duration=4)

# Cancel new work experience block
try:
    selenium.click_by_xpath(xpath='//button[@data-test="experience-cancel"]')
except:
    pass


for degree in candidate_data['academics']:
    # Add academics
    selenium.click_by_xpath(xpath='//button[@data-test="add-education"]')

    # Univeristy Name
    selenium.send_keys_by_xpath(xpath='//input[@data-test="institution-autocomplete"]',
                                keys=[degree['university'], Keys.DOWN, Keys.ENTER])
    # University Major
    selenium.send_keys_by_xpath(xpath='//input[@data-test="education-major"]',
                                keys=[degree['major']])
    # University Degree
    selenium.send_keys_by_xpath(xpath='//input[@data-test="education-degree"]',
                                keys=[degree['degree_level']])
    try:
        # University Location
        selenium.send_keys_by_xpath(xpath='//input[@data-test="location-autocomplete"]',
                                    keys=[degree['location']])
    except NoSuchElementException:
        selenium.send_keys_by_xpath(xpath='//input[@aria-label="School location"]',
                                    keys=[degree['location'], Keys.DOWN, Keys.ENTER])
    # Degree Description
    selenium.send_keys_by_xpath(xpath='//textarea[@data-test="education-description"]',
                                keys=[degree['description']])

    start_date = {'month': str(degree['start_month']),
                  'year': str(degree['start_year'])}
    end_date = {'month': str(degree['end_month']),
                'year': str(degree['end_year'])}
    selenium.add_dates_smartr(category='education', 
                              start=start_date,
                              end=end_date)

    # Save education
    selenium.click_by_xpath(xpath='//button[@data-test="education-save"]')

try:
    # Cancel new education
    selenium.click_by_xpath(xpath='//button[@data-test="education-cancel"]')
except NoSuchElementException:
    pass


# Send LI URL
selenium.send_keys_by_id(id_='linkedin-input', key=candidate_data['linkedin_url'])

# Click on checkbox
try:
    selenium.click_by_id(id_='SINGLE')
except NoSuchElementException:
    pass

# Render Cover Letter 
position = selenium.get_text_by_xpath(xpath='//p[@data-test="topbar-job-title"]')
position = re.sub(r'\((.*?)\)', '', position).strip()
#position = position.replace(r'\(.*?\)','',rege).strip()
position = position.replace(r'\s+',' ')

company_name = selenium.attribute_by_xpath(xpath='//img[@class="brand-logo"]', attribute='alt')
company_name = company_name.replace(' Logo','').strip()

job_args = {'COMPANY_NAME': company_name, 
            'POSITION': position}
cover_letter = render_cover_letter(job_args)

selenium.send_keys_by_id(id_='hiring-manager-message-input', key=cover_letter)

try:
    # Click on submit
    selenium.click_by_xpath(xpath='//button[@data-test="footer-submit"]')
    notifier.notify_application_success(job_args=job_args)
except:
    notifier.notify_application_failure(job_args=job_args)