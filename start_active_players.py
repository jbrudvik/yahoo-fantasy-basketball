"""
Start active players for the week
"""

import requests
import os
import sys
from bs4 import BeautifulSoup


def usage():
    sys.stderr.write('Usage: YAHOO_USERNAME=<username> YAHOO_PASSWORD=<password> %s\n' % sys.argv[0])
    sys.exit(1)


def start_active_players(username, password):
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


def main():
    username = os.getenv('YAHOO_USERNAME')
    password = os.getenv('YAHOO_PASSWORD')

    if username is None or password is None:
        usage()

    start_active_players(username, password)


if __name__ == '__main__':
    main()
