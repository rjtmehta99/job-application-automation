import time
import requests
from bs4 import BeautifulSoup
from helpers import constants
from helpers.csv_helper import CSVManager

def scrape():    
    titles, urls, locations = [], [], []
    for keyword in constants.MUNICHRE_KEYWORDS:
        try:
            for page in range(constants.MUNICHRE_PAGE_RANGE):
                try:
                    url = f'https://munichre-jobs.com/api/list/Job?template=MunichRe&sortitem=id&sortdirection=DESC&format=cards&lang=en&widget=0&filter[company.id]=[1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C27%2C29%2C31%2C32%2C33%2C51%2C52%2C53%2C54%2C55%2C56%2C57%2C59%2C60%2C61%2C62%2C63%2C64%2C28%2C69%2C70%2C71%2C68%2C72]&filter[display_language]=en&filter[publication_channel]=careersite&filter[city.id]=[44324%2C43182%2C39117%2C37611]&keyword={keyword}&filter[entry_level.id]=[5%2C6]&sort[id]=DESC&page={page}'
                    response = requests.request("GET", url)
                    body = BeautifulSoup(response.content, 'html.parser')
                
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

    csv_manager = CSVManager(csv_path=constants.MUNICHRE_JOBS_CSV, 
                            columns=['title', 'url', 'location', 'notified']) 
    jobs_df = csv_manager.save_jobs(job_data={'title': titles, 'url': urls, 'location': locations})
    return jobs_df

if __name__ == '__main__':
    scrape()
