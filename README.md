# Scripts for Yahoo! fantasy basketball

## Install dependencies

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

## Activate virtualenv (if not already done)

    $ . venv/bin/activate

## Start active players

    $ YAHOO_USERNAME=<username> YAHOO_PASSWORD=<password> python start-active-players.py <league_id> <team_id>

## Project matchup

    $ python project-matchup.py
