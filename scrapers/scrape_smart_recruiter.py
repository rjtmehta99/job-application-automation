from __future__ import annotations
from helpers import constants
import pandas as pd
from helpers import selenium_helper
from selenium.common.exceptions import NoSuchElementException
import logging
logging.basicConfig(level=logging.WARN)

def scrape(urls: list[str]) -> pd.DataFrame:
    job_urls = []
    positions = []
    companies = []
    locations = []
    
    for url in urls:
        logging.warning(f'Scraping {url}')
        selenium = selenium_helper.Selenium(url=url, headless=True)
        try:
            selenium.click_by_id(id_='onetrust-accept-btn-handler')
        except NoSuchElementException:
            pass

        table = selenium.element_by_class(class_='jobs-list')
        rows = selenium.elements_by_class(class_='jobs-item', selected_element=table)

        for row in rows:
            job_details = selenium.element_by_tag(tag='a', selected_element=row)
            job_url = job_details.get_attribute('href')
            job_details = job_details.text.split('\n')
            position = job_details[0]
            company = job_details[1]
            location = job_details[2]

            # if 'gmbh' in company.lower() or ('germany' or 'deutschland') in location.lower():
            company_match = list(filter(lambda word: word in constants.COMPANY_CRITERIA, company.lower().split()))
            location_match = list(filter(lambda word: word in constants.LOCATION_CRITERIA, location.lower().split()))

            if (len(company_match) or len(location_match)) > 0:
                job_urls.append(job_url)
                positions.append(position)
                companies.append(company)
                locations.append(location)
        selenium.quit_driver()
    
    try:
        previous_df = pd.read_csv(constants.SMART_RECRUITERS_JOBS)
    except FileNotFoundError:
        previous_df = pd.DataFrame(columns=['position', 'company', 'location', 'url', 'notified'])
    
    current_df = pd.DataFrame(data={'position': positions, 'company': companies, 
                                    'location': locations, 'url': job_urls})
    #current_df.to_csv('current_df.csv', index=False)
    current_df['notified'] = False
    merged_df = pd.concat([current_df, previous_df])
    merged_df = merged_df.drop_duplicates(subset=['url'], keep='last').reset_index(drop=True)
    new_jobs = len(merged_df) - len(previous_df)
    logging.warn(f'{new_jobs} new jobs found')
    merged_df.to_csv(constants.SMART_RECRUITERS_JOBS, index=False)
    return merged_df

if __name__ == '__main__':
    scrape(urls=constants.SMART_RECRUITERS_URLS)
