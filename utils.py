import sys
import yahooscraper as ys

from datetime import datetime, date
from urllib.parse import urljoin


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


def parsed_and_bounded_arg(i, max, min, parse):
    """
    Returns parsed and bounded arg from argv.

    The `parse` parameter is a single-argument function which is called with
    the arg. The output of this function is only returned if it is between
    min and max.

    If parse fails or arg is not within bounds, None is returned.
    """
    if len(sys.argv) > i:
        try:
            parsed_arg = parse(sys.argv[i])
            return parsed_arg if min <= parsed_arg <= max else None
        except:
            return None
    else:
        return None


def date_from_argv(i, max, min=date.today()):
    return parsed_and_bounded_arg(
        i, max, min,
        lambda arg: datetime.strptime(arg, '%Y-%m-%d').date())


def int_from_argv(i, max, min=1):
    return parsed_and_bounded_arg(i, max, min, lambda arg: int(arg))


def output_team_info(session, league_id, team_id):
    """
    Output team name and league
    """
    response = session.get(ys.fantasy.team.url('nba', league_id, team_id))
    league = ys.fantasy.team.league(response.text)
    team = ys.fantasy.team.team(response.text)
    print('%s - %s:\n' % (league, team))
