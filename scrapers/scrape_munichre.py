import yaml
import time
from jinja2 import Template
from helpers import constants
from helpers.csv_helper import CSVManager
from helpers.scraper_helper import ScraperHelper

def load_company_info(company_name: str):
    # From the company master data yaml, returns all data for the company_name
    with open(constants.COMPANY_MASTER_DATA, 'r') as file:
        master_data = yaml.safe_load(file)
    company_data = master_data.get(company_name)
    return company_data

def render_url(url: str, **template_args):
    # Renders the specified params into the URL. 
    # These params can be keywords, page number, job count etc. 
    template = Template(url)
    rendered_url = template.render(**template_args)
    return rendered_url

def scrape():
    print('Scraping Munich Re')
    scraper = ScraperHelper(company_name='MunichRe')
    #company_data = load_company_info(company_name='MunichRe')
    company_data = scraper.load_company_info()
    
    company_url = company_data['url']
    keywords = company_data['keywords']
    pages = company_data['pages']
    csv_path = company_data['csv_path']
    columns = company_data['columns']
    
    titles, urls, locations = [], [], []
    
    for keyword in keywords:
        try:
            for page in range(pages):
                try:
                    rendered_url = scraper.render_url(company_url, keyword=keyword, page=page)
    
                    body = scraper.get_html_body(rendered_url)
                    #response = requests.request("GET", rendered_url)
                    #body = BeautifulSoup(response.content, 'html.parser')                
                    titles_page = body.find_all('span', attrs={'class': 'card-header__job-position'})[1:]
                    locations_page = body.find_all('span', attrs={'class': 'card-header__job-place'})[1:]
                    urls_page = body.find_all('a', attrs={'class': 'button mre lightbox-trigger job-link-open'})
                    urls_page = [url['href'] for url in urls_page]

                    titles.extend(titles_page)
                    locations.extend(locations_page)
                    urls.extend(urls_page)
                    time.sleep(2)
                # If page does not exists
                except:
                    break
        # If no jobs for the keyword
        except:
            continue

    csv_manager = CSVManager(csv_path=csv_path, 
                            columns=columns) 
    jobs_df = csv_manager.save_jobs(job_data={'title': titles, 'url': urls, 'location': locations})
    scraper.notify_new_jobs(jobs_df=jobs_df, csv_path=csv_path)

if __name__ == '__main__':
    scrape()
