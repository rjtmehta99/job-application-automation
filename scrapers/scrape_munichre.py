import time
from helpers.csv_helper import CSVManager
from helpers.scraper_helper import ScraperHelper
import logging
logging.basicConfig(level=logging.WARN)

def scrape():
    scraper = ScraperHelper(company_name='MunichRe')
    company_data = scraper.load_company_info()
    
    company_url = company_data['url']
    keywords = company_data['keywords']
    pages = company_data['pages']
    csv_path = company_data['csv_path']
    columns = company_data['columns']
    
    titles, urls, locations = [], [], []
    
    for keyword in keywords:
        logging.warning(f' Searching jobs for keyword: {keyword}')        
        try:
            for page in range(pages):
                try:
                    rendered_url = scraper.render_url(company_url, keyword=keyword, page=page)
                    
                    body = scraper.get_html_body(url=rendered_url)
                    titles_page = body.find_all('span', attrs={'class': 'card-header__job-position'})[1:]
                    titles_page = [title.text for title in titles_page]
                    locations_page = body.find_all('span', attrs={'class': 'card-header__job-place'})[1:]
                    locations_page = [location.text for location in locations_page]
                    urls_page = body.find_all('a', attrs={'class': 'button mre lightbox-trigger job-link-open'})
                    urls_page = [url['href'] for url in urls_page]

                    titles.extend(titles_page)
                    locations.extend(locations_page)
                    urls.extend(urls_page)
                    time.sleep(3)
                # If page does not exists
                except:
                    break
        # If no jobs for the keyword
        except:
            continue

    csv_manager = CSVManager(csv_path=csv_path, columns=columns) 
    jobs_df = csv_manager.save_jobs(job_data={'title': titles, 'url': urls, 'location': locations})
    scraper.notify_new_jobs(jobs_df=jobs_df, csv_path=csv_path)

if __name__ == '__main__':
    scrape()
