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

#Function to scrape jobs 
def get_job_cards(job_card):
    job_listing_atag = job_card.h2.a
    job_listing_span_tag = job_card.h2.a.span

    job_title = job_listing_span_tag.get('title')

    job_listing_url = 'http://jp.indeed.com' + job_listing_atag.get('href')

    company_name = job_card.find('span', 'companyName').text

    job_location = job_card.find('div', 'companyLocation').text

    job_snippet = job_card.find('div', 'job-snippet').text.replace('\n', ' ')

    todays_date = datetime.today().strftime('%Y-%m-%d')

    #Due to nested tags, dive a bit deeper and exclude everything but the post date
    job_listing_post_date = None
    for posting_date in job_card.find('span', 'date'):
        if not job_card.get('date'):
            job_listing_post_date = "Posted: " + posting_date.text

    #Error handling for whether or not a salary is posted in the job listing.
    try:
        job_salary = job_card.find('div', 'salary-snippet').text
    except AttributeError:
        job_salary = ''

    record = (job_title, company_name, job_location, job_listing_post_date, todays_date, job_snippet, job_salary, job_listing_url)

    return record

#List to store jobs we have scraped
found_jobs = []

for job_card in job_cards:
    found_job = get_job_cards(job_card) 
    found_jobs.append(found_job)
