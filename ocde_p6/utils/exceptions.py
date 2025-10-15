#ocde_p6/utils/exceptions

"""Custom exceptions for the API."""

class APIError(Exception):
    """Base exception for API errors."""
    pass

class ModelLoadError(APIError):
    """Exception raised when model loading fails."""
    pass

class ValidationError(APIError):
    """Exception raised when input validation fails."""
    pass

class PredictionError(APIError):
    """Exception raised when prediction fails."""
    pass

class TransformationError(APIError):
    """Exception raised when data transformation fails."""
    pass
