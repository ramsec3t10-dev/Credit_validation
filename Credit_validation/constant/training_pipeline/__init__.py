import os,sys
import pandas as pd
import numpy as np
from datetime import datetime

"""This contains constants for training pipeline
    """
TARGET_COLUMN = "loan_status"
PIPELINE_NAME :str = "CreditValidation"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "cleaned_loan_db.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME

"""
    

DATA_INGESTION_COLLECTION_NAME: str = "CreditValid"
DATA_INGESTION_DATABASE_NAME: str = "RAM_AI"
DATA_INGESTION_DIR_NAME: str = "Data_Ingestion"
DATA_INGESTION_FEATURE_STORE_NAME: str = "Feature_Store"
DATA_INGESTION_INGESTED_DIR: str = "Ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float= 0.3

"""
Data Validation related constants start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "Data_Validation"
DATA_VALIDATION_VALID_DIR: str = "Validated"
DATA_VALIDATION_INVALID_DIR: str = "Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"