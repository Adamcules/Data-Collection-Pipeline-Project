from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class Webscraper:

    def __init__(self): # setup webdriver and info_list which will contain game data from top 6 games of user selected category. ask user to input category.
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


    def get_game_info(self): # get desired info from current game page and store in dictionary
        info_dict = {'BGG_ID': "", 'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': "", 'Image': ""}
        # get bgg game id info:
        bgg_id_text = self.driver.find_element(By.XPATH, '//div[@class="game-itemid ng-binding"]').text
        # extract number (int) from id text:
        bgg_id = int(''.join(filter(str.isdigit, bgg_id_text)))
        # add id to dictionary:
        info_dict['BGG_ID'] = bgg_id
        # get game name:
        name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        # add name to dictionary:
        info_dict['Name'] = name
        # get year published:    
        year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        # add year to dictionary: 
        info_dict['Year'] = year
        # switch to 'ratings' tab:
        ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]')
        ratings_tab.click()
        # get game rating:
        rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text
        # add rating to dictionary:
        info_dict['Rating'] = rating
        # get 'player from' info:
        player_from = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text
        # get 'player to' info (not all games have this element, thus use of 'try' function): 
        try:
            player_to = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text
        except:
            player_to = ""
        # calculate game number of players. 'From-To' format:
        num_players = player_from + player_to
        # add num_players to dictionary:
        info_dict['Number of Players'] = num_players
        # get game age rating:
        age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        # add age to dictionary:
        info_dict['Age'] = age
        # switch to 'stats' tab:
        stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]')
        stats_tab.click()
        # get 'wanted by' info (number of people expressing wish to get game):
        wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text
        # add wanted_by to dictionary:
        info_dict['Wanted By'] = wanted_by
        # get game image link:
        image_xpath = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[1]/ng-include/div/a[1]/img')
        image_src = image_xpath.get_attribute("src")
        # add image to dictionary:
        info_dict['Image'] = image_src
        
        return info_dict

    def iterate_games(self): # open game pages and append game info to info_list. quit driver when complete. 
        time.sleep(2)
        links = self.game_links()
        for hyper in links:
            self.driver.get(hyper)
            self.info_list.append(self.get_game_info())            
            time.sleep(2)
        self.info_list = sorted(self.info_list, key=lambda k: k['Rating'], reverse = True) # sort games by rating value, highest first
        print (self.info_list)
        self.driver.quit()


if __name__ == "__main__":
    scrape = Webscraper()
    scrape.open_website()