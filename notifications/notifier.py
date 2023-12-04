from __future__ import annotations
from win11toast import toast
import webbrowser
from helpers import constants

def open_urls(args: str, urls: list[str]) -> None:
    if type(urls) == list:
        for url in urls:
            webbrowser.open(url)
    else:
        webbrowser.open(urls)

def notify_application_success(job_args) -> None:
    toast(title='Application Sent Successfully!',
          body=f'{job_args["POSITION"]} at {job_args["COMPANY_NAME"]}',
          scenario='incomingCall')

def notify_application_failure(job_args) -> None:
    toast(title='Application Failed, Check Browser!',
          body=f'{job_args["POSITION"]} at {job_args["COMPANY_NAME"]}',
          scenario='incomingCall')


def notify_jobs(urls: list[str]) -> None:
    toast(title='Relevant Jobs Found!', 
          body='Click to open jobs',
          on_click= lambda args: open_urls(args, urls),
          scenario='incomingCall')