"""
This module contains classes for initialising a webdriver (Class: Webdriver), a webscraper (BGGScraper) to scrape the website 'BoardGameGeek'
(BGG) (class: BGGScraper), for saving scraped data in local files (class: LocalSave) and for exporting local files to a cloud-based S3 bucket
(class: S3Exporter).
"""

import boto3 
import json 
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import urllib.request
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
        self.driver = webdriver.Chrome()
        self.driver.get(url)
    
    
    def accept_cookies(self, xpath: str): 
        """
        This function clicks an 'Accept Cookies' button if it appears and passes if none appears after 4 seconds.
        """
        time.sleep(1)
        delay = 4
        try:
            cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath))) # wait up to 4 seconds for 'Accept Cookies' button to appear. XPATH to button passed to function as xpath) 
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

    def run(self):
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
        
        self.accept_cookies('//*[@id="c-p-bn"]') # click 'Accept Cookies' button
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


class LocalSave:

    """
    This class contains methods to save information passed to it as a python dictionary within local folders.

    A user can enter a directory to store all the files or use the default directory.
    """
    
    def __init__(self, game_dict: dict, save_folder: str = input('Please enter directory for local save folder. Leave blank for default: ')):
        self.game_dict = game_dict
        if save_folder == "":
            self.save_folder = '/Users/adam-/OneDrive/Desktop/AI_Core/Data-Collection-Pipeline-Project/raw_data' # default directory used if user does not enter alternative
        else:
            self.save_folder = save_folder 

    def save_dict_records(self):
        """
        This function saves dictionary values as JSON files within a local directory folder. 
        
        The function attempts to create a file called 'raw_data' (unless the user has specified another directory). 
        The function then iterates through each item in the dictionary passed to it, checks whether a folder has already been created for that
        item and, if not, creates a folder for it within the parent folder, naming the folder after the dictionary key name.
        It then writes a JSON file within that folder called 'data.json' which contains the value information for that dictionary item.
        """
        if not os.path.exists(self.save_folder): # check whether directory already exists
            os.mkdir(self.save_folder) # create new folder
        else:
            print ("local save directory already exists.")
        for game in self.game_dict: # iterate through dictionary passed to instance of class
            directory = os.path.join(self.save_folder, game) # create directory name for dictionary item
            try:
                os.mkdir(directory) # check whether folder already exists for dictionary item and create if it doesn't
            except:
                print (f"game directory {game} already exists.")
            data_file = os.path.join(directory, 'data.json') # create file name for saved data 
            with open(data_file, 'w') as fp: # write json file containing value info for dictionary item
                json.dump(self.game_dict[game], fp)


    def save_game_images(self): 
        """
        This function creates a file called 'images' within the parent folder created by self.save_dict_records and saves image files found within dictionary passed to instance of class  
        
        NB: For this function to work, the dictionary passed to the class must consist of nested dictionaries containing the key 'Images'.

        The function first checks whether a folder called 'images' has been created within the parent folder. If not, it creates this folder.
        The function then iterates through the dictionary passed to the class instance. For each item, it obtains the url to the image file
        stored under the nested dictionary key 'Images' and saves the image within the 'images' folder using urllib.request library and
        .urlretrieve function. The file is named after the key name.
        """
        images = os.path.join(self.save_folder, 'images') # create 'images' folder name
        if not os.path.exists(images): # check if folder already exists
            os.mkdir(images) # create folder
        else:
            print ('images directory already exists.')
        for game in self.game_dict:
            name = f"{game}.jpg" # create file name for image 
            url = self.game_dict[game]['Image'] # get url for image
            image_file = os.path.join(images, name) # create directory for image file
            urllib.request.urlretrieve(url, image_file) # save image file in 'images' folder
        
    def run(self):
        """
        This function contains the logic for running an instance of Local_Save class.

        The function calls to self.save_dict_recrods and self.save_game_images in turn.
        """
        self.save_dict_records()
        self.save_game_images()


class S3ExporterLocal:
    """
    This class contains a method to export local files to an S3 Bucket
    """
    def __init__(self, local_path: str, bucket_name: str) -> None:
        self.local_path = local_path # defines local folder containing files to export
        self.bucket_name = bucket_name # name of target S3 bucket to export to
        self.s3_client = boto3.client('s3') # initialise S3 boto3 client

    def export_to_bucket(self):
        """
        This function iterates through a local folder and uploads the files to an S3 bucket
        """
        for root,dirs,files in os.walk(self.local_path): # iterate through folders and files in local directory
            for file in files: # iterate through source files
                parse_root = root.split('\\')[1] # get parent folder name of file
                if parse_root == 'images': # checks if file is in local 'images' folder
                    file_name = file.removesuffix('.jpg') + ' - ' + 'image.jpg' # set upload filename
                    self.s3_client.upload_file(os.path.join(root, file), self.bucket_name, file_name) # upload file to S3 bucket
                else:
                    file_name = parse_root + ' - ' + file # set upload filename
                    self.s3_client.upload_file(os.path.join(root, file), self.bucket_name, file_name) # upload file to S3 bucket


class S3ExporterDirect():
    def __init__(self, bucket_name: str, game_dict: dict) -> None:
        self.bucket_name = bucket_name
        self.game_dict = game_dict
        self.s3_client = boto3.client('s3') # initialise S3 boto3 client
    
    def export_json(self):
        for game in self.game_dict:
            file_name = game + ' - ' + 'data.json'
            json_object = self.game_dict[game]
            self.s3_client.put_object(Body=json.dumps(json_object), Bucket=self.bucket_name, Key=file_name)
    
    def export_image(self):
        for game in self.game_dict:
            file_name = game + ' - ' + 'image.jpg'
            url = self.game_dict[game]['Image']
            response = requests.get(url, stream=True)
            image = response.content
            self.s3_client.put_object(Body=image, Bucket=self.bucket_name, Key=file_name)
        

if __name__ == "__main__":
    bgg_scrape = BGGScraper()
    bgg_scrape.run()
    save_option = input("Press 'L' to store data locally, 'C' to upload data to cloud or 'B' to do both: ").capitalize()
    if save_option == 'L':
        data_save = LocalSave(bgg_scrape.game_dict)
        data_save.run()
    elif save_option == 'C':
        direct_data_export = S3ExporterDirect('data-collection-project-bucket', bgg_scrape.game_dict)
        direct_data_export.export_json()
        direct_data_export.export_image()
    elif save_option == 'B':
        data_save = LocalSave(bgg_scrape.game_dict)
        data_save.run()
        local_data_export = S3ExporterLocal('./raw_data','data-collection-project-bucket')
        local_data_export.export_to_bucket()