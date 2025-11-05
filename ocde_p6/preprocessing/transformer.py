#ocde_p6/preprocessing/transformer.py
"""Data transformation utilities for API inputs."""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

from ..utils.logger import get_logger
from ..validation.schemas import BuildingInput

logger = get_logger(__name__)

def fix_floors_and_discretize(df_in):
    """
    Fonction de preprocessing personnalisée appliquée dans le pipeline.
    """
    # Copie pour ne pas modifier l'original
    df = df_in.copy()
    df.replace('', pd.NA, inplace=True)
    

    # Fix floors
    if 'NumberofFloors' in df.columns:
        df['NumberofFloors'] = df['NumberofFloors'].fillna(1)
        df['NumberofFloors'] = df['NumberofFloors'].clip(lower=1)
    
    # Créer PropertySize 
    if 'SumLargestGFA' in df.columns:
        
        # Discretize size
        bins = [0, 20000, 100000, 500000, float('inf')]
        labels = ['Small', 'Mid', 'Large', 'XLarge']
        df['PropertySize'] = pd.cut(df['SumLargestGFA'], bins=bins, labels=labels)
        df['log_GFA'] = np.log1p(df['SumLargestGFA'])
        df['GFA_per_floor'] = df['SumLargestGFA'] / df['NumberofFloors']
        df['building_volume'] = df['SumLargestGFA'] * df['NumberofFloors']


    # Créer AgeProperty et AgeCategory
    if 'YearBuilt' in df.columns:
        current_year = 2016  # Année des données
        df['AgeProperty'] = current_year - df['YearBuilt']
        
        # Discretize age
        age_bins = [0, 10, 30, float('inf')]
        age_labels = ['New', 'Recent', 'Old']
        df['AgeCategory'] = pd.cut(df['AgeProperty'], bins=age_bins, labels=age_labels)
    
    # Créer EnergyEra
    if 'YearBuilt' in df.columns:
        df['EnergyEra'] = df['YearBuilt'].apply(
            lambda x: 'Pre-Crisis' if x < 1973 else 'Modern'
        )
    
    # Créer HeightCategory
    if 'NumberofFloors' in df.columns:
        height_bins = [0, 4, 12, float('inf')]
        height_labels = ['Low', 'Mid', 'High']
        df['HeightCategory'] = pd.cut(df['NumberofFloors'], bins=height_bins, labels=height_labels)
    
    # Remplir NaN dans SecondLargestPropertyUseType
    if 'SecondLargestPropertyUseType' in df.columns:
        # Conversion "" → NaN pour toutes les colonnes (ou celle spécifique)
        df['SecondLargestPropertyUseType'] = df['SecondLargestPropertyUseType'].fillna('None')
    
    columns_to_drop = ['YearBuilt','NumberofFloors','log_GFA','PropertySize' ,]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])    
    return df


class DataTransformer:
    """Handles transformation of user input to model-ready format."""
    
    def __init__(self):
        # Features attendues en entrée par le pipeline
        self.input_features = [
            'FirstUseType',
            'SecondLargestPropertyUseType',
            'MultipleUseType',
            'SumLargestGFA',
            'UseSteam',
            'UseGas',
            'NumberofFloors',
            'NumberofBuildings',
            'CityDistance',
            'Neighborhood',
            'YearBuilt'
        ]
        
        # Features après encodage (à récupérer du modèle si nécessaire)
        self.categorical_features = [
            'FirstUseType',
            'SecondLargestPropertyUseType',
            'PropertySize',
            'Neighborhood',
            'AgeCategory',
            'EnergyEra',
            'HeightCategory'
        ]
        
        self.numerical_features = [
            'AgeProperty',
            'CityDistance',
            'MultipleUseType',
            'NumberofBuildings'
        ]
    
    def transform_input(self, building_input: BuildingInput) -> pd.DataFrame:
        """Transform validated user input to model format.
        
        Args:
            building_input: Validated Pydantic model
            
        Returns:
            pandas DataFrame ready for model prediction
        """
        try:
            # Créer DataFrame avec les features attendues par le pipeline
            data = {
                'FirstUseType': building_input.first_use_type.value,
                'SecondLargestPropertyUseType': building_input.second_use_type.value,
                'MultipleUseType': building_input.multiple_use_type,
                'SumLargestGFA': building_input.sum_largest_gfa,
                'UseSteam': building_input.use_steam,
                'UseGas': building_input.use_gas,
                'NumberofFloors': building_input.number_of_floors,
                'NumberofBuildings': building_input.number_of_buildings,
                'CityDistance': building_input.city_distance,
                'Neighborhood': building_input.neighborhood,
                'YearBuilt': building_input.year_built
            }
            
            df = pd.DataFrame([data])
            
            logger.info(f"Transformed input: {data}")
            return df
            
        except Exception as e:
            logger.error(f"Error transforming input: {str(e)}")
            raise ValueError(f"Failed to transform input data: {str(e)}")

# Global instance
data_transformer = DataTransformer()
