# Scripts for Yahoo fantasy basketball

## Install dependencies

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

## Activate virtualenv (if not already done)

    $ . venv/bin/activate

## Authentication

Set Yahoo credentials in the `YAHOO_USERNAME` and `YAHOO_PASSWORD` [environment variables](http://en.wikipedia.org/wiki/Environment_variable#Assignment).

## Start active players

    $ python start_active_players.py <league_id> <team_id> <date (default: today, format: YYYY-MM-DD)> <num_days (default: 1, max: 100)>

### Usage examples with output

Start active players for the next week:

    $ python start_active_players.py 847591 8 8
    Superteams League - Lamarc Gasolridge's Team:

    - Sat, Feb 07, 2015: Started active players
        - Alternate: Gerald Henderson (Cha - SG,SF) [@Phi]
    - Sun, Feb 08, 2015: Started active players
    - Mon, Feb 09, 2015: Started active players
    - Tue, Feb 10, 2015: Started active players
    - Wed, Feb 11, 2015: Started active players
    - Thu, Feb 12, 2015: Started active players
    - Fri, Feb 13, 2015: Started active players
    - Sat, Feb 14, 2015: Started active players

Start active players for the week starting with March 3, 2015:

    $ python start_active_players.py 847591 8 2015-03-03 7
    Superteams League - Lamarc Gasolridge's Team:

    - Tue, Mar 03, 2015: Started active players
    - Wed, Mar 04, 2015: Started active players
    - Thu, Mar 05, 2015: Started active players
    - Fri, Mar 06, 2015: Started active players
        - Alternate: DeMarcus Cousins (Sac - PF,C) [@Orl]
        - Alternate: Dennis Schroder (Atl - PG) [Cle]
    - Sat, Mar 07, 2015: Started active players
    - Sun, Mar 08, 2015: Started active players
    - Mon, Mar 09, 2015: Started active players

## Project matchup

    $ python project_matchup.py <league_id> <team_id>
