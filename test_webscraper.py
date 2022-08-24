import unittest
from webscraper import BGGScraper
import time
from selenium.webdriver.common.by import By

class WebscraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_scraper = BGGScraper()
        self.test_scraper.accept_cookies('//*[@id="c-p-bn"]')   

    @unittest.skip
    def test_select_category(self):
        self.test_scraper.select_category(self.test_scraper.category)
        page_category = self.test_scraper.driver.find_element(By.XPATH, '//*[@class="game-header-title-info"]/h1/a').text
        self.assertMultiLineEqual(self.test_scraper.category, page_category)  
    
    
    def test_iterate_categories(self):
        category_links = self.test_scraper.category_links()
        game_links = self.test_scraper.iterate_categories(category_links)
        link_count = 0
        for category in game_links:
            link_count += len(game_links[category]) 
        self.assertEqual(len(category_links)*6, link_count)


    @unittest.skip
    def test_iterate_games(self):
        self.test_scraper.select_category(self.test_scraper.category)
        game_links = {}
        game_links[self.test_scraper.category] = self.test_scraper.game_links()
        self.assertEqual(len(self.test_scraper.iterate_games(game_links)), len(game_links[self.test_scraper.category]))
    
    def tearDown(self) -> None:
        self.test_scraper.driver.quit()

unittest.main()

# future improvement: look at unittest mock package (https://www.youtube.com/watch?v=cH6G9qFOrPg&list=PLQuVqKqF3P6pv9q0xJl3cA33-g_XKCP-L&index=33)
# and setup and teardown class (allows all tests to run in one sweep, rather than setup/teardown occuring for each test) https://www.techbeamers.com/selenium-python-test-suite-unittest/#h1.1
