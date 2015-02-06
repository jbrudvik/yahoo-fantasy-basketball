"""
Project results of the current matchup
"""

import requests
import os
import sys
import yahooscraper as ys
from urllib.parse import urljoin


# Environment variables
USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

# Command-line args
REQUIRED_ARGS = (
    '<league_id>',
    '<team_id>'
)
OPTIONAL_ARGS = ()
MIN_ARGS = len(REQUIRED_ARGS) + 1
MAX_ARGS = MIN_ARGS + len(OPTIONAL_ARGS)
REQUIRED_NUM_ARGS = range(MIN_ARGS, MAX_ARGS + 1)

# Error messages
LOGIN_ERROR_MSG = 'Failed to log in'


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


def main():
    username = os.getenv(USERNAME_ENV)
    password = os.getenv(PASSWORD_ENV)

    credentials_missing = username is None or password is None
    num_args_incorrect = len(sys.argv) not in REQUIRED_NUM_ARGS
    if credentials_missing or num_args_incorrect:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]

    # Create session for maintaining logged-in status, necessary headers
    session = requests.Session()
    session.headers.update(ys.login.headers())

    try:
        login(session, league_id, team_id, username, password)
    except:
        sys.exit(LOGIN_ERROR_MSG)

    try:
        output_team_info(session, league_id, team_id)
    except:
        sys.exit(START_PLAYERS_ERROR_MSG)


if __name__ == '__main__':
    main()
