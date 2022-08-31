"""
This module contains a unittest class to test the correct functionality of 3 public methods within the BGGScraper class
"""


import unittest
from webscraper import BGGScraper
from selenium.webdriver.common.by import By

class WebscraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_scraper = BGGScraper()
        self.test_scraper.accept_cookies('//*[@id="c-p-bn"]')   

    @unittest.skip
    def test_select_category(self):
        """
        Tests that the page visted by select_category method is the correct name
        """
        self.test_scraper.select_category(self.test_scraper.category) # goto user selected category using select_category method
        page_category = self.test_scraper.driver.find_element(By.XPATH, '//*[@class="game-header-title-info"]/h1/a').text # get category name from page visited
        self.assertMultiLineEqual(self.test_scraper.category, page_category) # compare user entered category name with category name on page and test they are the same 
    
    @unittest.skip
    def test_iterate_categories(self):
        """
        Tests that iterate_categories method returns a dictionary the same length as the number of categories on the categories page
        """
        category_links = self.test_scraper.category_links() # get category links from category page
        self.assertEqual(len(category_links), len(self.test_scraper.iterate_categories(category_links))) # test length of list returned by category_links() is equal to length of dictionary returned by iterate_categories()


    @unittest.skip
    def test_iterate_games(self):
        """
        Tests that iterate_games method returns a dictionary of length equal to the number of game links on selected category page
        """
        self.test_scraper.select_category(self.test_scraper.category) # goto user inputted category
        game_links = {}
        game_links[self.test_scraper.category] = self.test_scraper.game_links() # get game links from page
        self.assertEqual(len(self.test_scraper.iterate_games(game_links)), len(game_links[self.test_scraper.category])) # test length of dictionary returned by iterate_games() is equal to the value of game_links (which is a list)
    
    def tearDown(self) -> None:
        self.test_scraper.driver.quit()

unittest.main(argv=[''], verbosity=0, exit=False)

# future improvement: look at unittest mock package (https://www.youtube.com/watch?v=cH6G9qFOrPg&list=PLQuVqKqF3P6pv9q0xJl3cA33-g_XKCP-L&index=33)
# and setup and teardown class (allows all tests to run in one sweep, rather than setup/teardown occuring for each test) https://www.techbeamers.com/selenium-python-test-suite-unittest/#h1.1
