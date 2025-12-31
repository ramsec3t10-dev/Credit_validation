from Credit_validation.exception.exception import CreditDataException
from Credit_validation.logging.logger import logging

from Credit_validation.entity.artifact_entity import DataIngestionArtifact
from Credit_validation.component.data_ingestion import Data_Ingestion
from Credit_validation.entity.config_entity import (TrainingPipelineConfig,DataIngestionConfig)

import os,sys
 
try:
    trainingpipelineconfig = TrainingPipelineConfig()
    logging.info("Data ingestion has started")
    data_ingestion_congif = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
    data_ingestion = Data_Ingestion(data_ingestion_config=data_ingestion_congif)
    logging.info("Data ingestion is over")
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)
except Exception as e:
    raise CreditDataException(e,sys)