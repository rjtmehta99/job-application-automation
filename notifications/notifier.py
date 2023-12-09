from __future__ import annotations
from win11toast import toast
import webbrowser
from helpers import constants

def open_urls(args: str, urls: list[str]|str) -> None:
    if type(urls) == list:
        for url in urls:
            webbrowser.open(url)
    else:
        webbrowser.open(urls)


def notify_application_success(job_args: dict[str], urls: str) -> None:
    toast(title='Application Sent Successfully!',
          body=f'{job_args["POSITION"]} at {job_args["COMPANY_NAME"]}.\nClick to view application.',
          on_click= lambda args: open_urls(args, urls),
          scenario='incomingCall')


def notify_application_failure(job_args: dict[str]) -> None:
    toast(title='Application Failed, Check Browser!',
          body=f'{job_args["POSITION"]} at {job_args["COMPANY_NAME"]}',
          scenario='incomingCall')


def notify_jobs(company: str, urls: list[str]) -> None:
    toast(title=f'Relevant Jobs Found at {company}!', 
          body='Click to open jobs',
          on_click= lambda args: open_urls(args, urls),
          scenario='incomingCall')