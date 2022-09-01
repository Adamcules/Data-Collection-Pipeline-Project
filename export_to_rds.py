"""
This module contains two classes. One to create a data_frame from passed dictionary (DataFrame) and one to export the 
dataframe as an SQL table to an AWS RDS database.
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


class DataFrame():
    """
    This class takes a dictionary and returns a dataframe using pandas.

    Attributes:
        game_dict: dictionary passed to class
    """
    def __init__(self, game_dict: dict):
        self.game_dict = game_dict
    
    def create_data_frame(self):
        data_frame = pd.DataFrame(self.game_dict) # create initial dataframe
        transposed_frame = data_frame.transpose() # swap columns to rows and rows to columns
        return transposed_frame


class RDSExport():
    """
    This class takes a dataframe and exports it to an AWS RDS database, concatenating it to an existing table if found.

    Attributes:
        engine: sqlalchemy engine to connect to RDS
        data_frame: dataframe passed to class
    """
    def __init__(self, data_frame):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'data-collection-project-rds.cnyhboqptnp4.eu-west-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'adamus83'
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}") # initialise sqlalchemy engine
        self.engine.connect() # connect to RDS
        self.data_frame = data_frame # dataframe passed to class
    
    def clean_table(self):
        """
        This function gets the existing table from RDS, concatenates the new dataframe to it and removes duplicates
        """
        get_table = pd.read_sql_table('game_dataset', self.engine) # get existing table from RDS
        removed_index = get_table.set_index('index') # remove generic index column from RDS table as it does not exist in new dataframe to be concatenated
        appended_table = pd.concat([removed_index, self.data_frame]) # concatenate new dataframe to old table 
        appended_table.drop_duplicates(subset='BGG_ID', keep='last', inplace=True) # remove duplicates found in newly concatenated table based on their BGG_ID
        return appended_table
    
    def export_to_rds(self, appended_table):
        """
        This function exports the dataframe as an sql table to RDS
        """
        appended_table.to_sql('game_dataset', self.engine, if_exists='replace')


def run_rds_export(game_dict):
    """
    This function contains the run logic for the module
    """    
    df = DataFrame(game_dict)
    data_frame = df.create_data_frame()
    export = RDSExport(data_frame)
    export.export_to_rds(export.clean_table())



