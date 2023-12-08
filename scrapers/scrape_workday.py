from helpers.selenium_helper import Selenium
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_jobs(selenium: Selenium):
    #table = selenium.element_by_xpath(xpath='//section[@data-automation-id="jobResults"]')
    #rows = selenium.elements_by_class(class_='css-1q2dra3', selected_element=table)
    jobs = selenium.driver.find_elements(by=By.XPATH, value='//a[@data-automation-id="jobTitle"]')
    titles = []
    urls = []
    for job in jobs:
        titles.append(job.text)
        urls.append(job.get_attribute('href'))
    return titles, urls

def next_page(selenium: Selenium):
    # Go to next page
    page_block = selenium.element_by_xpath(xpath='//nav[@aria-label="pagination"]')
    pages = selenium.elements_by_tag(tag='li', selected_element=page_block)[1:]
    
    job_titles = []
    job_urls = []

    for page in pages:
        selenium.click_by_xpath(xpath= '//button[@data-uxi-widget-type="paginationPageButton"]')
        titles, urls = scrape_jobs(selenium=selenium)
    
    job_titles.append(titles)
    job_urls.append(urls)
    
    return job_titles, job_urls

def scrape_workday_jobs(URL):
    selenium = Selenium(url=URL)
    selenium.click_by_xpath(xpath='//button[@data-automation-id="legalNoticeDeclineButton"]')
    job_titles = []
    job_urls = []

    titles, urls = scrape_jobs(selenium)
    job_titles.extend(titles)
    job_urls.extend(urls)

    titles, urls = next_page(selenium)

    job_titles.extend(titles)
    job_urls.extend(urls)

    df = pd.DataFrame(data={'job_title': job_titles, 'job_url': job_urls})
    df.to_csv('workday_jobs.csv', index=False)
    
    selenium.quit_driver()

if __name__ == '__main__':
    URL = 'https://db.wd3.myworkdayjobs.com/en-US/DBWebsite/details/Divisional-Risk-and-Control-Analyst--d-m-w-_R0263735?q=data+science&Country=dcc5b7608d8644b3a93716604e78e995&workerSubType=645e861bc53a015625eefdaefb3a1909'
    scrape_workday_jobs(URL)
