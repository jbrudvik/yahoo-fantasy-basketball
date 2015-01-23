# Scripts for Yahoo! fantasy basketball

## Install dependencies

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

## Activate virtualenv (if not already done)

    $ . venv/bin/activate

## Authentication

Set Yahoo! credentials in the `YAHOO_USERNAME` and `YAHOO_PASSWORD` [environment variables](http://en.wikipedia.org/wiki/Environment_variable#Assignment).

## Start active players

    $ python start_active_players.py <league_id> <team_id>

## Project matchup

    $ python project_matchup.py <league_id> <team_id>
