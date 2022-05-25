import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(pos,loc):
    template_url = 'https://jp.indeed.com/jobs?q={}&l={}'
    pos = pos.replace(' ', '+')
    loc = loc.replace(' ', '+')
    url = template_url.format(pos, loc)
    return url

url = get_url('Full-stack Developer', '東京都')
print(url)