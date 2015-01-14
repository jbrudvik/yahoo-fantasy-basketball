"""
Project results of the current matchup

# Algorithm sketch
- Loop through Mon-Sun, sucking in stats (add column for day)
    - Mon: http://basketball.fantasysports.yahoo.com/nba/178276/6
    - Tues: http://basketball.fantasysports.yahoo.com/nba/178276/6/team?&date=2015-01-13&stat1=S&stat2=D
- Average / sum these
- Also do for opponent
- Output category statistics, and projected overall score vs opponent

# Use
- If anything major jumps out, address it through personnel changes

# Implementation
- numpy or pandas?
- How to authenticate? Ideally, take environment vars
    - Then set via $ YAHOO_USERNAME=foo YAHOO_PASSWORD=bar python project-matchup.py
"""
