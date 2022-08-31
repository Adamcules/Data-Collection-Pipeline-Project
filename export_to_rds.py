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
    This class takes a dataframe and exports it to an AWS RDS database.

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
    
    def export_to_rds(self):
        """
        This function exports the dataframe as an sql table to RDS
        """
        self.data_frame.to_sql('game_dataset', self.engine, if_exists='replace')


def run(game_dict):
    """
    This function contains the run logic for the module
    """
    df = DataFrame(game_dict)
    data_frame = df.create_data_frame()
    export = RDSExport(data_frame)
    export.export_to_rds()




