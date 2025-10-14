#ocde_p6/model/model_loader.py

"""Model loader for building energy prediction."""

import bentoml
import logging
from typing import Any

from ..utils.logger import get_logger
from ..utils.exceptions import ModelLoadError

logger = get_logger(__name__)

class ModelLoader:
    """Handles loading and management of the trained model."""
    
    def __init__(self):
        self._model = None
        self.model_name = "building_energy_rf_pipeline"
    
    def load_model(self) -> Any:
        """Load the BentoML saved model.
        
        Returns:
            Loaded model pipeline ready for prediction
            
        Raises:
            ModelLoadError: If model loading fails
        """
        if self._model is None:
            try:
                logger.info(f"Loading model: {self.model_name}")
                self._model = bentoml.sklearn.load_model(self.model_name)
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                raise ModelLoadError(f"Could not load model {self.model_name}: {str(e)}")
        
        return self._model
    
    def predict(self, input_data):
        """Make prediction using the loaded model.
        
        Args:
            input_data: Preprocessed input data for prediction
            
        Returns:
            Prediction result
        """
        model = self.load_model()
        try:
            prediction = model.predict(input_data)
            logger.info("Prediction completed successfully")
            return prediction
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise ModelLoadError(f"Prediction error: {str(e)}")

# Global instance
model_loader = ModelLoader()
