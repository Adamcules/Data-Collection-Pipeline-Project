from selenium import webdriver
from selenium.webdriver.common.by import By
import time

category = input("Please enter board game category. Ensure first letter of all words is capitalised: ")

def open_website(): #open website and accept cookies
    driver = webdriver.Chrome()
    URL = "https://boardgamegeek.com/browse/boardgamecategory"
    driver.get(URL)
    time.sleep(2)

    try:
        cookies_button = driver.find_element(By.XPATH, '//*[@id="c-p-bn"]') # accept all cookies button
        cookies_button.click()
    except:
        pass
    
    return driver

driver = open_website()

def select_category(category): # select inputted category
    category = category
    time.sleep(2)
    link = driver.find_element(By.LINK_TEXT, f"{category}")
    link.click()

    return driver

select_category(category)

def game_links(): # get links to top 6 games for selected category
    time.sleep(2)
    game_container = driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing 6 top games
    game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
    link_list = [] # will contain hyperlinks to top 6 games listed

    for game in game_list: #iterate through games and get hyperlinks
        a_tag = game.find_element(By.TAG_NAME, 'a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list

game_links()

links = game_links()
info_list = [] 

def get_info():
    info_dict = {'Name': "", 'Year': "", 'Rating': "", 'Number of Players': "", 'Age': "", 'Wanted By': ""}
    name = driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/a').text
    info_dict['Name'] = (name)
    year = driver.find_element(By.XPATH, '//div[@class="game-header-title-info"]/h1/span').text
    info_dict['Year'] = (year)
    ratings_tab = driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[2]')
    ratings_tab.click()
    rating = driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/ratings-module/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/ul/li[1]/div[2]').text
    info_dict['Rating'] = (rating)
    player_from = driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]').text
    try:
        player_to = driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]').text
    except:
        player_to = ""
    num_players = player_from + player_to
    info_dict['Number of Players'] = (num_players)
    age = driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/ng-include/div/div[2]/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span').text
    info_dict['Age'] = (age)
    stats_tab = driver.find_element(By.XPATH, '//*[@id="primary_tabs"]/ul/li[7]')
    stats_tab.click()
    wanted_by = driver.find_element(By.XPATH, '//*[@id="mainbody"]/div[2]/div/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/div/div[3]/div[2]/div[2]/ul/li[5]/div[2]/a').text
    info_dict['Wanted By'] = (wanted_by)

    return info_dict

def iterate_games(): 
    for hyper in links:
        driver.get(hyper)
        info_list.append(get_info())
        time.sleep(3)

iterate_games()  

info_list = sorted(info_list, key=lambda k: k['Rating'], reverse = True)
print (info_list)




    

