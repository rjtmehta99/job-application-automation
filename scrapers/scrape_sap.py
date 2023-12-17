import time
from helpers.csv_helper import CSVManager
from helpers.scraper_helper import ScraperHelper
import logging
logging.basicConfig(level=logging.WARN)

def scrape():
    scraper = ScraperHelper(company_name='SAP')
    company_data = scraper.load_company_info()
    
    company_url = company_data['url']
    keywords = company_data['keywords']
    levels = company_data['levels']
    next_page_queries = company_data['next_page_queries']
    csv_path = company_data['csv_path']
    columns = company_data['columns']
    
    titles, urls, locations = [], [], []
    
    for keyword in keywords:
        logging.warning(f' Searching jobs for keyword: {keyword}')
        for level in levels:
            for query in next_page_queries:
                try:
                    rendered_url = scraper.render_url(company_url, keyword=keyword, 
                                                      level=level, query=query)

                    body = scraper.get_html_body(rendered_url)

                    urls_page = body.find_all('a',
                                              attrs={'class': 'jobTitle-link'})
                    base_url = 'https://jobs.sap.com'
                    urls_page = [base_url+url['href'] for url in urls_page]
                    titles_page = [url.text for url in urls_page]
                    locations_page = body.find_all('span', 
                                                   attrs={'class': 'jobLocation'})
                    locations_page = [location.text for location in locations_page]

                    urls.extend(urls_page)
                    titles.extend(titles_page)
                    locations.extend(locations_page)
                    time.sleep(3)
                # If no jobs for the keyword
                except:
                    continue

    csv_manager = CSVManager(csv_path=csv_path, 
                            columns=columns) 
    jobs_df = csv_manager.save_jobs(job_data={'title': titles, 'url': urls, 'location': locations})
    scraper.notify_new_jobs(jobs_df=jobs_df, csv_path=csv_path)

if __name__ == '__main__':
    scrape()
