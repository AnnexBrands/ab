"""Custom exceptions for the ABConnect SDK."""


class ABConnectError(Exception):
    """Base exception for all ABConnect SDK errors."""


class AuthenticationError(ABConnectError):
    """Raised when authentication fails (invalid credentials, expired tokens)."""


class RequestError(ABConnectError):
    """Raised when an API request fails with an error response.

    Attributes:
        status_code: HTTP status code from the response.
        message: Error message from the API or a description of the failure.
    """

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class ConfigurationError(ABConnectError):
    """Raised when required configuration is missing or invalid."""


class ValidationError(ABConnectError):
    """Raised when data validation fails outside of Pydantic model validation."""
