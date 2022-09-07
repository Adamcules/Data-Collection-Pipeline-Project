"""
This module contains a class for saving python dictionary and image data in a local folder
"""

import json 
import os
import urllib.request

class LocalSave:

    """
    This class contains methods to save information passed to it as a python dictionary within local folders.

    A user can enter a directory to store all the files or use the default directory.

    Attributes:
        game_dict: dictionary passed to class containing data to save to local files
        save_folder: target directory of local folder to save files 
    """
    
    def __init__(self, game_dict: dict):
        self.game_dict = game_dict
        self.save_folder = str(input('Please enter directory for local save folder. Leave blank for default: '))
        if self.save_folder == "":
            self.save_folder = '/Users/adam-/OneDrive/Desktop/AI_Core/Data-Collection-Pipeline-Project/raw_data' # default directory used if user does not enter alternative 

    
    def save_dict_records(self):
        """
        This function saves dictionary values as JSON files within a local directory folder. 
        
        The function attempts to create a file called 'raw_data' (unless the user has specified another directory). 
        The function then iterates through each item in the dictionary passed to it, checks whether a folder has already been created for that
        item and, if not, creates a folder for it within the parent folder, naming the folder after the dictionary key name.
        It then writes a JSON file within that folder called 'data.json' which contains the value information for that dictionary item.
        """
        if not os.path.exists(self.save_folder): # check whether directory already exists
            os.mkdir(self.save_folder) # create new folder
        else:
            print ("local save directory already exists.")
        for game in self.game_dict: # iterate through dictionary passed to instance of class
            strip_special_characters = ''.join(filter(str.isalnum, self.game_dict[game]['Name'])) # remove special characters from game name to guarantee valid file name
            folder_name = game + ' - ' + strip_special_characters
            directory = os.path.join(self.save_folder, folder_name) # create directory name for dictionary item
            try:
                os.mkdir(directory) # check whether folder already exists for dictionary item and create if it doesn't
            except:
                print (f"game directory {folder_name} already exists.")
            data_file = os.path.join(directory, 'data.json') # create file name for saved data 
            with open(data_file, 'w') as fp: # write json file containing value info for dictionary item
                json.dump(self.game_dict[game], fp)


    def save_game_images(self): 
        """
        This function creates a file called 'images' within the parent folder created by self.save_dict_records and saves image files found within dictionary passed to instance of class  
        
        NB: For this function to work, the dictionary passed to the class must consist of nested dictionaries containing the key 'Images'.

        The function first checks whether a folder called 'images' has been created within the parent folder. If not, it creates this folder.
        The function then iterates through the dictionary passed to the class instance. For each item, it obtains the url to the image file
        stored under the nested dictionary key 'Images' and saves the image within the 'images' folder using urllib.request library and
        .urlretrieve function. The file is named after the key name.
        """
        images = os.path.join(self.save_folder, 'images') # create 'images' folder name
        if not os.path.exists(images): # check if folder already exists
            os.mkdir(images) # create folder
        else:
            print ('images directory already exists.')
        for game in self.game_dict:
            strip_special_characters = ''.join(filter(str.isalnum, self.game_dict[game]['Name'])) # remove special characters from game name to guarantee valid file name
            file_name = game + ' - ' + strip_special_characters + '.jpg'
            url = self.game_dict[game]['Image'] # get url for image
            image_file = os.path.join(images, file_name) # create directory for image file
            urllib.request.urlretrieve(url, image_file) # save image file in 'images' folder
        
    def run(self):
        """
        This function contains the logic for running an instance of Local_Save class.

        The function calls to self.save_dict_recrods and self.save_game_images in turn.
        """
        self.save_dict_records()
        self.save_game_images()