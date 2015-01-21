"""
Start active players for the week
"""

import requests
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse


YAHOO_URL = 'http://basketball.fantasysports.yahoo.com/nba'
DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'


def usage():
    username = 'YAHOO_USERNAME=<username>'
    password = 'YAHOO_PASSWORD=<password>'
    league_id = '<league_id>'
    team_id = '<team_id>'
    msg = ' '.join((
        'Usage:',
        username,
        password,
        sys.argv[0],
        league_id,
        team_id
    ))
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def start_active_players(league_id, team_id, username, password):
    team_url = '%s/%s/%s/' % (YAHOO_URL, league_id, team_id)
    headers = {
        'user-agent': DESKTOP_USER_AGENT
    }
    session = requests.Session()
    response = session.get(team_url, headers=headers)
    soup = BeautifulSoup(response.text)

    login_url = urlparse(response.url)
    login_action = soup.find(id='mbr-login-form')['action']
    login_form_url = '%s://%s%s' % (
        login_url.scheme,
        login_url.netloc,
        login_action
    )

    inputs = soup.find(id='hiddens').findAll('input')
    fields = {input['name']: input['value'] for input in inputs}
    fields['username'] = username
    fields['passwd'] = password

    response = session.post(login_form_url, data=fields, headers=headers)
    print(response.text)


def main():
    username = os.getenv('YAHOO_USERNAME')
    password = os.getenv('YAHOO_PASSWORD')

    if username is None or password is None or len(sys.argv) != 3:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]

    start_active_players(league_id, team_id, username, password)


if __name__ == '__main__':
    main()
