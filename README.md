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
Changed game_list type from list to dictionary (renamed to game_dict) in order to speed up iteration checks.

Extracted BGG_ID value in iterate_game method by using .split() function on the game URL in order to determine BGG_ID more reliably. The function now checks whether BGG_ID exists within game_dict before making driver goto game page and if so, simply appends the current category name as a value to the game's [Category] key within game_dict:

![Check bgg_id in game_dict](https://user-images.githubusercontent.com/106440366/183736925-9ca15af0-944c-4bb4-81b9-8208c3806e52.JPG)

Restructured code to containerise code within 3 classes: Webscraper, BGGScraper and LocalSave.
Webscraper class initialises general Chrome webdriver. BGGScraper contains specific methods for scraping the BGG website and LocalSave contains methods for saving scraped info and image files in local folders. 

Refactored several methods within the BGGScraper class so they no longer call to another function within the class and generally return a value instead. Previously the class would run when initiated and the logic flowed by functions calling to the next function in the flow. Instead, the 'run()' function was added which now handles the logic flow and is called from outside the class:

![run() function](https://user-images.githubusercontent.com/106440366/187181663-79af97ad-453b-44ce-89ea-d835db8c387c.JPG)

## Milestone 5
Added docstrings to all functions.

Created test_webscraper.py file which contains unittests for 3 of the public functions within the BGGScraper class: select_category(), iterate_categories() and iterate_games().

## Milestone 6

Created an S3 bucket (data-collection-project-bucket) on Amazon Web Services (AWS). Configured development environment using the 'awscli' package to enable local computer to communicate with AWS account.

Installed and imported the boto3 package enabling boto3 client to upload and download files to/from the S3 bucket. Used the policy generator on AWS to create public access policy for the S3 bucket, enabling free access to the files stored in the bucket.

Wrote script containing two classes that make use of a boto3 client to either upload files to the S3 bucket from locally saved files, or to write files directly to the S3 bucket from a passed dictionary (in the case of this project the passed dictionary would be generated by the boardgamegeek webscraper class (BGGScraper).
This script successfully enabled all scraped data, including image data to be uplaoded to S3 bucket.

Created a postgres RDS database on AWS (data-collection-project-rds). Created a security group on AWS allowing local machine to connect to the RDS ports.
Installed and imported SQLALchemy to establish connection to RDS database (create_engine method from SQLAlchemy). Installed and imported Psycopg2 as the database API, enabling SQL functionality within Python script.

Wrote script containing a class to generate a dataframe using Pandas from a passed dictionary. A second class then contains methods for exporting the dataframe as an SQL table to the RDS database.
This script successfully enabled scraped data generated from the BGG webscraper to be uploaded to the RDS database.

Split Python code into separate modules: 'main.py', 'webscraper.py', 'local_save.py', 'export_to_S3.py', 'export_to_rds.py' and 'test_webscraper.py'.<br />
'webscraper' module: contains classes/methods for initialising a webdriver and scraping the BGG website.<br />
'local_save' module: contains classes/methods for saving scraped data as .JSON and .JPG files to local folders.<br />
'export_to_S3' module: contains classes/methods for exporting scraped data as .JSON and .JPG files to S3 bucket.<br />
'export_to_rds' module: contains classes/methods for exporting scraped data to an RDS database.<br />
'main' module: imports the other above modules and provides the logic for running the webscraper and various data storage options, giving options to the user as to what they want to scrape and how they want to store the scraped data.<br />
<br />
'test_webscraper' module: contains unittest classes/methods for testing the correct functionality of the webscraper module.


## Milestone 7
Checked webscraper collected all required data without failing (over 300 records when scraping all game categories on BGG website).

Unittests on webscraper public methods passed successfully.

Included in the 'iterate_games' method of the BGGScraper class is a check as to whether a particular game page has already been scraped. It does this by checking whether the BGG_ID value already exists in the 'game_dict' dictionary that 'iterate_games' method generates. If the game already exists in the dictionary, the webdriver does not go to the game page again to prevent wasted resources on rescraping.

To prevent duplicate records being generated in the RDS database, the RDSExport class in the 'export_to_rds' module contains a method called 'clean_table' which gets the current table from RDS, concatenates it with the dataframe created from the newly scraped data, then uses the Pandas method 'drop_duplicates' to remove duplicated records based on the 'BGG_ID' value of games:

![clean_table() function](https://user-images.githubusercontent.com/106440366/188142084-a3ed240f-1055-4ade-963f-6a5cd9d40c03.JPG)

This new dataframe cleaned of duplicates is then uploaded back to the RDS database as an SQL table.

## Milestone 8

Added the import of 'Options' from selenium.webdriver.chrome.options to webscraper.py in order to set options necessary for the Webdriver class to run the selenium webdriver within a Docker container. The options set were 'headless', 'no-sandbox' and 'disable-dev-shm-usage':

![image](https://user-images.githubusercontent.com/106440366/192865717-544d7401-ed18-4f63-bc43-f3e50f741fc3.png)

Created a Dockerfile using the base image python:3.10. This file contains commands to install all the necessary dependencies needed to successfully run the webscraper within a Docker container, including a number of Python packages which are installed from the 'requirements.txt' file using the pip install -r option.

Dockerfile:<br />
![image](https://user-images.githubusercontent.com/106440366/192869118-46f358b0-797c-475c-b4bc-6b24a5b783a8.png)

Requirements file:<br />
![image](https://user-images.githubusercontent.com/106440366/192869294-fc1633ba-76d1-4e8c-804a-bf61cc2df600.png)

Initially built Docker image using docker build command on local machine and successfully ran webscraper within a Docker container.

The Docker image was then pushed to Docker Hub.

A new EC2 instance was created on AWS and the Docker image pulled from Docker Hub onto this instance. 

On the local machine, the boto3 client retrieves the required aws_access_key_id and aws_secret_access_key it needs to access the S3 bucket from the .aws folder found in the home directory. This is not available within the EC2 instance and therefore when running the Docker image from the EC2 instance, the Docker container was not able to successfully upload data to the S3 bucket.

This was fixed by editing the .bash_profile file within the EC2 instance to set the ID and Key as environment variables. These are then passed as environment variables to the Docker container when it is run using the following command:

docker run -e aws_access_key_id=$aws_access_key_id -e aws_secret_access_key=$aws_secret_access_key <image_name>

The code within the file 'export_to_S3.py' was modified such that the boto3 client now found this ID and Key info from the relevant environment variables:

![image](https://user-images.githubusercontent.com/106440366/192878454-8b30e349-5b04-4b93-bd12-b39f28939412.png)

This enabled the webscraper to run successfully as a Docker container from the EC2 instance and was able to export data to both the S3 bucket and RDS database.

The next step was to schedule the scraper to run periodically on the EC2 instance. 

Firstly, the code in several of the modules was modified to remove any required user inputs, enabling the webscraper to run periodically without the need for a user to be present.

Cron was used for the job scheduling. Initially this was attempted by scheduling Cron to run the Docker image every 5 minutes using the below Crontab schedule:

![image](https://user-images.githubusercontent.com/106440366/192881026-163b1bf5-8809-4698-acc7-c5d4fbf66a19.png)

However, this did not successfully pass the environment variables to the Docker container and thus export of data to the S3 bucket was not successful.

To fix this, a .sh file was created (cron_docker_run.sh) containing a script for the above command defined as a bash command:

![image](https://user-images.githubusercontent.com/106440366/192883470-e1c45cf6-b11b-427d-b2bf-569af3dac3fb.png)

Crontab could then be used to run this script by setting BASH_ENV equal to the environment variables within the .bash_profile file:

![image](https://user-images.githubusercontent.com/106440366/192884326-a47051f7-8558-47ec-9f31-e223bcc146f6.png)

This successfully ran the Docker image every 5 minutes and the Docker containers successfully exported the relevant data to the S3 bucket and RDS database.







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
