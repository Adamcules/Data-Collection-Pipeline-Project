import unittest
from webscraper import BGG_Scraper
import time

class WebscraperTestCase(unittest.TestCase):
    # def test_iterate_categories(self):
    #     test_scraper = BGG_Scraper()
    #     test_scraper.run()
    #     self.assertIsInstance(test_scraper.iterate_categories(), dict)

    def test_iterate_games(self):
        test_scraper = BGG_Scraper()
        test_scraper.accept_cookies('//*[@id="c-p-bn"]')
        test_scraper.select_category(test_scraper.category)
        game_links = {}
        game_links[test_scraper.category] = test_scraper.game_links()
        test_scraper.iterate_games(game_links)
        self.assertEqual(len(test_scraper.game_dict), len(game_links[test_scraper.category]))

unittest.main()