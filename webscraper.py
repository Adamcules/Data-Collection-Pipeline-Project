"""
This module contains two classes: Webdriver and BGGScraper.

Webdriver initialises a Selenium Chrome webdriver and BGGScraper is a child class that performs a scrape of the website boardgamegeek.com (BGG)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import uuid


class Webdriver:
    """
    This class initialises a Chrome webdriver.

    The webdriver opens the url passed to it and attempts to click an 'Accept Cookies' button if it appears.

    Attributes:
        driver (webdriver): Chrome webdriver imported from Selenium.
    """
    def __init__(self, url: str):
        """
        See help(Webdriver) for accurate signature.
        """
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url)
    
    
    def accept_cookies(self, button): 
        """
        This function clicks an 'Accept Cookies' button if it appears and passes if none appears after 4 seconds.
        """
        time.sleep(1)
        delay = 4
        try:
            cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, button))) # wait up to 4 seconds for 'Accept Cookies' button to appear. XPATH to button passed to function as button) 
            cookies_button.click()
        except TimeoutException:
            pass


class BGGScraper(Webdriver):
    """ 
    This class is a Child of the 'Webdriver' class. It uses the webdriver to scrape game info from the website 'boardgamegeek.com' (BGG).

    The webdriver opens the 'Categories' page on the website. The driver then either goes to a specific category or iterates through all
    categories based on user input.
    Within each category page, the driver iterates through and follows the url to each of the 'Top 6' games listed under that category.
    The driver then gathers info on each of those games, storing the info within the dictionary 'game_dict'.    
    
    Attributes:
    game_dict (dict): Stores all the game info scraped.
    category (str): The category to be scraped entered by the user (if left blank, all categories are scraped)."""

    def __init__(self, url: str = "https://boardgamegeek.com/browse/boardgamecategory"):
        super().__init__(url)
        self.game_dict = {} 
        self.category = str(input("Please enter board game category. Leave blank to scrape all categories: ")).title() # User input determines whether all categories will be scraped or one specific category.
    
    def select_category(self, category: str):
        """
        This function is called when the user enters a specific category.
        
        It makes the webdriver click on the link to the specific category.
        """
        time.sleep(1)
        delay = 4
        try:   
            link = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, f"{category}")))
            link.click()
        except TimeoutException: # if invalid category is inputted message is printed and file stops running
            print ("Input does not match an available category. Please run file again and enter valid category")
            #TODO: get user to re-enter category without having to rerun file
            self.driver.quit()


    def category_links(self):
        """
        This function returns category_link list. A list of links to all categories on the 'Categories' page. 
        """
        time.sleep(2)
        category_container = self.driver.find_element(By.XPATH, '//*[@id="maincontent"]/table/tbody') # element containing all categories on page
        category_list = category_container.find_elements(By.XPATH, './tr/td') # list of categories 
        category_link_list = []
        for category in category_list: # iterates through categories and appends href of each category to category_link_list
            a_tag = category.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            category_link_list.append(link)  
        return category_link_list


    def game_links(self):
        """
        This function returns game_link_list. A list of links to each of the 'Top 6' games listed under a category.
        """
        game_container = self.driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing top 6 games listed on page
        game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
        game_link_list = []
        for game in game_list: # iterates through games and appends href of each game to game_link_list
            a_tag = game.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            game_link_list.append(link)
        return game_link_list 
        
        
    def __get_name(self):
        """
        This function returns the name of a game.
        """
        try:
            name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        except:
            name = ""
        return name

    
    def __get_year(self):
        """
        This function returns the year a game was published.
        """   
        try:
            year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        except:
            year = ""
        return year


    def __get_rating(self):
        """
        This function returns the rating of a game (scored out of 10)
        """    
        try:
            ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]') # get 'ratings' tab
            ratings_tab.click() # switch to 'ratings' tab 
            rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text
        except:
            rating = ""
        return rating

        
    def __get_num_players(self):
        "This function returns the number of players that can play a game."    
        try:
            player_from = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text # get 'player from' info
            try:
                player_to = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text # get 'player to' info (not all games have this element))
                player_to = player_to.replace('–', ' to ') # make number of players read '2 to 4' instead of '2 - 4' as dash symbol used on website is U+2013, which is uncommon in source code.
            except:
                player_to = ""
            num_players = player_from + player_to # calculate game number of players. 'From To' format
        except:
            num_players = ""
        return num_players

        
    def __get_age(self):
        """
        This function returns the advised player age rating of a game (e.g. 12+)
        """
        try:
            age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        except:
            age = ""
        return age

        
    def __get_wanted_by(self):
        """
        This function returns the number of people who have this game on their BGG wishlist"
        """
        try:
            stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]') # get 'stats' tab 
            stats_tab.click() # switch to 'stats' tab
            wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text 
        except:
            wanted_by = ""
        return wanted_by

        
    def __get_image(self):
        """
        This function returns the url for the image icon of a game.
        """  
        try:
            image_xpath = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[1]/ng-include/div/a[1]/img')
            image_src = image_xpath.get_attribute("src")
        except:
            image_src = ""
        return image_src


    def iterate_categories(self, category_links):
        """
        This function makes the webdriver goto each category and returns a dictionary (game_links) containing links to each of the 'top 6' games listed under each category.

        The function iterates through and goes to each hyperlink in category_links list. For each category, it adds the category name
        as a key to the dictionary game_links and makes a call to self.game_links which returns a list of links to games which is added
        as the value to the category key in the dictionary.
        """
        game_links = {}
        for hyper in category_links:
            time.sleep(2)
            self.driver.get(hyper)
            category = self.driver.find_element(By.XPATH, '//*[@class="game-header-title-info"]/h1/a').text # get category name
            game_links[category] = self.game_links() # create category name as key and self.game_links() as value.
        return game_links
    
    
    def iterate_games(self, game_links: dict): 
        """
        This function iterates through game_links, checking whether a game has already been added to self.game_dict and appending game info accordingly.
        
        The function first checks to see if the game has already been added to self.game_dict. If so, it does not follow the game link and simply
        adds the name of the current category as a value to the game's [Category] key (which is a list) within the game's info dictionary: info_dict (a
        game can appear as a 'top 6' game in more than one category).
        If the game has not been added, the driver goes to the game page and creates info_dict to contain scraped game info. The function then calls
        various class methods to obtain the following info and add it to info_dict:
        
        'UUID'              (generated as a uuid4 by the function using uuid library)
        'BGG_ID'            (a unique ID number for the game assigned by BGG)
        'Name'              (name of boardgame)
        'Year'              (year game was published)
        'Rating'            (a game rating score out of 10)
        'Number of players' (number of players that can play the game)
        'Age'               (advised age rating for game)
        'Wanted By'         (number of people who have game on BGG wishlist)
        'Image'             (url of game icon image)
        'Category'          (list of categories for which the game is rated as a 'Top 6' game)

        This dictionary of game info is then added as a nested dictionary to self.game_dict, with the BGG_ID used as the key.
        """
        time.sleep(1)
        for category in game_links: # iterate through each category in game_links dictionary (category names are used as keys)
            for hyper in game_links[category]: # iterate through each game link for each category within game_links dictionary
                bgg_id = hyper.split("/")[4] # get bgg_id from game's url
                if bgg_id in self.game_dict: # check whether game has already been added to self.game_dict
                    self.game_dict[bgg_id]['Category'].append(category) # append current category name as value to game's [Category] key within self.game_dict
                else:
                    self.driver.get(hyper)
                    info_dict = {'UUID': "", 'BGG_ID': "", 'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': "", 'Image': "", 'Category': []}
                    info_dict['UUID'] = str(uuid.uuid4())
                    info_dict['BGG_ID'] = bgg_id
                    info_dict['Name'] = self.__get_name()
                    info_dict['Year'] = self.__get_year()
                    info_dict['Rating'] = self.__get_rating()
                    info_dict['Number of Players'] = self.__get_num_players()
                    info_dict['Age'] = self.__get_age()
                    info_dict['Wanted By'] = self.__get_wanted_by()
                    info_dict['Image'] = self.__get_image()
                    info_dict['Category'].append(category)
                    self.game_dict[bgg_id] = info_dict # add info_dict as value to self.game_dict, using bgg_id as key.
                time.sleep(1)
        return self.game_dict

    def run(self, button):
        """
        This function contains the logic for running an instance of BBGScraper class.

        The function first makes a call to self.accept_cookes. Then if the user has not entered a specific category it makes a call to
        self.category_links to get a list of links to all categories (category_links). This is then passed to self.iterate_categories
        to get a dictionary containing links to the 'top 6' games for each category (game_links). Finally, game_links is passed in turn
        to self.iterate_games to scrape info for each game and add that info to self.game_dict.

        If the user did enter a category, the function makes a call to self.select_category to goto the specific category page. The function
        then creates the dictionary game_links, adding a single 'key : value' pair that has the selected category name as key and a list of
        links to the the 'top 6' games for that category, obtained by calling to self.game_links.
        The game_links dictionary is then passed to self.iterate_games to scrape info for each game and add that info to self.game_dict.
        """
        
        self.accept_cookies(button) # click 'Accept Cookies' button
        if self.category == "": # check whether user enters a specific category or no
            category_links = self.category_links() # obtain links to categories
            game_links = self.iterate_categories(category_links) # obtain links to games
            self.iterate_games(game_links) # scrape info for each game
            self.driver.quit()
        else:
            self.select_category(self.category) # goto category page entered by user
            game_links = {}
            game_links[self.category] = self.game_links() # add list of game links as value to game_links dictionary
            self.iterate_games(game_links) # scrape info for each game
            self.driver.quit()