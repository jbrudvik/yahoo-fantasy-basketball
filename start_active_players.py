"""
Start active players for the week
"""

import requests
import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from urllib.parse import urlparse


USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

DATE_LIMIT = date.today() + timedelta(days=365)
NUM_DAYS_MAX = 100

# Command-line arguments
REQUIRED_ARGS = [
    '<league_id>',
    '<team_id>'
]
OPTIONAL_ARGS = [
    '<date (default: today, max: %s)>' % DATE_LIMIT.strftime('%Y-%m-%d'),
    '<num_days (default: 1, max: %d)>' % NUM_DAYS_MAX
]

MIN_ARGS = len(REQUIRED_ARGS) + 1
MAX_ARGS = MIN_ARGS + len(OPTIONAL_ARGS)
REQUIRED_NUM_ARGS = range(MIN_ARGS, MAX_ARGS + 1)

YAHOO_URL = 'http://basketball.fantasysports.yahoo.com/nba'
DESKTOP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'
YAHOO_HEADERS = {
    'user-agent': DESKTOP_USER_AGENT
}

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


def team_url(league_id, team_id, start_date=None):
    url = '%s/%s/%s/' % (YAHOO_URL, league_id, team_id)
    if start_date is not None:
        url += 'team?&date=%s' % start_date
    return url


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


def login_url(response):
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
    return url


def login_post_data(response, username, password):
    soup = BeautifulSoup(response.text)
    inputs = soup.find(id='hiddens').findAll('input')
    post_data = {input['name']: input['value'] for input in inputs}
    post_data['username'] = username
    post_data['passwd'] = password
    return post_data


def start_active_players_button(response):
    soup = BeautifulSoup(response.text)
    url_path = attr_from_element_or_exit(
        soup.find('a', href=True, text='Start Active Players'),
        'href',
        LOGIN_ERROR_MSG
    )
    return resolved_url_from_response(
        url_path,
        response,
        'Error: "Start Active Players" button not found'
    )


def show_team_info(response):
    soup = BeautifulSoup(response.text)
    league, team = soup.find('title').text.split(' | ')[0].split(' - ')
    print('%s - %s:\n' % (league, team))


def show_start_active_players_results(response):
    if not (200 <= response.status_code < 300):
        exit_with_error(
            '- %s: Failed to start active players' % formatted_date
        )

    soup = BeautifulSoup(response.text)

    # Parse date
    page_date = attr_from_element_or_exit(
        soup.find('input', attrs={'name': 'date'}),
        'value',
        LOGIN_ERROR_MSG
    )
    parsed_date = datetime.strptime(page_date, '%Y-%m-%d')
    formatted_date = parsed_date.strftime('%a, %b %d, %Y')

    # Parse bench
    bench = soup.find_all('tr', class_='bench')
    bench_bios = [p.find('div', class_='ysf-player-name') for p in bench]
    names = [p.find('a').text for p in bench_bios]
    details = [p.find('span').text for p in bench_bios]
    opponents = [p.find_all('td', recursive=False)[3].text for p in bench]
    players = [{'name': n, 'details': d, 'opponent': o}
               for (n, d, o) in zip(names, details, opponents)]
    alternates = [p for p in players if len(p['opponent']) > 0]

    # Show results
    print('- %s: Started active players' % formatted_date)
    for player in alternates:
        print('    - Alternate: %s (%s) [%s]' % (
            player['name'],
            player['details'],
            player['opponent']
        ))


def login(league_id, team_id, username, password):
    # Create session to maintain logged-in status
    session = requests.Session()

    # Attempt to load team page
    response = session.get(team_url(league_id, team_id),
                           headers=YAHOO_HEADERS)

    # Login at redirected login page
    response = session.post(login_url(response),
                            data=login_post_data(response, username, password),
                            headers=YAHOO_HEADERS)

    # Show league, team info
    show_team_info(response)

    return session


def start_active_players(session, league_id, team_id,
                         start_date=None, num_days=1):
    # Load team page
    response = session.get(team_url(league_id, team_id, start_date),
                           headers=YAHOO_HEADERS)

    # On team page, press "Start Active Players button"
    response = session.get(start_active_players_button(response),
                           headers=YAHOO_HEADERS)

    # Show results of starting active players
    show_start_active_players_results(response)


def parse_date(i):
    if len(sys.argv) > i:
        try:
            input_date = datetime.strptime(sys.argv[i], '%Y-%m-%d').date()
            today = date.today()
            return input_date if today <= input_date <= DATE_LIMIT else None
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
    start_date = parse_date(3)  # TODO: Don't use `date` here
    num_days = parse_num_days(3 if start_date is None else 4)

    try:
        session = login(league_id, team_id, username, password)
        start_active_players(session, league_id, team_id, start_date, num_days)
    except:
        exit_with_error(UNKNOWN_ERROR_MSG)


if __name__ == '__main__':
    main()
