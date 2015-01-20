"""
Start active players for the week
"""

import requests
from bs4 import BeautifulSoup

TEAM_URL = 'http://basketball.fantasysports.yahoo.com/nba/178276/6/'

DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'

headers = {
    'user-agent': DESKTOP_USER_AGENT
}
response = requests.get(TEAM_URL, headers=headers)
soup = BeautifulSoup(response.text)
inputs = soup.find(id='hiddens').findAll('input')
fields = {input['name']: input['value'] for input in inputs}
print(fields)
