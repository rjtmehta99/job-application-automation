from __future__ import annotations
import yaml
from helpers import selenium_helper, constants
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from cv_resume_generator.render_cover_letter import render_cover_letter

with open(constants.CANDIDATE_DATA, 'r') as file:
    candidate_data = yaml.safe_load(file)

URL = 'https://jobs.smartrecruiters.com/oneclick-ui/company/HitachiSolutions/publication/c83eaee0-aaa4-49a9-b380-7259c05fe178?dcr_ci=HitachiSolutions'
#URL = 'https://jobs.smartrecruiters.com/oneclick-ui/company/BoschGroup/publication/0481e880-871a-42dd-8231-53a2ae8c8d37?dcr_ci=BoschGroup'

selenium = selenium_helper.Selenium(url=URL)

# Reject Cookies
selenium.click_by_id(id_='onetrust-reject-all-handler')

# Send first name
selenium.send_keys_by_id(id_='first-name-input', key=candidate_data['first_name'])

# Send last name
selenium.send_keys_by_id(id_='last-name-input', key=candidate_data['last_name'])

# Send email id
selenium.send_keys_by_id(id_='email-input', key=candidate_data['email_id'])
selenium.send_keys_by_id(id_='confirm-email-input', key=candidate_data['email_id'])

# Send current location
selenium.send_keys_by_xpath(xpath='//input[@class="sr-location-autocomplete element--input element--block"]',
                            keys=[candidate_data['location'][:-1], Keys.DOWN, Keys.ENTER])

# Send contact number
selenium.send_keys_by_id(id_='phone-number-input', key=candidate_data['mobile_number'])

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
selenium.click_by_xpath(xpath='//button[@data-test="experience-cancel"]')

# Add academics
selenium.click_by_xpath(xpath='//button[@data-test="add-education"]')

for degree in candidate_data['academics']:
    # Univeristy Name
    selenium.send_keys_by_xpath(xpath='//input[@data-test="institution-autocomplete"]',
                                keys=[degree['university']])
    # University Major
    selenium.send_keys_by_xpath(xpath='//input[@data-test="education-major"]',
                                keys=[degree['major']])
    # University Degree
    selenium.send_keys_by_xpath(xpath='//input[@data-test="education-degree"]',
                                keys=[degree['degree_level']])
    # University Location
    selenium.send_keys_by_xpath(xpath='//input[@data-test="location-autocomplete"]',
                                keys=[degree['location']])
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

# Cancel new education
selenium.click_by_xpath(xpath='//button[@data-test="education-cancel"]')

# Upload resume, ensure absolute path
selenium.upload_file_by_css(css_selector="input[type='file']", file_path=constants.RESUME_PATH)

# Send LI URL
selenium.send_keys_by_id(id_='linkedin-input', value=candidate_data['linkedin_url'])

# Click on checkbox
selenium.click_by_id(id_='SINGLE')

# Render Cover Letter 
position = selenium.get_text_by_xpath(xpath='//p[@data-test="topbar-job-title"]')
position = position.replace(r'\((.*?)\)','').strip()
position = position.replace(r'\s+',' ')

company_name = selenium.attribute_by_xpath(xpath='//img[@class="brand-logo"]', attribute='alt')
company_name = company_name.replace(' Logo','').strip()

job_args = {'COMPANY_NAME': company_name, 
            'POSITION': position}
cover_letter = render_cover_letter(job_args)

selenium.send_keys_by_id(id_='hiring-manager-message-input', key=cover_letter)

# Click on submit
#selenium.click_by_xpath(xpath='//button[@data-test="footer-submit"]')
