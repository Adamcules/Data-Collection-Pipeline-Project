"""
This module contains two classes, S3ExporterLocal and S3ExporterDirect. 

They upload data from local folders or from a passed dictionary respectively to an S3 bucket
"""

import boto3
import json
import os
import requests

class S3ExporterLocal:
    """
    This class contains a method to export local files to an S3 Bucket

    Attributes:
        local_path: local folder containing files to upload
        bucket_name: name of target S3 bucket to upload to
        s3_client: instance of boto3 S3 client
    """
    def __init__(self, local_path: str, bucket_name: str) -> None:
        self.local_path = local_path # defines local folder containing files to export
        self.bucket_name = bucket_name # name of target S3 bucket to export to
        self.s3_client = boto3.client('s3') # initialise S3 boto3 client

    def export_to_bucket(self):
        """
        This function iterates through a local folder and uploads the files to an S3 bucket
        """
        for root,dirs,files in os.walk(self.local_path): # iterate through folders and files in local directory
            for file in files: # iterate through source files
                parse_root = root.split('\\')[1] # get parent folder name of file
                if parse_root == 'images': # checks if file is in local 'images' folder
                    file_name = file.removesuffix('.jpg') + ' - ' + 'image.jpg' # set upload filename
                    self.s3_client.upload_file(os.path.join(root, file), self.bucket_name, file_name) # upload file to S3 bucket
                else:
                    file_name = parse_root + ' - ' + file # set upload filename
                    self.s3_client.upload_file(os.path.join(root, file), self.bucket_name, file_name) # upload file to S3 bucket


class S3ExporterDirect():
    """
    This class uploads data from a passed python dictionary to an S3 bucket

    Attributes:
        bucket_name: name of target S3 bucket to upload to
        game_dict: dictionary passed to class containing data to upload
        s3_client: instance of boto3 S3 client
    """
    def __init__(self, bucket_name: str, game_dict: dict) -> None:
        self.bucket_name = bucket_name # name of target S3 bucket to export to
        self.game_dict = game_dict # passed dictionary
        self.s3_client = boto3.client('s3') # initialise S3 boto3 client
    
    def export_json(self):
        """
        This function uploads dictionary info as a JSON file
        """
        for game in self.game_dict: # iterate through dictionary
            file_name = game + ' - ' + self.game_dict[game]['Name'] + ' - ' + 'data.json' # set target file name
            json_object = self.game_dict[game] # json data to upload: value of dictionary key 
            self.s3_client.put_object(Body=json.dumps(json_object), Bucket=self.bucket_name, Key=file_name) # upload file to S3 bucket
    
    def export_image(self):
        """
        This function uploads image file nested in dictionary.

        NB: function will only work if dictionary has nested dictionary with key named 'Image'
        """
        for game in self.game_dict: # iterate through dictionary
            file_name = game + ' - ' + self.game_dict[game]['Name'] + ' - ' + 'image.jpg' # set target file name
            url = self.game_dict[game]['Image'] # get image url
            response = requests.get(url, stream=True) # get image data
            image = response.content # get response content (returns content as byte array which is required format for 'Body' argument in .put_object function below)
            self.s3_client.put_object(Body=image, Bucket=self.bucket_name, Key=file_name) # upload file to S3 bucket