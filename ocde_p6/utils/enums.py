#ocde_p6/utils/enums.py

"""Enum definitions for categorical fields."""

from enum import Enum


class FirstUseTypeEnum(str, Enum):
    """First largest property use type enum."""
    
    data_center = "Data Center"
    distribution_center = "Distribution Center"
    hospital = "Hospital"
    k_12_school = "K-12 School"
    laboratory = "Laboratory"
    large_office = "Large Office"
    manufacturing_industrial_plant = "Manufacturing/Industrial Plant"
    other = "Other"
    parking = "Parking"
    restaurant = "Restaurant"
    self_storage_facility = "Self-Storage Facility"
    supermarket_grocery_store = "Supermarket / Grocery Store"
    university = "University"
    warehouse = "Warehouse"
    worship_facility = "Worship Facility"
    value_not_listed = "Value not listed"


class SecondUseTypeEnum(str, Enum):
    """Second largest property use type enum."""
    
    data_center = "Data Center"
    laboratory = "Laboratory"
    office = "Office"
    parking = "Parking"
    restaurant = "Restaurant"
    value_not_listed = "Value not listed"
    none = "None"
