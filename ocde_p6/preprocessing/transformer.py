#ocde_p6/preprocessing/transformer.py
"""Data transformation utilities for API inputs."""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

from ..utils.logger import get_logger
from ..validation.schemas import BuildingInput

logger = get_logger(__name__)

class DataTransformer:
    """Handles transformation of user input to model-ready format."""
    
    def __init__(self):
        self.feature_names = ['YearBuilt', 'FirstUseType']
    
    def transform_input(self, building_input: BuildingInput) -> pd.DataFrame:
        """Transform validated user input to model format.
        
        Args:
            building_input: Validated Pydantic model
            
        Returns:
            pandas DataFrame ready for model prediction
        """
        try:
            # Create DataFrame with expected feature names
            data = {
                'YearBuilt': [building_input.year_built],
                'FirstUseType': [building_input.first_use_type]
            }
            
            df = pd.DataFrame(data)
            
            logger.info(f"Transformed input: {data}")
            return df
            
        except Exception as e:
            logger.error(f"Error transforming input: {str(e)}")
            raise ValueError(f"Failed to transform input data: {str(e)}")
    
    def validate_feature_names(self, df: pd.DataFrame) -> bool:
        """Validate that DataFrame has expected feature names.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        expected_features = set(self.feature_names)
        actual_features = set(df.columns)
        
        if expected_features != actual_features:
            logger.warning(f"Feature mismatch. Expected: {expected_features}, Got: {actual_features}")
            return False
        
        return True

# Global instance
data_transformer = DataTransformer()

