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


def exit_with_error(msg, code=1):
    sys.stderr.write(msg + '\n')
    sys.exit(code)


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
    exit_with_error(msg)


def resolved_url_from_url(relative_url, source_url):
    url_a = urlparse(source_url)
    return '%s://%s%s' % (
        url_a.scheme,
        url_a.netloc,
        relative_url
    )


def resolved_url_from_response(url, response, error_msg="URL not found"):
    if url is None:
        exit_with_error(error_msg)
    return resolved_url_from_url(url, response.url)


def start_active_players(league_id, team_id, username, password):
    session = requests.Session()

    # Attempt to load team page
    url = '%s/%s/%s/' % (YAHOO_URL, league_id, team_id)
    headers = {
        'user-agent': DESKTOP_USER_AGENT
    }
    response = session.get(url, headers=headers)

    # Login at redirected login page
    soup = BeautifulSoup(response.text)
    url = resolved_url_from_response(
        soup.find(id='mbr-login-form')['action'],
        response,
        'Error: Login link not found'
    )
    inputs = soup.find(id='hiddens').findAll('input')
    fields = {input['name']: input['value'] for input in inputs}
    fields['username'] = username
    fields['passwd'] = password
    response = session.post(url, data=fields, headers=headers)

    if response.url == url:
        exit_with_error('Error: Login failed')

    # Now on team page, press "Start Active Players" button
    soup = BeautifulSoup(response.text)
    url = resolved_url_from_response(
        soup.find('a', href=True, text='Start Active Players')['href'],
        response,
        'Error: "Start Active Players" button not found'
    )
    response = session.get(url, headers=headers)

    if 200 <= response.status_code < 300:
        print('Started active players (though others may be on bench)!')
    else:
        exit_with_error('Error: Failed to start active players')


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
