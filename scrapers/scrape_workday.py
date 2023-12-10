from __future__ import annotations
from helpers.selenium_helper import Selenium
from helpers.selenium_helper import constants
from helpers.csv_helper import CSVManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from notifications import notifier
import pandas as pd
import yaml
import logging
logging.basicConfig(level=logging.WARN)


class WorkdayJobScraper(Selenium):
    def __init__(self, url, company, csv_path) -> None:
        super().__init__(url=url, headless=True)
        self.company = company
        self.csv_path = csv_path
        self.columns = constants.WORKDAY_COLUMNS
        self.csv_manager = CSVManager(csv_path=csv_path, columns=self.columns)
        self.sleep(duration=5.0)
    

    def scrape_jobs(self) -> tuple[list[str], list[str]]:
        jobs = self.driver.find_elements(by=By.XPATH, 
                                         value='//a[@data-automation-id="jobTitle"]')
        titles = [job.text for job in jobs]
        urls = [job.get_attribute('href') for job in jobs]
        return titles, urls


    def next_page(self) -> tuple[list[str], list[str]]:
        page_block = self.element_by_xpath(xpath='//nav[@aria-label="pagination"]')
        pages = self.elements_by_tag(tag='li', selected_element=page_block)[1:]
        len(pages)
        job_titles = []
        job_urls = []

        for page in pages:
            self.click_by_xpath(xpath='//button[@data-uxi-widget-type="stepToNextButton"]')
            titles, urls = self.scrape_jobs()
            job_titles.extend(titles)
            job_urls.extend(urls)
        return job_titles, job_urls
    

    def save_jobs(self, job_data: dict) -> pd.DataFrame:
        jobs_df = self.csv_manager.save_jobs(job_data=job_data)
        return jobs_df


    def scrape_workday(self) -> pd.DataFrame:
        logging.warning(f'Scraping Workday for {self.company}')

        try:
            self.click_by_xpath(xpath='//button[@data-automation-id="legalNoticeDeclineButton"]')
        except NoSuchElementException:
            # No Legal Notice Button Found
            pass

        job_titles, job_urls = self.scrape_jobs()
        try:
            job_titles_next_page, job_urls_next_page = self.next_page()
        except NoSuchElementException:
            # No pagination on website
            pass

        job_titles.extend(job_titles_next_page)
        job_urls.extend(job_urls_next_page)

        job_data = {'title': job_titles, 'url': job_urls}
        jobs_df = self.save_jobs(job_data=job_data)
        self.quit_driver()
        return jobs_df
    

    def notify_new_jobs(self, jobs_df: pd.DataFrame) -> None:
        unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()        
        if len(unnotified_jobs) > 0:
            notifier.notify_jobs(company=self.company, urls=unnotified_jobs)
            jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
            self.csv_manager.save_df_to_csv(df=jobs_df)
        else:
            print('No new jobs found')


if __name__ == '__main__':
    with open(constants.WORKDAY_DATA, 'r') as file:
        workday_data = yaml.safe_load(file)
    
    for data in workday_data['workday_companies']:
        logging.warning(f'Scraping Workday for {data["company_name"]}')
        scraper = WorkdayJobScraper(company=data['company_name'], 
                                    url=data['url'], 
                                    csv_path=data['csv_path'])
        jobs_df = scraper.scrape_workday()
        scraper.notify_new_jobs(jobs_df=jobs_df)
