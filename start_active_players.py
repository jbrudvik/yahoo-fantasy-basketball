"""
Start active players for the week
"""

import requests
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse


USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

DEFAULT_NUM_DAYS = 1
NUM_DAYS_MAX = 100

# Command-line arguments
REQUIRED_ARGS = [
    '<league_id>',
    '<team_id>'
]
OPTIONAL_ARGS = [
    '<num_days (default: %d, max: %d)>' % (DEFAULT_NUM_DAYS, NUM_DAYS_MAX)
]

MIN_ARGS = len(REQUIRED_ARGS) + 1
MAX_ARGS = MIN_ARGS + len(OPTIONAL_ARGS)
REQUIRED_NUM_ARGS = range(MIN_ARGS, MAX_ARGS + 1)

YAHOO_URL = 'http://basketball.fantasysports.yahoo.com/nba'
DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'

LOGIN_ERROR_MSG = 'Error: Login failed'


def exit_with_error(msg, code=1):
    sys.stderr.write(msg + '\n')
    sys.exit(code)


def usage():
    msg_lines = [
        ' '.join((
            'Usage:',
            sys.argv[0],
            ' '.join(REQUIRED_ARGS),
            ' '.join(OPTIONAL_ARGS)
        )),
        'Environment variables %s and %s must also be set' % (
            USERNAME_ENV,
            PASSWORD_ENV
        )
    ]
    exit_with_error('\n\n'.join(msg_lines))


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


def attr_from_element_or_exit(element, attr, error_msg="Attribute not found"):
    try:
        return element[attr]
    except:
        exit_with_error(error_msg)


def start_active_players(league_id, team_id, username, password, num_days):
    session = requests.Session()

    # Attempt to load team page
    url = '%s/%s/%s/' % (YAHOO_URL, league_id, team_id)
    headers = {
        'user-agent': DESKTOP_USER_AGENT
    }
    response = session.get(url, headers=headers)

    # Login at redirected login page
    soup = BeautifulSoup(response.text)
    url_path = attr_from_element_or_exit(
        soup.find(id='mbr-login-form'),
        'action',
        LOGIN_ERROR_MSG + ': Unexpected login page'
    )
    url = resolved_url_from_response(
        url_path,
        response,
        LOGIN_ERROR_MSG + ': Login link not found'
    )
    inputs = soup.find(id='hiddens').findAll('input')
    fields = {input['name']: input['value'] for input in inputs}
    fields['username'] = username
    fields['passwd'] = password
    response = session.post(url, data=fields, headers=headers)

    # Now on team page, press "Start Active Players" button
    soup = BeautifulSoup(response.text)
    url_path = attr_from_element_or_exit(
        soup.find('a', href=True, text='Start Active Players'),
        'href',
        LOGIN_ERROR_MSG
    )
    url = resolved_url_from_response(
        url_path,
        response,
        'Error: "Start Active Players" button not found'
    )

    response = session.get(url, headers=headers)

    if 200 <= response.status_code < 300:
        print('Started active players (though others may be on bench)!')
    else:
        exit_with_error('Error: Failed to start active players')


def main():
    username = os.getenv(USERNAME_ENV)
    password = os.getenv(PASSWORD_ENV)

    missing_credentials = username is None or password is None
    incorrect_num_args = len(sys.argv) not in REQUIRED_NUM_ARGS

    if missing_credentials or incorrect_num_args:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]
    try:
        num_days = int(sys.argv[3] if len(sys.argv) > 3 else DEFAULT_NUM_DAYS)
    except:
        usage()
    if num_days > NUM_DAYS_MAX:
        usage()

    start_active_players(
        league_id,
        team_id,
        username,
        password,
        num_days
    )


if __name__ == '__main__':
    main()
