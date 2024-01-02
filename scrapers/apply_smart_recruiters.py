from __future__ import annotations
import re
import yaml
import logging
from helpers import constants
from notifications import notifier
from helpers.selenium_helper import Selenium
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from cv_resume_generator.render_cover_letter import render_cover_letter
logging.basicConfig(level=logging.WARN)

class SmartRecruiterApplier(Selenium):
    def __init__(self, url):
        super().__init__(url=url)
        # Load candidate data
        with open(constants.CANDIDATE_DATA, 'r') as file:
            self.candidate_data = yaml.safe_load(file)
    
    def clear_and_fill_info(self):
        # All information is first cleared, then entered from the YAML file.
        # Send first name
        self.clear_by_id(id_='first-name-input')
        self.send_keys_by_id(id_='first-name-input', key=self.candidate_data['first_name'])

        # Send last name
        self.clear_by_id(id_='last-name-input')
        self.send_keys_by_id(id_='last-name-input', key=self.candidate_data['last_name'])

        # Send email id
        self.clear_by_id(id_='email-input')
        self.send_keys_by_id(id_='email-input', key=self.candidate_data['email_id'])
        self.clear_by_id(id_='confirm-email-input')
        self.send_keys_by_id(id_='confirm-email-input', key=self.candidate_data['email_id'])

        # Send current location
        try:
            self.clear_by_xpath(xpath='//input[@class="sr-location-autocomplete element--input element--block"]')
            self.send_keys_by_xpath(xpath='//input[@class="sr-location-autocomplete element--input element--block"]',
                                    keys=[self.candidate_data['location'][:-1], Keys.DOWN, Keys.ENTER])
        except NoSuchElementException:
            self.clear_by_xpath(xpath='//input[@aria-label="Wohnsitz"]')
            self.send_keys_by_xpath(xpath='//input[@aria-label="Wohnsitz"]',
                                    keys=[self.candidate_data['location'][:-1], Keys.DOWN, Keys.ENTER])
        
        # Send contact number
        self.clear_by_id(id_='phone-number-input')
        self.send_keys_by_id(id_='phone-number-input', key=self.candidate_data['mobile_number'])


    def remove_extra_workex_edu(self):
            # Remove drafted information boxes for experience and education info from resume
            while True:
                try:
                    self.click_by_xpath('//button[(@data-test="experience-cancel")]')
                except NoSuchElementException:
                    break

            # Remove experience and education info from resume
            while True:
                try:
                    self.click_by_xpath(xpath='//button[(@aria-label="See options") or (@aria-label="Optionen anzeigen")]')
                    self.click_by_xpath('//button[@data-test="entry-delete"]')
                    self.click_by_xpath('//button[(text()="Yes") or (text()="Ja")]')
                except NoSuchElementException:
                    break


    def clear_and_fill_workex(self):
        # Add work experience
        for work_ex in self.candidate_data['work_experiences']:
            self.click_by_xpath(xpath='//button[@data-test="add-experience"]')

            # Send job title
            self.send_keys_by_xpath(xpath='//input[@data-test="job-title-autocomplete"]', 
                                        keys=[work_ex['position']])
            # Send company name
            self.send_keys_by_xpath(xpath='//input[@data-test="company-autocomplete"]', 
                                        keys=[work_ex['company'], Keys.ESCAPE])
            # Send job location
            self.send_keys_by_xpath(xpath='(//input[@class="sr-location-autocomplete element--input element--block"])[2]', 
                                        keys=[work_ex['location'], Keys.DOWN, Keys.ENTER])
            # Send job description
            self.send_keys_by_xpath(xpath='//textarea[@data-test="experience-description"]',
                                        keys=[work_ex['job_description']])
            
            start_date = {'month': str(work_ex['start_month']),
                        'year': str(work_ex['start_year'])}
            end_date = {'month': str(work_ex['end_month']),
                        'year': str(work_ex['end_year'])}
            self.add_dates_smartr(category='experience', 
                                    start=start_date,
                                    end=end_date)

            # Save work experience
            self.click_by_xpath(xpath='//button[@data-test="experience-save"]')
            self.sleep(duration=4)

            # Cancel new work experience block
            try:
                self.click_by_xpath(xpath='//button[@data-test="experience-cancel"]')
            except:
                pass


    def clear_and_fill_edu(self):            
        for degree in self.candidate_data['academics']:
            # Add academics
            self.click_by_xpath(xpath='//button[@data-test="add-education"]')
            # Univeristy Name
            self.send_keys_by_xpath(xpath='//input[@data-test="institution-autocomplete"]',
                                        keys=[degree['university'], Keys.DOWN, Keys.ENTER])
            # University Major
            self.send_keys_by_xpath(xpath='//input[@data-test="education-major"]',
                                        keys=[degree['major']])
            # University Degree
            self.send_keys_by_xpath(xpath='//input[@data-test="education-degree"]',
                                        keys=[degree['degree_level']])
            try:
                # University Location
                self.send_keys_by_xpath(xpath='//input[@data-test="location-autocomplete"]',
                                            keys=[degree['location']])
            except NoSuchElementException:
                self.send_keys_by_xpath(xpath='//input[(@aria-label="School location") or (@aria-label="Standort der Bildungsstätte")]',
                                            keys=[degree['location'], Keys.DOWN, Keys.ENTER])
            # Degree Description
            self.send_keys_by_xpath(xpath='//textarea[@data-test="education-description"]',
                                        keys=[degree['description']])
            start_date = {'month': str(degree['start_month']),
                        'year': str(degree['start_year'])}
            end_date = {'month': str(degree['end_month']),
                        'year': str(degree['end_year'])}
            self.add_dates_smartr(category='education', 
                                    start=start_date,
                                    end=end_date)
            # Save education
            self.click_by_xpath(xpath='//button[@data-test="education-save"]')

        try:
            # Cancel new education
            self.click_by_xpath(xpath='//button[@data-test="education-cancel"]')
        except NoSuchElementException:
            pass

    def get_cover_letter_args(self):
        # Get company name and job title to be inserted into cover letter
        position = self.get_text_by_xpath(xpath='//p[@data-test="topbar-job-title"]')
        position = re.sub(r'\((.*?)\)', '', position).strip()
        position = position.replace(r'\s+',' ')

        company_name = self.attribute_by_xpath(xpath='//img[@class="brand-logo"]', attribute='alt')
        company_name = company_name.replace(' Logo','').strip()

        args = {'COMPANY_NAME': company_name, 
                             'POSITION': position}
        return args


