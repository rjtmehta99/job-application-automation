import yaml
from helpers.constants import GREENHOUSE_DATA
from scrapers.scrape_greenhouse import scrape

with open(GREENHOUSE_DATA, 'r') as file:
    gh_data = yaml.safe_load(file)

for company_data in gh_data['greenhouse_companies']:
    scrape(company_data=company_data)
