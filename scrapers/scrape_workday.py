from helpers.selenium_helper import Selenium

URL = 'https://db.wd3.myworkdayjobs.com/en-US/DBWebsite/details/Divisional-Risk-and-Control-Analyst--d-m-w-_R0263735?q=data+science&Country=dcc5b7608d8644b3a93716604e78e995&workerSubType=645e861bc53a015625eefdaefb3a1909'

selenium = Selenium(url=URL)

table = selenium.element_by_xpath(xpath='//section[@data-automation-id="jobResults"]')
rows = selenium.elements_by_class(class_='css-1q2dra3', selected_element=table)
len(rows)