from Credit_validation.exception.exception import CreditDataException
from Credit_validation.logging.logger import logging
import os,sys,json
import pandas as pd
import pymongo
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")

class CreditDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CreditDataException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            record = data.to_dict(orient="records")
            logging.info("CSV converted to json")
            return record
        except Exception as e:
            logging.info("Failed to convert CSV to json")
            raise CreditDataException(e,sys)
        
    def insert_mongo_db(self,record,database,collections):
        try:
            self.mongo_db_client = pymongo.MongoClient(mongo_db_url)
            db = self.mongo_db_client[database]
            col = db[collections]
            logging.info("Records inserted into mongo_db")
            result = col.insert_many(record,ordered=False)

            return len(result.inserted_ids)
        except Exception as e:
            raise CreditDataException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = os.path.join("Credit_data","cleaned_loan_db.csv")
    DATABASE = "RAM_AI"
    COLLECTION = "CreditValid"
    credobj = CreditDataExtract()
    records = credobj.csv_to_json(file_path=FILE_PATH)
    print(f"total records read from csv : {len(records)}")
    no_of_records = credobj.insert_mongo_db(record=records,database=DATABASE,collections=COLLECTION)
    print(f"No of records inserted in mongdb is {no_of_records} ")


        