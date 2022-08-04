from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.request
import time
import uuid
import os
import json


class Webscraper:

    def __init__(self): # setup wedbdriver and game_dict which will contain game data from top 6 games of user selected category or all categories. ask user to input category.
        self.game_dict = {} # will contain all game info, each game will be contained within nested dictionary
        self.category = input("Please enter board game category. Ensure first letter of all words is capitalised. Leave blank to scrape all categories: ")
        self.driver = webdriver.Chrome()

    
    def open_website(self): # open website and accept cookies
        URL = "https://boardgamegeek.com/browse/boardgamecategory"
        self.driver.get(URL)
        time.sleep(1)
        delay = 4
        try:
            cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="c-p-bn"]')))
            cookies_button.click()
        except TimeoutException:
            pass
        self.select_category(self.category)


    def select_category(self, category): # make driver click link to inputted game category
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
                print ("Input does not match an available category. Please run file again")
                self.driver.quit()


    def category_links(self):
        category_container = self.driver.find_element(By.XPATH, '//*[@id="maincontent"]/table/tbody') # element containing all categories on page
        category_list = category_container.find_elements(By.XPATH, './tr/td') # list of categories 
        category_link_list = []
        for category in category_list:
            a_tag = category.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            category_link_list.append(link)   
        return category_link_list


    def game_links(self): # get links to top 6 games for selected category
        game_container = self.driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing top 6 games listed on page
        game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
        game_link_list = [] # will contain hyperlinks to top 6 games listed
        for game in game_list: # iterate through games and get hyperlinks
            a_tag = game.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            game_link_list.append(link)
        return game_link_list 
        
        
    def get_name(self): # get game name
        try:
            name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        except:
            name = ""
        return name

    
    def get_year(self): # get year published:    
        try:
            year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        except:
            year = ""
        return year


    def get_rating(self): # get game rating    
        try:
            ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]') 
            ratings_tab.click() # switch to 'ratings' tab 
            rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text # get game rating
        except:
            rating = ""
        return rating

        
    def get_num_players(self):    
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

        
    def get_age(self): # get game age rating
        try:
            age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        except:
            age = ""
        return age

        
    def get_wanted_by(self): # get number of people that have game on wishlist
        try:
            stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]') 
            stats_tab.click() # switch to 'stats' tab
            wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text # get 'wanted by' info (number of people expressing wish to get game)
        except:
            wanted_by = ""
        return wanted_by

        
    def get_image(self): # get game image url   
        try:
            image_xpath = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[1]/ng-include/div/a[1]/img')
            image_src = image_xpath.get_attribute("src")
        except:
            image_src = ""
        return image_src


    def iterate_categories(self):
        links = self.category_links()
        for hyper in links:
            time.sleep(1)
            self.driver.get(hyper)
            category = self.driver.find_element(By.XPATH, '//*[@class="game-header-title-info"]/h1/a').text
            self.iterate_games(category)
        self.driver.quit()
        save_dict_records(self.game_dict)
    
    
    def iterate_games(self, category): # open game pages, create dictionary of info for each game and append dictionaries to game_dict. quit driver when complete. 
        time.sleep(1)
        links = self.game_links()
        for hyper in links:
            BGG_ID = hyper.split("/")[4]
            if BGG_ID in self.game_dict:
                self.game_dict[BGG_ID]['Category'].append(category)
            else:
                self.driver.get(hyper)
                info_dict = {'UUID': "", 'BGG_ID': "", 'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': "", 'Image': "", 'Category': []}
                info_dict['UUID'] = str(uuid.uuid4())
                info_dict['BGG_ID'] = BGG_ID
                info_dict['Name'] = self.get_name()
                info_dict['Year'] = self.get_year()
                info_dict['Rating'] = self.get_rating()
                info_dict['Number of Players'] = self.get_num_players()
                info_dict['Age'] = self.get_age()
                info_dict['Wanted By'] = self.get_wanted_by()
                info_dict['Image'] = self.get_image()
                info_dict['Category'].append(category)
                self.game_dict[BGG_ID] = info_dict
            time.sleep(1)


def save_dict_records(game_dict): # save each game dictionary in unique folder within folder 'raw_data'
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