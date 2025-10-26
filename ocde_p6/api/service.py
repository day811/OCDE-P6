#ocde_p6/api/services.py

"""BentoML service for building energy prediction API."""

import bentoml


import pandas as pd
import numpy as np
from typing import Dict, Any
import traceback

from ..model.model_loader import model_loader
from ..preprocessing.transformer import data_transformer
from ..validation.schemas import BuildingInput, PredictionResponse, ErrorResponse
from ..utils.logger import get_logger
from ..utils.exceptions import ModelLoadError, ValidationError, PredictionError

logger = get_logger(__name__)

# Create BentoML service
@bentoml.service(
    name="building_energy_prediction",
    resources={"cpu": "2"},
    traffic={"timeout": 30}
)
class BuildingEnergyService:
    """Service for predicting building energy consumption."""
    
    def __init__(self):
        """Initialize the service."""
        logger.info("Initializing BuildingEnergyService")
        # Model will be loaded on first prediction
    
    @bentoml.api
    def predict(self, input_data: BuildingInput) -> Dict[str, Any]:
        """Predict building energy consumption.
        
        Args:
            input_data: Validated building characteristics (BentoML handles Pydantic validation)
            
        Returns:
            JSON response with prediction or error
        """
        try:
            logger.info(f"Received input: {input_data}")
#            building_input = BuildingInput(**input_data)
            
            # Transform input data
            df_input = data_transformer.transform_input(input_data)
            
            # Make prediction
            prediction = model_loader.predict(df_input)
            
            # Prepare response
            response = PredictionResponse(
                prediction=round(np.expm1(float(prediction[0])),2),
                input_data=input_data,
                status="success"
            )
            
            logger.info(f"Prediction successful: {prediction[0]}")
            return response.model_dump()
            
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            error_response = ErrorResponse(
                error=f"Input validation failed: {str(e)}",
                status="validation_error"
            )
            return error_response.model_dump()
            
        except (ModelLoadError, PredictionError) as e:
            logger.error(f"Model error: {str(e)}")
            error_response = ErrorResponse(
                error=f"Model error: {str(e)}",
                status="model_error"
            )
            return error_response.model_dump()
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            error_response = ErrorResponse(
                error=f"Internal server error: {str(e)}",
                status="internal_error"
            )
            return error_response.model_dump()
    
    @bentoml.api
    def health(self) -> Dict[str, str]:
        """Health check endpoint.
        
        Returns:
            JSON response indicating service health
        """
        try:
            # Try to load model to verify it's accessible
            model_loader.load_model()
            return {
                "status": "healthy",
                "model": "loaded",
                "message": "Service is running normally"
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "model": "error",
                "message": f"Service error: {str(e)}"
            }