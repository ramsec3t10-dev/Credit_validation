from Credit_validation.entity.artifact_entity import DataIngestionArtifact
from Credit_validation.entity.config_entity import DataIngestionConfig

from Credit_validation.exception.exception import CreditDataException
from Credit_validation.logging.logger import logging

from sklearn.model_selection import train_test_split
import os,sys,pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

class Data_Ingestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditDataException(e,sys)
        
    def Mongo_collection_dataframe(self):
        try:
            database = self.data_ingestion_config.database
            collections = self.data_ingestion_config.collection_name
            self.mongo_db_client = pymongo.MongoClient(mongo_db_url)
            collection = self.mongo_db_client[database][collections]
            df = pd.DataFrame(list(collection.find()))

            if"_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True)
            df.replace({"na":np.nan},inplace=True)

            return df
        except Exception as e:
            raise CreditDataException(e,sys)
        
    def feature_data_store(self,dataframe : pd.DataFrame):
        try:
            feature_file_path = self.data_ingestion_config.feature_store_name
            feature_dir_name = os.path.dirname(feature_file_path)
            os.makedirs(feature_dir_name,exist_ok=True)
            dataframe.to_csv(feature_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise CreditDataException(e,sys)
        
    def split_train_test_data(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info("train and test sets created")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,header = True)
            logging.info("Exported data to training set")
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index = False,header = True)
            logging.info("Exported data to testing set")           
            
        except Exception as e:
            raise CreditDataException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.Mongo_collection_dataframe()
            dataframe = self.feature_data_store(dataframe=dataframe)
            self.split_train_test_data(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact

        except Exception as e:
            raise CreditDataException(e,sys)