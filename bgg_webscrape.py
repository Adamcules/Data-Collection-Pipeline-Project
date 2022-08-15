"""
This module contains a class for initialising a webscraper to scrape the website 'BoardGameGeek' (BGG) and
functions for saving the scraped data in local files.
"""

import json 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import urllib.request
import uuid



class Webscraper:
    """
    This class initialises a Chrome webdriver and generates a dictionary containing information on boardgames.

    The webdriver opens the 'Categories' page on the website 'BoardGameGeek' (BGG). The driver then iterates through
    and follows the URL to each category found on the page (unless the user enters a specific category to check). 
    Within each category, the driver iterates through and follows the URL to each of the 'Top 6' games listed
    under that category. The driver then gathers info on each of those games, storing the info within the 
    dictionary 'game_dict'.

    Attributes:
        game_dict (dict): Stores all the game info scraped.
        category (str): The category to be scraped entered by the user (if left blank, all categories are scraped).
        driver (webdriver): Chrome webdriver imported from Selenium.
    """
    def __init__(self):
        """
        See help(Webscraper) for accurate signature.
        """
        self.game_dict = {} 
        self.category = input("Please enter board game category. Ensure first letter of all words is capitalised. Leave blank to scrape all categories: ")
        self.driver = webdriver.Chrome()

    
    def open_website(self, url: str = "https://boardgamegeek.com/browse/boardgamecategory"): 
        """
        This function opens the BGG website. 
        
        The webdriver opens the website on the 'Categories' page and clicks the 'Accept Cookies' button if required.
        The function then calls to the method "self.select_category"
        """
        self.driver.get(url)
        time.sleep(1)
        delay = 4
        try:
            cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="c-p-bn"]')))
            cookies_button.click()
        except TimeoutException
            pass
        self.select_category(self.category)


    def select_category(self, category: str):
        """
        This function makes webdriver iterate through all categories or goto one specific category.

        If the user did not enter a category, this function calls the 'self.iterate_categories' function which iterates
        through all categories, otherwise it makes the driver click on a specific category and then calls to the
        'self.iterate_games' method to scrape games info from that one category.
        """
        time.sleep(1)
        if category == "": 
            self.iterate_categories()
        else:
            delay = 4
            try:   
                link = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, f"{category}")))
                link.click()
                self.iterate_games(category)
            except TimeoutException:
                print ("Input does not match an available category. Please run file again and enter valid category")
                #TODO: get user to re-enter category without having to rerun file
                self.driver.quit()


    def category_links(self):
        """
        This function returns a list of links to all categories on the 'Categories' page. 
        """
        category_container = self.driver.find_element(By.XPATH, '//*[@id="maincontent"]/table/tbody') # element containing all categories on page
        category_list = category_container.find_elements(By.XPATH, './tr/td') # list of categories 
        category_link_list = []
        for category in category_list:
            a_tag = category.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            category_link_list.append(link)   
        return category_link_list


    def game_links(self):
        """
        This function returns a list of links to each of the 'Top 6' games listed under a category.
        """
        game_container = self.driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing top 6 games listed on page
        game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
        game_link_list = [] # will contain hyperlinks to top 6 games listed
        for game in game_list: # iterate through games and get hyperlinks
            a_tag = game.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            game_link_list.append(link)
        return game_link_list 
        
        
    def get_name(self):
        """
        This function returns the name of a game.
        """
        try:
            name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        except:
            name = ""
        return name

    
    def get_year(self):
        """
        This function returns the year a game was published.
        """   
        try:
            year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        except:
            year = ""
        return year


    def get_rating(self):
        """
        This function returns the rating of a game (scored out of 10)
        """    
        try:
            ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]') 
            ratings_tab.click() # switch to 'ratings' tab 
            rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text # get game rating
        except:
            rating = ""
        return rating

        
    def get_num_players(self):
        "This function returns the number of players that can play a game."    
        try:
            player_from = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text # get 'player from' info
            try:
                player_to = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text # get 'player to' info (not all games have this element, thus use of 'try' function)
                player_to = player_to.replace('–', ' to ')
            except:
                player_to = ""
            num_players = player_from + player_to # calculate game number of players. 'From To' format
        except:
            num_players = ""
        return num_players

        
    def get_age(self):
        """
        This function returns the advised player age rating of a game (e.g. 12+)
        """
        try:
            age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        except:
            age = ""
        return age

        
    def get_wanted_by(self):
        """
        This function returns the number of people who have this game on their BGG wishlist"
        """
        try:
            stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]') 
            stats_tab.click() # switch to 'stats' tab
            wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text # get 'wanted by' info (number of people expressing wish to get game)
        except:
            wanted_by = ""
        return wanted_by

        
    def get_image(self):
        """
        This function returns the url for the image icon of a game.
        """  
        try:
            image_xpath = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[1]/ng-include/div/a[1]/img')
            image_src = image_xpath.get_attribute("src")
        except:
            image_src = ""
        return image_src


    def iterate_categories(self):
        """
        This function makes the webdriver click on each category on the 'Categories' page.

        The function iterates through each hyperlink in the list 'links' (returned by self.category_links()). The
        driver follows each link and for each makes a call to the method 'self.iterate_games', passing the
        argument 'category' as a string, which is the name of the current category (e.g. 'Card Game').
        Finally it makes the driver quit and makes a call to the function 'save_dict_records', passing self.game_dict
        as an argument.
        """
        links = self.category_links()
        for hyper in links:
            time.sleep(1)
            self.driver.get(hyper)
            category = self.driver.find_element(By.XPATH, '//*[@class="game-header-title-info"]/h1/a').text
            self.iterate_games(category)
        self.driver.quit()
        save_dict_records(self.game_dict)
    
    
    def iterate_games(self, category: str): 
        """
        This function checks whether a game has already been stored within self.game_dict and appends game info to self.game_dict accordingly.
        
        After the driver has followed a link to a given category page, this function calls to self.game_links to create a list called 'links'
        which contains links to the top 6 games listed for the category. The function checks to see if any of the games have already been added
        to self.game_dict. If not, the driver goes to the game page and creates a dictionary (info_dict) to contain scraped game info. The
        function then calls various class methods to obtain the following info and append to info_dict:
        
        'UUID'              (generated as a uuid4 by the function using uuid library)
        'BGG_ID'            (a unique ID number for the game assigned by BoardGameGeek)
        'Name'              (name of boardgame)
        'Year'              (year game was published)
        'Rating'            (a game rating score out of 10)
        'Number of players' (number of players that can play the game)
        'Age'               (advised age rating for game)
        'Wanted By'         (number of people who have game on BGG wishlist)
        'Image'             (url of game icon image)
        'Category'          (list of categories for which the game is rated as a 'Top 6' game)

        This dictionary of game info is then appended as a nested dictionary to self.game_dict.

        If the game has already been added to self.game_dict, then only the category name is appended as a value to the game's 
        [Category] key (which is a list).         
        """
        time.sleep(1)
        links = self.game_links()
        for hyper in links:
            bgg_id = hyper.split("/")[4]
            if bgg_id in self.game_dict:
                self.game_dict[bgg_id]['Category'].append(category)
            else:
                self.driver.get(hyper)
                info_dict = {'UUID': "", 'BGG_ID': "", 'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': "", 'Image': "", 'Category': []}
                info_dict['UUID'] = str(uuid.uuid4())
                info_dict['BGG_ID'] = bgg_id
                info_dict['Name'] = self.get_name()
                info_dict['Year'] = self.get_year()
                info_dict['Rating'] = self.get_rating()
                info_dict['Number of Players'] = self.get_num_players()
                info_dict['Age'] = self.get_age()
                info_dict['Wanted By'] = self.get_wanted_by()
                info_dict['Image'] = self.get_image()
                info_dict['Category'].append(category)
                self.game_dict[bgg_id] = info_dict
            time.sleep(1)


