import csv
from datetime import datetime
import requests
from flask import Flask, render_template
from time import sleep
from random import randint
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def find_jobs():
    def get_url(pos,loc):
        template_url = 'https://jp.indeed.com/jobs?q={}&l={}'
        pos = pos.replace(' ', '+')
        loc = loc.replace(' ', '+')
        url = template_url.format(pos, loc)
        return url

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
                job_listing_post_date = posting_date.text

        #Error handling for whether or not a salary is posted in the job listing.
        try:
            job_salary = job_card.find('div', 'salary-snippet').text
        except AttributeError:
            job_salary = ''

        record = (job_title, company_name, job_location, job_salary, job_listing_post_date, todays_date, job_snippet, job_listing_url)

        return record

    def main_function(job_position):
        records = []
        url = get_url(job_position, '東京都') #Temporarily hard-coded Tokyo as our default search location

        while True: 
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', 'slider_item')

                for job_card in job_cards:
                    record = get_job_cards(job_card)
                    records.append(record)

                try:
                    url = 'http://jp.indeed.com' + soup.find('a', {'aria-label': '次へ'}).get('href')
                    delay = randint(1, 10)
                    sleep(delay)
                except AttributeError:
                    break

        return records
        # with open('results.csv', 'w', newline='', encoding='utf-8') as found_jobs:
        #     writer = csv.writer(found_jobs)
        #     writer.writerow(['Job Title', 'Company', 'Location', 'Salary', 'Posting Date', 'Extract Date', 'Summary', 'Job Url']) #This order has to match our record tuple listed above
        #     writer.writerows(records)

    scraped_listings = main_function('Full-Stack Developer')

    return render_template('index.html', scraped_listings=scraped_listings)