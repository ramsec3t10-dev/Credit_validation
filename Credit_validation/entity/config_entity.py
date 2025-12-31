from Credit_validation.constant import training_pipeline as tp
import os,sys
from datetime import datetime
from Credit_validation.exception.exception import logging

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime('_%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = tp.PIPELINE_NAME
        self.artifact_name = tp.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        logging.info("DATAINGESTIONCONFIG created")
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,tp.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_name = os.path.join(
            self.data_ingestion_dir,tp.DATA_INGESTION_FEATURE_STORE_NAME
        )
        self.training_file_path = os.path.join(
            self.data_ingestion_dir,tp.DATA_INGESTION_INGESTED_DIR,tp.TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,tp.DATA_INGESTION_INGESTED_DIR,tp.TEST_FILE_NAME
        )
        self.train_test_split_ratio:float = tp.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str = tp.DATA_INGESTION_COLLECTION_NAME
        self.database:str = tp.DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,training_pipeline_config :TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,tp.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir = os.path.join(self.data_validation_dir,tp.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir,tp.DATA_VALIDATION_INVALID_DIR)
        self.valid_training_file_path = os.path.join(self.valid_data_dir,tp.TRAIN_FILE_NAME)
        self.valid_testing_file_path = os.path.join(self.valid_data_dir,tp.TEST_FILE_NAME)
        self.invalid_training_file_path = os.path.join(self.invalid_data_dir,tp.TRAIN_FILE_NAME)
        self.invalid_testing_file_path = os.path.join(self.invalid_data_dir,tp.TEST_FILE_NAME)
        self.drift_report_file_path = os.path.join(self.data_validation_dir,tp.DATA_VALIDATION_DRIFT_REPORT_DIR,tp.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)