def save_dict_records(game_dict):
    """
    This function is passed the game_dict from the Webscraper class and saves individual game info as JSON files
    within local folders.

    The function attempts to create a file called 'raw_data' within the specified directory. The function then
    iterates through each game in game_dict, creating a folder for each game within raw_data named after the BGG_ID
    number of the game and then writes a JSON file within the folder containg all game info scraped by the Webscraper
    class.

    Finally the function calls to save_game_images.
    """
    raw_data = '/Users/adam-/OneDrive/Desktop/AI_Core/Data-Collection-Pipeline-Project/raw_data'
    if not os.path.exists(raw_data):
        os.mkdir(raw_data)
    else:
        print ("raw_data directory already exists.")
    for game in game_dict:
        directory = os.path.join(raw_data, game)
        try:
            os.mkdir(directory)
        except:
            print (f"game directory {game} already exists.")
        data_file = os.path.join(directory, 'data.json')
        with open(data_file, 'w') as fp:
            json.dump(game_dict[game], fp)
    save_game_images(raw_data, game_dict)


def save_game_images(raw_data, game_dict): # save game image for each game within 'images' folder inside 'raw_data' folder
    """
    This function saves the game icon image for each game in a folder called 'images' within the 'raw_data' folder. 
    """
    images = os.path.join(raw_data, 'images')
    if not os.path.exists(images):
        os.mkdir(images)
    else:
        print ('images directory already exists.')
    for game in game_dict:
        name = f"{game}.jpg"
        url = game_dict[game]['Image']
        image_file = os.path.join(images, name)
        urllib.request.urlretrieve(url, image_file)


if __name__ == "__main__":
    scrape = Webscraper()
    scrape.open_website()