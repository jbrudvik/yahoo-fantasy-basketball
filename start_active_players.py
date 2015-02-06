"""
Start active players for a range of dates
"""

import requests
import os
import sys
from datetime import datetime, date, timedelta
import yahooscraper as ys
from urllib.parse import urljoin


# Environment variables
USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

# Command-line args
DATE_LIMIT = date.today() + timedelta(days=365)
NUM_DAYS_MAX = 100
REQUIRED_ARGS = (
    '<league_id>',
    '<team_id>'
)
OPTIONAL_ARGS = (
    '<date (default: today, max: %s)>' % DATE_LIMIT.strftime('%Y-%m-%d'),
    '<num_days (default: 1, max: %d)>' % NUM_DAYS_MAX
)
MIN_ARGS = len(REQUIRED_ARGS) + 1
MAX_ARGS = MIN_ARGS + len(OPTIONAL_ARGS)
REQUIRED_NUM_ARGS = range(MIN_ARGS, MAX_ARGS + 1)

# Error messages
LOGIN_ERROR_MSG = 'Failed to log in'
START_PLAYERS_ERROR_MSG = 'Failed to start players'


def usage():
    """
    Print usage and exit
    """
    msg_lines = [
        ' '.join((
            'Usage: python',
            sys.argv[0],
            ' '.join(REQUIRED_ARGS),
            ' '.join(OPTIONAL_ARGS))),
        'Environment variables %s and %s must also be set' % (
            USERNAME_ENV,
            PASSWORD_ENV)]
    sys.exit('\n\n'.join(msg_lines))


def date_from_argv(i):
    """
    Parse date from command-line args
    """
    if len(sys.argv) > i:
        try:
            input_date = datetime.strptime(sys.argv[i], '%Y-%m-%d').date()
            today = date.today()
            return input_date if today <= input_date <= DATE_LIMIT else None
        except:
            return None
    else:
        return None


def num_days_from_argv(i):
    """
    Parse num_days from command-line args
    """
    if len(sys.argv) > i:
        try:
            return int(sys.argv[i])
        except:
            usage()
        if num_days > NUM_DAYS_MAX:
            usage()
    return 1


def login(session, league_id, team_id, username, password):
    """
    Log in to Yahoo
    """
    response = session.get(ys.login.url())
    login_path = ys.login.path(response.text)
    login_url = urljoin(response.url, login_path)
    login_post_data = ys.login.post_data(response.text, username, password)
    session.post(login_url, data=login_post_data)


def output_team_info(session, league_id, team_id):
    """
    Output team name and league
    """
    response = session.get(ys.fantasy.team.url('nba', league_id, team_id))
    league = ys.fantasy.team.league(response.text)
    team = ys.fantasy.team.team(response.text)
    print('%s - %s:\n' % (league, team))


def start_active_players(session, league_id, team_id, start_date=None):
    """
    Start active players and output results
    """
    # Load team page
    team_url = ys.fantasy.team.url('nba', league_id, team_id, start_date)
    response = session.get(team_url)

    # Press "Start Active Players" button
    start_path = ys.fantasy.team.start_active_players_path(response.text)
    start_url = urljoin(response.url, start_path)
    response = session.get(start_url)

    # If unsuccessful, report failure
    formatted_date = ys.fantasy.team.date(response.text)
    if not (200 <= response.status_code < 300):
        print('- %s: Failed to start active players' % formatted_date)

    # Report success and highlight available bench players
    print('- %s: Started active players' % formatted_date)
    alternates = ys.fantasy.team.alternates(response.text)
    for player in alternates:
        print('    - Alternate: %s (%s) [%s]' % (
            player['name'],
            player['details'],
            player['opponent']))


def main():
    username = os.getenv(USERNAME_ENV)
    password = os.getenv(PASSWORD_ENV)

    credentials_missing = username is None or password is None
    num_args_incorrect = len(sys.argv) not in REQUIRED_NUM_ARGS
    if credentials_missing or num_args_incorrect:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]
    start_date = date_from_argv(3)
    num_days = num_days_from_argv(3 if start_date is None else 4)
    if start_date is None:
        start_date = date.today()

    # Create session for maintaining logged-in status, necessary headers
    session = requests.Session()
    session.headers.update(ys.login.headers())

    try:
        login(session, league_id, team_id, username, password)
    except:
        sys.exit(LOGIN_ERROR_MSG)

    try:
        output_team_info(session, league_id, team_id)
        for _ in range(num_days):
            start_active_players(session, league_id, team_id, start_date)
            start_date = start_date + timedelta(days=1)
    except:
        sys.exit(START_PLAYERS_ERROR_MSG)


if __name__ == '__main__':
    main()
