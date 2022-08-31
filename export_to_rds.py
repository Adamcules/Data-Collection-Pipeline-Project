import pandas as pd
import psycopg2
from sqlalchemy import create_engine


class DataFrame():
    def __init__(self, game_dict: dict):
        self.game_dict = game_dict
    
    def create_data_frame(self):
        data_frame = pd.DataFrame(self.game_dict)
        transposed_frame = data_frame.transpose()
        return transposed_frame


class RDSExport():
    def __init__(self, data_frame):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'data-collection-project-rds.cnyhboqptnp4.eu-west-2.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'adamus83'
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect()
        self.data_frame = data_frame
    
    def export_to_rds(self):
        self.data_frame.to_sql('game_dataset', self.engine, if_exists='replace')


def run(game_dict):
    df = DataFrame(game_dict)
    data_frame = df.create_data_frame()
    export = RDSExport(data_frame)
    export.export_to_rds()




