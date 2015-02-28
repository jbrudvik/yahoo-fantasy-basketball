"""
Project results of the current matchup
"""

import os
import requests
import sys
import yahooscraper as ys

from urllib.parse import urljoin
from utils import *


def main():
    username = os.getenv(USERNAME_ENV)
    password = os.getenv(PASSWORD_ENV)

    credentials_missing = username is None or password is None
    num_args_incorrect = len(sys.argv) not in required_num_args()
    if credentials_missing or num_args_incorrect:
        usage()

    league_id = sys.argv[1]
    team_id = sys.argv[2]

    # Create session for maintaining logged-in status, necessary headers
    session = requests.Session()
    session.headers.update(ys.login.headers())

    try:
        login(session, username, password)
    except:
        sys.exit(LOGIN_ERROR_MSG)

    try:
        output_team_info(session, league_id, team_id)
    except:
        sys.exit(START_PLAYERS_ERROR_MSG)


if __name__ == '__main__':
    main()
