#ocde_p6/validations/schemas.py

"""Pydantic schemas for input validation."""

from pydantic import BaseModel, Field, field_validator
from typing import Literal
from enum import Enum

class BuildingTypeEnum(str, Enum):
    """Allowed building types."""
    HOTEL = "Hotel"
    DATA_CENTER = "DataCenter"
    RESTAURANT = "Restaurant"

class BuildingInput(BaseModel):
    """Input schema for building energy prediction.
    
    Validates user input for the building energy prediction API.
    """
    
    year_built: int = Field(
        ...,
        ge=1900,
        le=2025,
        description="Year the building was constructed",
        example=2010
    )
    
    first_use_type: BuildingTypeEnum = Field(
        ...,
        description="Primary use type of the building",
        example="Hotel"
    )
    
    @field_validator('year_built')
    @classmethod
    def validate_year_built(cls, v: int) -> int:
        """Validate year built is reasonable."""
        current_year = 2025
        if v > current_year:
            raise ValueError(f'Year built cannot be in the future (max: {current_year})')
        if v < 1900:
            raise ValueError('Year built seems unrealistic (min: 1900)')
        return v
    
    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "year_built": 2010,
                "first_use_type": "Hotel"
            }
        }
    }

class PredictionResponse(BaseModel):
    """Response schema for prediction results."""
    
    prediction: float = Field(
        ...,
        description="Predicted energy consumption in kBtu",
        example=125000.5
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
