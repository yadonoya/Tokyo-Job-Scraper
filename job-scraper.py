import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


#Setup our URL to begin our webscrape from Indeed JP
def get_url(pos,loc):
    template_url = 'https://jp.indeed.com/jobs?q={}&l={}'
    pos = pos.replace(' ', '+')
    loc = loc.replace(' ', '+')
    url = template_url.format(pos, loc)
    return url

#Input parameters for the job title and location we would like to search for
url = get_url('Full-stack Developer', '東京都')


# Extract HTML
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#This is going to use the soup object to find all elements that have a div tag, and the given class
job_cards = soup.find_all('div', 'slider_item')

# Single record/card 

job_card = job_cards[0]

job_listing_atag = job_card.h2.a
job_listing_span_tag = job_card.h2.a.span

job_title = job_listing_span_tag.get('title')

job_listing_url = 'http://jp.indeed.com' + job_listing_atag.get('href')

company_name = job_card.find('span', 'companyName').text

job_location = job_card.find('div', 'companyLocation').text

job_snippet = job_card.find('div', 'job-snippet').text.replace('\n', ' ')