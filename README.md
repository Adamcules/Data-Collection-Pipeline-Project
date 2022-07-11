# Data-Collection-Pipeline-Project

An implementation of an industry grade data collection pipeline that runs scalably in the cloud.

## Milestone 1
Scraping website boardgamegeek.com (BGG). <br />
Chosen website as large amount of categorised data with statistics. <br />

## Milestone 2
Created scraper class (python file). <br />
Use Selenium webdriver (Chrome) to navigate through website and retrieve data. <br />
Code asks user for a particular category of board game and is returned info as a list (with nested dictionaries) on the top 6 games (by rating) within that category: <br />

![Adventure Game Info](https://user-images.githubusercontent.com/106440366/178328806-115d4dcf-da1b-4333-b532-e3a13b0d4151.JPG)



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
