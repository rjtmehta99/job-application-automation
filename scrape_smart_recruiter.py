# TODO: parameterize location and company names.
# Apply via LinkedIn automatically, stop at other questions.
import constants
import pandas as pd
import selenium_helper

def scrape(url: str) -> pd.DataFrame:
    selenium = selenium_helper.Selenium(url=url, headless=True)
    selenium.click_by_id(id_='onetrust-accept-btn-handler')

    urls = []
    positions = []
    companies = []
    locations = []

    table = selenium.element_by_class(class_='jobs-list')
    rows = selenium.elements_by_class(class_='jobs-item', selected_element=table)

    for row in rows:
        job_details = selenium.element_by_tag(tag='a', selected_element=row)
        url = job_details.get_attribute('href')
        job_details = job_details.text.split('\n')
        position = job_details[0]
        company = job_details[1]
        location = job_details[2]
        #if company.lower.__contains__('gmbh') or location.lower.__contains__('germany')
        if 'gmbh' in company.lower() or ('germany' or 'deutschland') in location.lower():
            urls.append(url)
            positions.append(position)
            companies.append(company)
            locations.append(location)
    print(f'{len(urls)} relevant jobs found.', end='\n-----\n')
    selenium.quit_driver()
    
    try:
        previous_df = pd.read_csv(constants.SMART_RECRUITERS_JOBS)
    except FileNotFoundError:
        previous_df = pd.DataFrame(columns=['position', 'company', 'location', 'url', 'notified'])

    current_df = pd.DataFrame(data={'position': positions, 'company': companies, 
                                    'location': locations, 'url': urls})
    current_df['notified'] = False
    merged_df = pd.concat([current_df, previous_df])
    merged_df = merged_df.drop_duplicates(subset=['url'], keep='last').reset_index(drop=True)
    merged_df.to_csv(constants.SMART_RECRUITERS_JOBS, index=False)
    return merged_df

if __name__ == '__main__':
    url = 'https://jobs.smartrecruiters.com/?keyword=data%20scientist'
    scrape(url=url)
