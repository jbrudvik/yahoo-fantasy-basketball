from urllib.parse import urljoin
import sys
import yahooscraper as ys


# Environment variables
USERNAME_ENV = 'YAHOO_USERNAME'
PASSWORD_ENV = 'YAHOO_PASSWORD'

# Command-line args
REQUIRED_ARGS = [
    '<league_id>',
    '<team_id>'
]
OPTIONAL_ARGS = []

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


def required_num_args():
    min_args = len(REQUIRED_ARGS) + 1
    max_args = min_args + len(OPTIONAL_ARGS)
    return range(min_args, max_args + 1)


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
