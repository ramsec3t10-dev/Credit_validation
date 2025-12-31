import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

from Credit_validation.exception.exception import CreditDataException
from Credit_validation.entity.artifact_entity import DataValidationArtifact
from Credit_validation.entity.config_entity import DataValidationConfig
from Credit_validation.logging.logger import logging
from Credit_validation.constant.training_pipeline import SCHEMA_FILE_PATH
from Credit_validation.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:

    def __init__(self, data_ingestion_artifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- UTIL --------------------

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- COLUMN VALIDATION --------------------

    def validate_no_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            required_columns = (
                list(self.schema_config["numerical_columns"].keys())
                + list(self.schema_config["ordinal_categorical_columns"].keys())
                + list(self.schema_config["nominal_categorical_columns"].keys())
                + [self.schema_config["target_column"]["name"]]
            )

            missing = set(required_columns) - set(df.columns)

            if missing:
                logging.error(f"Missing required columns: {missing}")
                return False

            logging.info("All required columns are present")
            return True

        except Exception as e:
            raise CreditDataException(e, sys)


    # -------------------- NUMERICAL --------------------

    def validate_numerical_columns(self, df: pd.DataFrame) -> bool:
        try:
            for col in self.schema_config["numerical_columns"].keys():
                if not pd.api.types.is_numeric_dtype(df[col]):
                    logging.error(f"Non-numeric column: {col}")
                    return False
            return True
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- ORDINAL --------------------

    def validate_ordinal_columns(self, df: pd.DataFrame) -> bool:
        try:
            for col, rules in self.schema_config["ordinal_categorical_columns"].items():
                allowed = rules.get("allowed_values", [])
                if allowed and not df[col].dropna().isin(allowed).all():
                    logging.error(f"Invalid ordinal values in {col}")
                    return False
            return True
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- NOMINAL --------------------

    def validate_nominal_columns(self, df: pd.DataFrame) -> bool:
        try:
            for col, rules in self.schema_config["nominal_categorical_columns"].items():
                allowed = set(rules.get("allowed_values", []))
                observed = set(df[col].dropna().unique())

                if not observed.issubset(allowed):
                    logging.error(
                        f"Unexpected categories in {col}: {observed - allowed}"
                    )
                    return False
            return True
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- TARGET --------------------

    def validate_target(self, df: pd.DataFrame) -> bool:
        try:
            target_col = self.schema_config["target_column"]["name"]
            allowed = self.schema_config["target_column"].get("allowed_values", [])

            if allowed and not df[target_col].dropna().isin(allowed).all():
                logging.error("Invalid target values detected")
                return False
            return True
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- DRIFT --------------------

    def detect_data_drift(self, base_df, curr_df, threshold=0.05) -> bool:
        try:
            report = {}
            drift_found = False

            for col in self.schema_config["numerical_columns"].keys():
                ks = ks_2samp(
                    base_df[col].dropna(),
                    curr_df[col].dropna()
                )
                drift = ks.pvalue < threshold
                report[col] = {
                    "p_value": float(ks.pvalue),
                    "drift_detected": drift
                }
                if drift:
                    drift_found = True

            report["overall_drift_status"] = not drift_found

            os.makedirs(
                os.path.dirname(self.data_validation_config.drift_report_file_path),
                exist_ok=True
            )

            write_yaml_file(
                self.data_validation_config.drift_report_file_path,
                report
            )

            return not drift_found
        except Exception as e:
            raise CreditDataException(e, sys)

    # -------------------- PIPELINE --------------------

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            validations = [
                ("columns", self.validate_no_of_columns),
                ("numerical", self.validate_numerical_columns),
                ("ordinal", self.validate_ordinal_columns),
                ("nominal", self.validate_nominal_columns),
                ("target", self.validate_target),
            ]

            for name, validate in validations:
                logging.info(f"Running {name} validation on TRAIN")
                if not validate(train_df):
                    raise Exception(f"Train {name} validation failed")

                logging.info(f"Running {name} validation on TEST")
                if not validate(test_df):
                    raise Exception(f"Test {name} validation failed")

            drift_status = self.detect_data_drift(train_df, test_df)

            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_training_file_path),
                exist_ok=True
            )

            train_df.to_csv(self.data_validation_config.valid_training_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_testing_file_path, index=False)

            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_training_file_path,
                valid_test_file_path=self.data_validation_config.valid_testing_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise CreditDataException(e, sys)
