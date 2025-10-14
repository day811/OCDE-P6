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
    ALLOWED_USE_TYPES = ['Hotel', 'DataCenter', 'Restaurant']
    
    # Validation ranges
    MIN_YEAR_BUILT = 1900
    MAX_YEAR_BUILT = 2025

config = Config()
