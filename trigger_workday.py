from scrapers.scrape_workday import WorkdayJobScraper
from helpers import constants
import yaml

with open(constants.WORKDAY_DATA, 'r') as file:
    workday_data = yaml.safe_load(file)

for data in workday_data['workday_companies']:
    scraper = WorkdayJobScraper(company=data['company_name'], 
                                url=data['url'], 
                                csv_path=data['csv_path'])
    jobs_df = scraper.scrape_workday()
    scraper.notify_new_jobs(jobs_df=jobs_df)
