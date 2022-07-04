from selenium import webdriver
from selenium.webdriver.common.by import By
import time

num_pages = int(input("Please enter the number of pages you wish to scrape:"))

def load_and_accept_cookies() -> webdriver.Chrome:

    driver = webdriver.Chrome() 
    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
    try:
        driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="save"]')
        accept_cookies_button.click()
    except:
        pass # If there is no cookies button, we won't find it, so we can pass

    return driver

def get_links(driver: webdriver.Chrome) -> list:

    prop_container = driver.find_element(By.XPATH, '//*[@class="css-1itfubx e1c0stq80"]') # find div tag containing all property listings

    prop_list = prop_container.find_elements(By.XPATH, './div') # list of properties on page
    link_list = [] # will contain hyperlinks to all listed properties

    for property in prop_list: #iterate through properties and get hyperlinks
        a_tag = property.find_element(By.TAG_NAME, 'a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list
    
big_link_list = []
driver = load_and_accept_cookies() 

for i in range (num_pages): # collect links from number of pages entered by user
    big_link_list.extend(get_links(driver))
    time.sleep(2)
    next_button = driver.find_element(By.XPATH, '//a[@class="eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"]')
    next_button.click()

driver.quit()

def get_prop_info(): #get price and address info from property
    time.sleep(1)
    try:
        driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="save"]')
        accept_cookies_button.click()
    except:
        pass # If there is no cookies button, we won't find it, so we can pass
    dict_prop_info = {'Price': [], 'Address': []}
    price = driver.find_element(By.XPATH, '//*[@data-testid="price"]').text
    dict_prop_info['Price'].append(price)
    address = driver.find_element(By.XPATH, '//*[@data-testid="address-label"]').text
    dict_prop_info['Address'].append(address)
    
    return dict_prop_info

info_list = []

for hyper in big_link_list:
    driver = webdriver.Chrome()
    driver.get(hyper)
    info_list.append(get_prop_info())
    driver.quit()

print (f'There are {len(big_link_list)} properties on these pages')
print (info_list)