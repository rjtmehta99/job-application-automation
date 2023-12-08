from notifications import notifier
from scrapers import scrape_smart_recruiter
from helpers import helper, constants

jobs_df = scrape_smart_recruiter.scrape(constants.SMART_RECRUITERS_URLS)
unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()

if len(unnotified_jobs) > 0:
    notifier.notify_jobs(urls=unnotified_jobs)
    jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
    helper.save_csv(jobs_df, constants.SMART_RECRUITERS_JOBS)

else:
    print('No new jobs found')