def apply(url: str) -> None:
    """
    Sends candidate's data from YAML file to Smart Recruiter Job Portal.
    Uploads the resume first and then deletes the auto-filled data from the portal.
    Then it will add relevant data from YAMl to fields.
    If information cannot be filled from YAML file, notification will popup so,
    the user can manually fill it.

    Args:
        url (str): job url
    """
    #selenium = selenium_helper.Selenium(url=url)
    applier = SmartRecruiterApplier(url)
    
    # Click on apply / jetzt bewerben
    try:
        try:
            applier.click_by_id('st-apply')
        except NoSuchElementException:
            applier.click_btn_by_text('Apply now!')
    except NoSuchElementException:
        logging.warn(' Click on apply failed, continuing applier')
    
    # Reject Cookies
    try:
        applier.click_by_id(id_='onetrust-reject-all-handler')
    except NoSuchElementException:
        pass

    # Upload resume, ensure absolute path
    applier.upload_file_by_css(css_selector="input[type='file']", file_path=constants.RESUME_PATH)

    applier.clear_and_fill_info()
    applier.remove_extra_workex_edu()
    applier.clear_and_fill_workex()
    applier.clear_and_fill_edu()

    # Send LinkedIn URL
    applier.send_keys_by_id(id_='linkedin-input', key=applier.candidate_data['linkedin_url'])

    # Render and send cover letter with job position and company name
    job_args = applier.get_cover_letter_args()
    cover_letter = render_cover_letter(job_args=job_args)
    applier.send_keys_by_id(id_='hiring-manager-message-input', key=cover_letter)

    # Click on T&C checkbox
    try:
        applier.click_by_id(id_='SINGLE')
    except NoSuchElementException:
        pass
    
    # Notify 
    try:
        # Click on submit
        applier.click_by_xpath(xpath='//button[@data-test="footer-submit"]')
        notifier.notify_application_success(job_args=job_args, urls=applier.url)
    except:
        # If submission failed (due to further information)
        notifier.notify_application_failure(job_args=job_args)