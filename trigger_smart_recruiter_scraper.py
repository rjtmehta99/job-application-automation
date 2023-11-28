import notifier
import scrape_smart_recruiter
import helper
import constants

url = 'https://jobs.smartrecruiters.com/?keyword=data%20scientist'
jobs_df = scrape_smart_recruiter.scrape(url)
unnotified_jobs = jobs_df[jobs_df['notified'] == False]['url'].to_list()

if len(unnotified_jobs) > 0:
    notifier.notify(urls=unnotified_jobs)
    jobs_df.loc[jobs_df['notified'] == False, 'notified'] = True
    helper.save_csv(jobs_df, constants.SMART_RECRUITERS_JOBS)

else:
    print('No new jobs found')
