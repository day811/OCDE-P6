#ocde_p6/validations/schemas.py

"""Pydantic schemas for input validation."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from ..utils.enums import FirstUseTypeEnum

class BuildingInput(BaseModel):
    """Input schema for building energy prediction."""
    
    first_use_type: Optional[FirstUseTypeEnum] = Field(
        ...,
        description="First largest property use type",
        example="Hospital"
    )
    
    second_use_type: Optional[str] = Field(
        default=None,
        description="Second largest property use type",
        example="Parking"
    )
    
    multiple_use_type: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Number of different property use types",
        example=1
    )
    
    sum_largest_gfa : float = Field(
        ...,
        ge=0,
        description="Three largest property use type GFA in square feet",
        example=88434.0
    )
    
    use_steam: bool = Field(
        default=False,
        description="Building uses steam",
        example=True
    )
    
    use_gas: bool = Field(
        default=False,
        description="Building uses natural gas",
        example=False
    )
    
    number_of_floors: float = Field(
        ...,
        ge=1,
        le=100,
        description="Number of floors",
        example=12.0
    )
    
    number_of_buildings: float = Field(
        default=1.0,
        ge=1,
        description="Number of buildings",
        example=1.0
    )
    
    city_distance: float = Field(
        ...,
        ge=0,
        le=20,
        description="Distance from city center in miles",
        example=8.5
    )
    
    neighborhood: str = Field(
        ...,
        description="Seattle neighborhood",
        example="DOWNTOWN"
    )
    
    year_built: int = Field(
        ...,
        ge=1900,
        le=2025,
        description="Year the building was constructed",
        example=1927
    )
    
    """Pydantic configuration."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "first_use_type": "Hospital",
                "second_use_type": None,
                "multiple_use_type": 1,
                "sum_largest_gfa": 88434.0,
                "use_steam": True,
                "use_gas": False,
                "number_of_floors": 12.0,
                "number_of_buildings": 1.0,
                "city_distance": 8.5,
                "neighborhood": "DOWNTOWN",
                "year_built": 1999
            }
        }
    }
        
class PredictionResponse(BaseModel):
    """Response schema for prediction results."""
    
    prediction: float = Field(
        ...,
        description="Predicted energy consumption in kBtu/sf",
        example=81.71
    )
    
    input_data: BuildingInput = Field(
        ...,
        description="Echo of input data used for prediction"
    )
    
    status: str = Field(
        default="success",
        description="Status of the prediction"
    )

class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(
        ...,
        description="Error message"
    )
    
    status: str = Field(
        default="error",
        description="Status indicating error"
    )
