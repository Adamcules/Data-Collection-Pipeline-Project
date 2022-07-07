from ast import Break
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Webscraper:

    def __init__(self): # setup webdriver and info_list which will contain game info from selected game category
        self.info_list = []
        self.category = input("Please enter board game category. Ensure first letter of all words is capitalised: ")
        self.driver = webdriver.Chrome()

    
    def open_website(self): # open website, accept cookies and ask user for game category
        URL = "https://boardgamegeek.com/browse/boardgamecategory"
        self.driver.get(URL)
        time.sleep(2)
        
        try:
            cookies_button = self.driver.find_element(By.XPATH, '//*[@id="c-p-bn"]')
            cookies_button.click()
        except:
            pass
        self.select_category(self.category)


    def select_category(self, category): # make driver click inputted game category
        time.sleep(2)
        try:   
            link = self.driver.find_element(By.LINK_TEXT, f"{category}")
            link.click()
            self.iterate_games()
        except:
            print ("Input does not match an available category. Please run file again")
            self.driver.quit()
            Break       


    def game_links(self): # get links to top 6 games for selected category
        game_container = self.driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing top 6 games listed on page
        game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
        link_list = [] # will contain hyperlinks to top 6 games listed

        for game in game_list: # iterate through games and get hyperlinks
            a_tag = game.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            link_list.append(link)

        return link_list

    
    def get_info(self): # get desired info from current game page and store in dictionary
        info_dict = {'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': ""}
        name = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
        info_dict['Name'] = (name)
        year = self.driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
        info_dict['Year'] = (year)
        ratings_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]')
        ratings_tab.click()
        rating = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text
        info_dict['Rating'] = (rating)
        player_from = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text
        try:
            player_to = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text
        except:
            player_to = ""
        num_players = player_from + player_to
        info_dict['Number of Players'] = (num_players)
        age = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
        info_dict['Age'] = (age)
        stats_tab = self.driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]')
        stats_tab.click()
        wanted_by = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text
        info_dict['Wanted By'] = (wanted_by)

        return info_dict

    def iterate_games(self): # open game pages and append game info to info_list. quit driver when complete. 
        time.sleep(2)
        links = self.game_links()
        for hyper in links:
            self.driver.get(hyper)
            self.info_list.append(self.get_info())
            time.sleep(2)
        self.info_list = sorted(self.info_list, key=lambda k: k['Rating'], reverse = True) # sort games by rating value, highest first
        print (self.info_list)
        self.driver.quit()


if __name__ == "__main__":
    scrape = Webscraper()
    scrape.open_website()


    

