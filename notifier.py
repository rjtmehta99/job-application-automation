from __future__ import annotations
from win11toast import toast
import webbrowser
import constants

def open_urls(args, urls):
    if type(urls) == list:
        for url in urls:
            webbrowser.open(url)
    else:
        webbrowser.open(urls)


def notify(urls: str|list[str]) -> None:
    print('here')
    toast(title='Relevant Jobs Found!', 
          body='Click to open jobs',
          on_click= lambda args: open_urls(args, urls),
          duration='long')