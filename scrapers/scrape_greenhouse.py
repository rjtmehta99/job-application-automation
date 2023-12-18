# Keep search locations as they are on the job board, case insensitive
import time
from helpers.csv_helper import CSVManager
from helpers.scraper_helper import ScraperHelper
from helpers import constants
import logging
logging.basicConfig(level=logging.WARN)

def scrape(company_data):
    # Load company parameters from Greenhouse YAML file
    name = company_data['name']
    url = company_data['url']
    search_titles = company_data['search_titles']
    search_locations = company_data['search_locations']
    csv_path = company_data['csv_path']
    columns = company_data['columns']

    scraper = ScraperHelper(company_name=name)
    titles, urls, locations = [], [], []

    body = scraper.get_html_body(url)
    jobs = body.find_all('div', attrs={'class': 'opening'})
    for job in jobs:
        job_title = job.find('a').text.lower().strip()
        job_url = job.find('a')['href']
        job_url = constants.GH_BASE_URL + job_url
        job_location = job.find('span').text.lower()
        
        if job_location in search_locations:
            for title in job_title.split():
                if any(title in value for value in search_titles):
                    titles.append(job_title)
                    urls.append(job_url)
                    locations.append(job_location)

    csv_manager = CSVManager(csv_path=csv_path, columns=columns)
    jobs_df = csv_manager.save_jobs(job_data={'title': titles, 'url': urls, 'location': locations})
    scraper.notify_new_jobs(jobs_df=jobs_df, csv_path=csv_path)
    print(jobs_df)

if __name__ == '__main__':
    import yaml
    with open('./data/greenhouse_data.yaml', 'r') as file:
        master_data = yaml.safe_load(file)

    for company_data in master_data['greenhouse_companies']:
        scrape(company_data)
      