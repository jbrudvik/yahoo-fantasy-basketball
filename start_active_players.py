"""
Start active players for the week
"""

import moment
import requests
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse


USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

NUM_DAYS_MAX = 100

# Command-line arguments
REQUIRED_ARGS = [
    '<league_id>',
    '<team_id>'
]
OPTIONAL_ARGS = [
    '<date (default: today, format: YYYY-MM-DD)>',
    '<num_days (default: 1, max: %d)>' % NUM_DAYS_MAX
]

MIN_ARGS = len(REQUIRED_ARGS) + 1
MAX_ARGS = MIN_ARGS + len(OPTIONAL_ARGS)
REQUIRED_NUM_ARGS = range(MIN_ARGS, MAX_ARGS + 1)

YAHOO_URL = 'http://basketball.fantasysports.yahoo.com/nba'
DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'

LOGIN_ERROR_MSG = 'Error: Login failed'
UNKNOWN_ERROR_MSG = 'Failed to start players'


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


def start_active_players(league_id, team_id, username, password,
                         date=None, num_days=1):
    session = requests.Session()

    # Attempt to load team page
    url = '%s/%s/%s/' % (YAHOO_URL, league_id, team_id)

    if date is not None:
        url += 'team?&date=%s' % date

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
    league, team = soup.find('title').text.split(' | ')[0].split(' - ')
    print('%s - %s:' % (league, team))
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

    # Show results "Start Active Players"
    soup = BeautifulSoup(response.text)
    date = attr_from_element_or_exit(
        soup.find('input', attrs={'name': 'date'}),
        'value',
        LOGIN_ERROR_MSG
    )
    formatted_date = moment.date(date).format('ddd, MMM DD, YYYY')

    bench = soup.find_all('tr', class_='bench')
    bench_bios = [p.find('div', class_='ysf-player-name') for p in bench]
    names = [p.find('a').text for p in bench_bios]
    details = [p.find('span').text for p in bench_bios]
    opponents = [p.find_all('td', recursive=False)[3].text for p in bench]
    players = [{'name': n, 'details': d, 'opponent': o}
               for (n, d, o) in zip(names, details, opponents)]
    alternates = [p for p in players if len(p['opponent']) > 0]

    if 200 <= response.status_code < 300:
        print(
            '- %s: Started active players' %
            formatted_date
        )
        for player in alternates:
            print('    - Alternate: %s (%s) [%s]' % (
                player['name'],
                player['details'],
                player['opponent']
            ))
    else:
        exit_with_error(
            '- %s: Failed to start active players' % formatted_date
        )


def parse_date(i):
    if len(sys.argv) > i:
        try:
            return moment.date(sys.argv[i]).format('YYYY-MM-DD')
        except:
            return None
    else:
        return None


def parse_num_days(i):
    if len(sys.argv) > i:
        try:
            return int(sys.argv[i])
        except:
            usage()
        if num_days > NUM_DAYS_MAX:
            usage()
    return None


def main():
    username = os.getenv(USERNAME_ENV)
    password = os.getenv(PASSWORD_ENV)

    missing_credentials = username is None or password is None
    incorrect_num_args = len(sys.argv) not in REQUIRED_NUM_ARGS

    if missing_credentials or incorrect_num_args:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]
    date = parse_date(3)
    num_days = parse_num_days(3 if date is None else 4)

    try:
        start_active_players(league_id, team_id, username, password,
                             date, num_days)
    except:
        exit_with_error(UNKNOWN_ERROR_MSG)


if __name__ == '__main__':
    main()
