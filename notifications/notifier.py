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


def notify(urls: list[str]) -> None:
    toast(title='Relevant Jobs Found!', 
          body='Click to open jobs',
          on_click= lambda args: open_urls(args, urls),
          duration='long')