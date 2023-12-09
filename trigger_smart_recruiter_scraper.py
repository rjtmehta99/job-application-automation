from notifications import notifier
from scrapers import scrape_smart_recruiter
from helpers import csv_helper, constants

company = 'Smart Recruiters'
jobs_df = scrape_smart_recruiter.scrape(constants.SMART_RECRUITERS_URLS)
unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()

if len(unnotified_jobs) > 0:
    notifier.notify_jobs(company=company, urls=unnotified_jobs)
    jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
    csv_helper(csv_path=constants.SMART_RECRUITERS_JOBS).save_df_to_csv(jobs_df)
    
else:
    print('No new jobs found')