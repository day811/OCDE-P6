#ocde_p6/utils/config.py

"""Configuration management for the API."""

import os
from typing import Optional


class Config:
    """Application configuration."""
    
    # Model configuration
    MODEL_NAME: str = "building_energy_rf_pipeline"
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "3000"))
    
    # Feature configuration
    REQUIRED_FEATURES = ['YearBuilt', 'FirstUseType']
    
    # Validation ranges
    MIN_YEAR_BUILT = 1900
    MAX_YEAR_BUILT = 2025
    
    # First use type values for API parameters
    FIRST_USE_TYPE_VALUES = [
        "Data Center",
        "Distribution Center",
        "Hospital",
        "K-12 School",
        "Laboratory",
        "Large Office",
        "Manufacturing/Industrial Plant",
        "Other",
        "Parking",
        "Restaurant",
        "Self-Storage Facility",
        "Supermarket / Grocery Store",
        "University",
        "Warehouse",
        "Worship Facility",
        "Value not listed"
    ]
    
    # Second largest use type values for API parameters
    SECOND_LARGEST_USE_TYPE_VALUES = [
        "Data Center",
        "Laboratory",
        "Office",
        "Parking",
        "Restaurant",
        "Value not listed",
        "None"
    ]
    
    # Neighborhood values
    NEIGHBORHOODS = [
        "GREATER DUWAMISH",
        "Value not listed",
    ]


config = Config()
