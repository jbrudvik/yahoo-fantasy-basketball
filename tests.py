import unittest
from yahooscraper import *


class YahooScraperImportTests(unittest.TestCase):
    def test_import(self):
        import yahooscraper

        self.assertIsNotNone(yahooscraper)

        self.assertIsNotNone(yahooscraper.login)
        self.assertIsNotNone(yahooscraper.fantasy)
        self.assertIsNotNone(yahooscraper.fantasy.team)

        self.assertIsNotNone(yahooscraper.login.url)
        self.assertIsNotNone(yahooscraper.fantasy.team.url)

    def test_import_as(self):
        import yahooscraper as ys

        self.assertIsNotNone(ys)

        self.assertIsNotNone(ys.login)
        self.assertIsNotNone(ys.fantasy)
        self.assertIsNotNone(ys.fantasy.team)

        self.assertIsNotNone(ys.login.url)
        self.assertIsNotNone(ys.fantasy.team.url)

    def test_import_all(self):
        # import * only allowed at module level, so this relies upon
        # `from yahooscraper import *` outside of test class

        self.assertIsNotNone(login)
        self.assertIsNotNone(fantasy)
        self.assertIsNotNone(fantasy.team)

        self.assertIsNotNone(login.url)
        self.assertIsNotNone(fantasy.team.url)

    def test_import_explicit(self):
        from yahooscraper import login, fantasy

        self.assertIsNotNone(login)
        self.assertIsNotNone(fantasy)
        self.assertIsNotNone(fantasy.team)

        self.assertIsNotNone(login.url)
        self.assertIsNotNone(fantasy.team.url)


class YahooScraperLoginTests(unittest.TestCase):
    def test_url(self):
        import yahooscraper as ys
        self.assertIsNotNone(ys.login.url())

    def test_path(self):
        import yahooscraper as ys
        self.assertIsNone(ys.login.path(''))
        self.assertEqual(
            ys.login.path('<div id="mbr-login-form" action="foo"></div>'),
            'foo')

    def test_post_data(self):
        import yahooscraper as ys
        self.assertIsNone(ys.login.post_data('', 'foo', 'bar'))
        self.assertIsInstance(
            ys.login.post_data('<div id="hiddens"></div>', 'foo', 'bar'),
            dict)


class YahooScraperFantasyTeamTests(unittest.TestCase):
    def test_url(self):
        import yahooscraper as ys
        self.assertIsNotNone(ys.fantasy.team.url('nba', 1, 2))

    def test_team(self):
        import yahooscraper as ys
        self.assertIsNone(ys.fantasy.team.team(''))
        self.assertEquals(
            ys.fantasy.team.team('<title>league-name - team-name</title>'),
            'team-name')

    def test_league(self):
        import yahooscraper as ys
        self.assertIsNone(ys.fantasy.team.league(''))
        self.assertIsNotNone(ys.fantasy.team.league(
            '<title>league-name - team-name</title>'),
            'league-name')

    def test_date(self):
        import yahooscraper as ys
        self.assertIsNone(ys.fantasy.team.date(''))
        self.assertEqual(ys.fantasy.team.date(
            '<input name="date" value="2020-01-31"></input>'),
            'Fri, Jan 31, 2020')

    def test_alternates(self):
        import yahooscraper as ys
        self.assertIsNotNone(iter(ys.fantasy.team.alternates('')))

    def test_start_active_players_path(self):
        import yahooscraper as ys
        self.assertIsNone(ys.fantasy.team.start_active_players_path(''))
        self.assertEqual(ys.fantasy.team.start_active_players_path(
            '<a href="baz">Start Active Players</a>'),
            'baz')


if __name__ == '__main__':
    unittest.main(verbosity=2)
