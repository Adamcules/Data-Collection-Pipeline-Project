from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import uuid
import os
import json

class Webscraper:

    def __init__(self): # setup wedbdriver and info_list which will contain game data from top 6 games of user selected category. ask user to input category.
        self.info_list = []
        self.category = input("Please enter board game category. Ensure first letter of all words is capitalised: ")
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


    def select_category(self, category): # make driver click inputted game category
        time.sleep(1)
        delay = 4
        try:   
            link = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, f"{category}")))
            link.click()
            self.iterate_games()
        except TimeoutException:
            print ("Input does not match an available category. Please run file again")
            self.driver.quit()     


    def game_links(self): # get links to top 6 games for selected category
        game_container = self.driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing top 6 games listed on page
        game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
        link_list = [] # will contain hyperlinks to top 6 games listed
        for game in game_list: # iterate through games and get hyperlinks
            a_tag = game.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        return link_list 
        
    def get_id(self): # get bgg game id info
        bgg_id_text = self.driver.find_element(By.XPATH, '//div[@class="game-itemid ng-binding"]').text
        bgg_id = ''.join(filter(str.isdigit, bgg_id_text))  # extract number (int) from id text
        return bgg_id

        
    def get_name(self): # get game name
        name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        return name

    
    def get_year(self): # get year published:    
        year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        return year


    def get_rating(self): # get game rating    
        ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]') 
        ratings_tab.click() # switch to 'ratings' tab 
        rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text # get game rating
        return rating

        
    def get_num_players(self):    
        player_from = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text # get 'player from' info
        try:
            player_to = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text # get 'player to' info (not all games have this element, thus use of 'try' function)
        except:
            player_to = ""
        num_players = player_from + player_to # calculate game number of players. 'From-To' format
        return num_players

        
    def get_age(self): # get game age rating
        age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        return age

        
    def get_wanted_by(self): # get number of people that have game on wishlist
        stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]') 
        stats_tab.click() # switch to 'stats' tab
        wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text # get 'wanted by' info (number of people expressing wish to get game)
        return wanted_by

        
    def get_image(self): # get game image link    
        image_xpath = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[1]/ng-include/div/a[1]/img')
        image_src = image_xpath.get_attribute("src")
        return image_src
        

    def iterate_games(self): # open game pages and append game info to info_list. quit driver when complete. 
        time.sleep(2)
        links = self.game_links()
        for hyper in links:
            self.driver.get(hyper)
            info_dict = {'UUID': "", 'BGG_ID': "", 'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': "", 'Image': ""}
            info_dict['UUID'] = str(uuid.uuid4())
            info_dict['BGG_ID'] = self.get_id()
            info_dict['Name'] = self.get_name()
            info_dict['Year'] = self.get_year()
            info_dict['Rating'] = self.get_rating()
            info_dict['Number of Players'] = self.get_num_players()
            info_dict['Age'] = self.get_age()
            info_dict['Wanted By'] = self.get_wanted_by()
            info_dict['Image'] = self.get_image()
            self.info_list.append(info_dict)            
            time.sleep(2)
        self.info_list = sorted(self.info_list, key=lambda k: k['Rating'], reverse = True) # sort games by rating value, highest first
        self.driver.quit()
        self.save_dict_records()
        

    def save_dict_records(self): # save each game dictionary in unique folder within folder 'raw_data'
        raw_data = '/Users/adam-/OneDrive/Desktop/AI_Core/Data-Collection-Pipeline-Project/raw_data'
        if not os.path.exists(raw_data):
            os.mkdir(raw_data)
        else:
            print ("raw_data directory already exists")
        for game in self.info_list:
            directory = os.path.join(raw_data, game['BGG_ID'])
            try:
                os.mkdir(directory)
            except:
                print (f"game directory {game['BGG_ID']} already exists")
            data_file = os.path.join(directory, 'data.json')
            with open(data_file, 'w') as fp:
                json.dump(game, fp)

            
if __name__ == "__main__":
    scrape = Webscraper()
    scrape.open_website()


    

