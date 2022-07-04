from selenium import webdriver
from selenium.webdriver.common.by import By
import time

category = input("Please enter board game category. Ensure first letter of all words is capitalised: ")

def open_website(): #open website and accept cookies
    driver = webdriver.Chrome()
    URL = "https://boardgamegeek.com/"
    driver.get(URL)
    time.sleep(2)

    try:
        cookies_button = driver.find_element(By.XPATH, '//*[@id="c-p-bn"]') # accept all cookies button
        cookies_button.click()
    except:
        pass
    
    return driver

driver = open_website()
driver

def goto_categories(): #goto board game categories section of website
    time.sleep(2)
    browse_button = driver.find_element(By.XPATH, '/html/body/gg-app/div/gg-header/header/nav/div/div[1]/div/div[1]/ul/li[1]/button')
    browse_button.click()
    time.sleep(2)
    categories_atag = driver.find_element(By.XPATH, '/html/body/gg-app/div/gg-header/header/nav/div/div[1]/div/div[1]/ul/li[1]/div/div/div/div[1]/span[2]/a')
    link = categories_atag.get_attribute('href')
    driver.get(link)

    return driver

goto_categories()

def select_category(category): # select inputted category
    category = category
    time.sleep(2)
    link = driver.find_element(By.PARTIAL_LINK_TEXT, f"{category}")
    link.click()

    return driver

select_category(category)

def game_links():
    game_container = driver.find_element(By.XPATH, '//*[@class="rec-grid-overview"]') # element containing 6 top games
    game_list = game_container.find_elements(By.XPATH, './li') # list of games on page
    link_list = [] # will contain hyperlinks to top 6 games listed

    for game in game_list: #iterate through properties and get hyperlinks
        a_tag = game.find_element(By.TAG_NAME, 'a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list

game_links()

links = game_links()


    

