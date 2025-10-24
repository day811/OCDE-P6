#ocde_p6/api/service.py

"""BentoML service for building energy prediction API."""

import bentoml
import pandas as pd
from typing import Dict, Any, Optional, Annotated
import traceback
from fastapi import Query

from ..model.model_loader import model_loader
from ..preprocessing.transformer import data_transformer
from ..validation.schemas import BuildingInput, PredictionResponse, ErrorResponse
from ..utils.enums import FirstUseTypeEnum, SecondLargestPropertyUseTypeEnum
from ..utils.logger import get_logger
from ..utils.config import config
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
    
    @bentoml.api(route="/predict")
    def predict(
        self,
        first_use_type: FirstUseTypeEnum = Annotated(
            ...,
            description="First largest property use type"
        ),
        second_largest_property_use_type: Optional[SecondLargestPropertyUseTypeEnum] = Annotated(
            None,
            description="Second largest property use type"
        ),
        multiple_use_type: int = Annotated(
            1,
            ge=1,
            le=10,
            description="Number of different property use types"
        ),
        sum_largest_gfa: float = Annotated(
            ...,
            ge=0,
            description="Three largest property use type GFA in square feet"
        ),
        use_steam: bool = Annotated(
            False,
            description="Building uses steam"
        ),
        use_gas: bool = Annotated(
            False,
            description="Building uses natural gas"
        ),
        number_of_floors: float = Annotated(
            ...,
            ge=1,
            le=100,
            description="Number of floors"
        ),
        number_of_buildings: float = Annotated(
            1.0,
            ge=1,
            description="Number of buildings"
        ),
        city_distance: float = Annotated(
            ...,
            ge=0,
            le=20,
            description="Distance from city center in miles"
        ),
        neighborhood: str = Annotated(
            ...,
            description="Seattle neighborhood"
        ),
        year_built: int = Annotated(
            ...,
            ge=1900,
            le=2025,
            description="Year the building was constructed"
        )
    ) -> Dict[str, Any]:
        """Predict building energy consumption.
        
        Args:
            first_use_type: First largest property use type
            second_largest_property_use_type: Second largest property use type (optional)
            multiple_use_type: Number of different property use types
            sum_largest_gfa: Three largest property use type GFA in square feet
            use_steam: Building uses steam
            use_gas: Building uses natural gas
            number_of_floors: Number of floors
            number_of_buildings: Number of buildings
            city_distance: Distance from city center in miles
            neighborhood: Seattle neighborhood
            year_built: Year the building was constructed
            
        Returns:
            JSON response with prediction or error
        """
        try:
            # Convert Enum values to their string values
            # Enum members automatically convert to their values when used as strings
            building_input = BuildingInput(
                first_use_type=first_use_type.value,
                second_largest_property_use_type=second_largest_property_use_type.value if second_largest_property_use_type else None,
                multiple_use_type=multiple_use_type,
                sum_largest_gfa=sum_largest_gfa,
                use_steam=use_steam,
                use_gas=use_gas,
                number_of_floors=number_of_floors,
                number_of_buildings=number_of_buildings,
                city_distance=city_distance,
                neighborhood=neighborhood,
                year_built=year_built
            )
            
            logger.info(f"Received input: {building_input}")
            
            # Transform input data
            df_input = data_transformer.transform_input(building_input)
            
            # Make prediction
            prediction = model_loader.predict(df_input)
            
            # Prepare response
            response = PredictionResponse(
                prediction=round(float(prediction[0]), 0),
                input_data=building_input,
                status="success"
            )
            
            logger.info(f"Prediction successful: {prediction[0]}")
            return response.model_dump()
            
        except (ValueError, TypeError) as e:
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
    
    @bentoml.api(route="/health")
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
    
    @bentoml.api(route="/available-values")
    def get_available_values(self) -> Dict[str, Any]:
        """Get available values for categorical fields.
        
        Returns:
            JSON response with all available values for dropdowns
        """
        return {
            "first_use_type": [e.value for e in FirstUseTypeEnum],
            "second_largest_property_use_type": [e.value for e in SecondLargestPropertyUseTypeEnum],
            "neighborhoods": config.NEIGHBORHOODS
        }
