from notifications import notifier
from scrapers import scrape_munichre
from helpers import constants

company = 'Munich Re'
jobs_df = scrape_munichre.scrape()
unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()

if len(unnotified_jobs) > 0:
    notifier.notify_jobs(company=company, urls=unnotified_jobs)
    jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
    jobs_df.to_csv(constants.MUNICHRE_CSV, index=False)
    
else:
    print('No new jobs found')