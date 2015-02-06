"""
Fantasy sports team page
"""

from bs4 import BeautifulSoup
from datetime import datetime


SPORT_URLS = {
    'nba': 'http://basketball.fantasysports.yahoo.com/nba'
}


def url(sport, league_id, team_id, start_date=None):
    """
    Given sport name, league_id, team_id, and optional start date (YYYY-MM-DD),
    return the url for the fantasy team page for that date (default: today)
    """
    url = '%s/%s/%s/' % (SPORT_URLS[sport], league_id, team_id)
    if start_date is not None:
        url += 'team?&date=%s' % start_date
    return url


def team(page):
    """
    Return the team name
    """
    soup = BeautifulSoup(page)
    try:
        return soup.find('title').text.split(' | ')[0].split(' - ')[1]
    except:
        return None


def league(page):
    """
    Return the league name
    """
    soup = BeautifulSoup(page)
    try:
        return soup.find('title').text.split(' | ')[0].split(' - ')[0]
    except:
        return None


def date(page):
    """
    Return the date, nicely-formatted
    """
    soup = BeautifulSoup(page)
    try:
        page_date = soup.find('input', attrs={'name': 'date'})['value']
        parsed_date = datetime.strptime(page_date, '%Y-%m-%d')
        return parsed_date.strftime('%a, %b %d, %Y')
    except:
        return None


def alternates(page):
    """
    Given text of Yahoo fantasy team page, return iterable containing players
    on bench who are available to play, where each player is a dict containing:

    - name
    - details
    - opponent
    """
    soup = BeautifulSoup(page)
    try:
        bench = soup.find_all('tr', class_='bench')
        bench_bios = [p.find('div', class_='ysf-player-name') for p in bench]
        names = [p.find('a').text for p in bench_bios]
        details = [p.find('span').text for p in bench_bios]
        opponents = [p.find_all('td', recursive=False)[3].text for p in bench]
        players = [{'name': n, 'details': d, 'opponent': o}
                   for (n, d, o) in zip(names, details, opponents)]
        return [p for p in players if len(p['opponent']) > 0]
    except:
        return None


def start_active_players_path(page):
    """
    Given text of Yahoo fantasy team page, return the path in the
    "Start Active Players" button
    """
    soup = BeautifulSoup(page)
    try:
        return soup.find('a', href=True, text='Start Active Players')['href']
    except:
        return None
