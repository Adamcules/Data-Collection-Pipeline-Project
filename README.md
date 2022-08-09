# Data-Collection-Pipeline-Project

An implementation of an industry grade data collection pipeline that runs scalably in the cloud.

## Milestone 1
Scraping website boardgamegeek.com (BGG). <br />
Chosen website as large amount of categorised data with statistics. <br />

## Milestone 2
Created scraper class (python file). <br />
Use Selenium webdriver (Chrome) to navigate through website and retrieve data. <br />
Code asks user for a particular category of board game and is returned info as a dictionary (with nested dictionaries) on the top 6 games (by rating) within that category: <br />

![Adventure Game Info](https://user-images.githubusercontent.com/106440366/178328806-115d4dcf-da1b-4333-b532-e3a13b0d4151.JPG)

## Milestone 3
Added method to collect game ID for each game as given by BGG (named BGG_ID). Used 'filter' function to extract the number only part of the game id from the web element text string.

Within the iterate_games method, added a UUID key to the game dictionary (info_dict) and generated a v4 UUID for each game within this method using the imported uuid module:

![UUID generation](https://user-images.githubusercontent.com/106440366/179084356-e5ef3c22-fa93-42ff-95a4-a85616e92162.JPG)

As such each game has two unique identification tags.

The dictionaries are stored locally as JSON files within a unique folder for each game (folder has name set to  game BGG_ID) and all within a parent folder called 'raw_data'. This is achieved by the method 'save_dict_records' and makes use of functionality from the imported os and json modules (e.g. 'os.mkdir' and 'json.dump' functions).

The game image files are downloaded and stored locally as jpeg files within an 'images' folder within the 'raw_data' folder. Each image has name set to game BGG_ID. The urllib module is imported for this purpose and the 'urllib.request.urlretrieve' function used.

Added 'iterate_categories' function and altered other parts of the code so that the user can now decide to scrape all categories and return info on the top 6 games within each category. As some games fall within multiple categories, the code checks whether the game has already been scraped by checking whether its BGG_ID value exists within 'self.info_list'and, if so, it simply appends the current category to the 'category' value of the game (which is created as a list and can thus hold multiple values). 

## Milestone 4
Optimised code:
Extracted BGG_ID value in iterate_game method by using .split() function on the game URL in order to determine BGG_ID more reliably. The function now checks whether BGG_ID exists within game_dict before making driver goto game page and if so, simply appends the current category name as a value to the game's [Category] key within game_dict:

![Check bgg_id in game_dict](https://user-images.githubusercontent.com/106440366/183736925-9ca15af0-944c-4bb4-81b9-8208c3806e52.JPG)

Added docstrings to all functions


Example text below
************************************


Does what you have built in this milestone connect to the previous one? If so explain how. What technologies are used? Why have you used them? Have you run any commands in the terminal? If so insert them using backticks (To get syntax highlighting for code snippets add the language after the first backticks).

Example below:

/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
The above command is used to check whether the topic has been created successfully, once confirmed the API script is edited to send data to the created kafka topic. The docker container has an attached volume which allows editing of files to persist on the container. The result of this is below:
"""Insert your code here"""
Insert screenshot of what you have built working.

Milestone n
Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

Conclusions
Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?
