"""
Start active players for a range of dates
"""

import os
import requests
import sys
import yahooscraper as ys

from datetime import datetime, date, timedelta
from urllib.parse import urljoin
from utils import *


# Command-line args
DATE_LIMIT = date.today() + timedelta(days=365)
NUM_DAYS_DEFAULT = 1
NUM_DAYS_MAX = 100
OPTIONAL_ARGS.extend([
    '<date (default: today, max: %s)>' % DATE_LIMIT.strftime('%Y-%m-%d'),
    '<num_days (default: %d, max: %d)>' % (NUM_DAYS_DEFAULT, NUM_DAYS_MAX)
])

# Error messages
START_PLAYERS_ERROR_MSG = 'Failed to start players'


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
    num_args_incorrect = len(sys.argv) not in required_num_args()
    if credentials_missing or num_args_incorrect:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]
    start_date = date_from_argv(3, DATE_LIMIT)
    num_days = int_from_argv(3 if start_date is None else 4, NUM_DAYS_MAX)
    if start_date is None:
        start_date = date.today()
    if num_days is None:
        num_days = NUM_DAYS_DEFAULT

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
