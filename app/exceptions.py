class CommonError(Exception):
    """
    Base error class for application-level exceptions that should be interpreted
    as internal server error (HTTP 500) in API responses.
    """


class ClientError(Exception):
    """
    Base error class for application-level exceptions that should be interpreted
    as bad request (HTTP 400) in API responses.
    """


class FileUploadError(ClientError):
    """Exception raised when a file upload fails due to client-side issues."""


class NotFoundFileError(ClientError):
    """Exception raised when a file record with the given ID is not found in the database."""


class InvalidFileExtensionError(ClientError):
    """Exception raised when an uploaded file has an unsupported or disallowed extension."""


class ConversionFailedError(CommonError):
    """Exception raised when a file conversion process fails."""


class RowNotFoundError(CommonError):
    """Exception raised when a database row is not found."""
