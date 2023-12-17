import yaml
import requests
import pandas as pd
from jinja2 import Template
from bs4 import BeautifulSoup
from helpers import constants
from notifications import notifier
import logging
logging.basicConfig(level=logging.WARN)

class ScraperHelper:
    def __init__(self, company_name: str):
        self.company_name = company_name
        logging.warning(f' Scraping {self.company_name} jobs')
    
    def get_html_body(self, rendered_url: str) -> BeautifulSoup:
        response = requests.request("GET", rendered_url)
        body = BeautifulSoup(response.content, 'html.parser')
        return body

    def load_company_info(self):
        # From the company master data yaml, returns all data for the company_name
        with open(constants.COMPANY_MASTER_DATA, 'r') as file:
            master_data = yaml.safe_load(file)
        company_data = master_data.get(self.company_name)
        return company_data

    def render_url(self, url, **template_args):
        # Renders the specified params into the URL. 
        # These params can be keywords, page number, job count etc. 
        template = Template(url)
        rendered_url = template.render(**template_args)
        return rendered_url

    def notify_new_jobs(self, jobs_df: pd.DataFrame, csv_path: str) -> None:
        # Notifies user about new and unnotified jobs 
        # Also saves event info about jobs that were notified. 
        unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()        
        if len(unnotified_jobs) > 0:
            notifier.notify_jobs(company=self.company_name, urls=unnotified_jobs)
            jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
            jobs_df.to_csv(csv_path, index=False)
