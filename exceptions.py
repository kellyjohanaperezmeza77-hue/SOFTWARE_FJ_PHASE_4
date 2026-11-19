
class SoftwareFJException(Exception):
    """Base exception for the Software FJ system."""
    pass


class ClientNotFoundError(SoftwareFJException):
    """Raised when a client cannot be found."""
    pass


class ServiceNotFoundError(SoftwareFJException):
    """Raised when a service cannot be found."""
    pass


class ReservationNotFoundError(SoftwareFJException):
    """Raised when a reservation cannot be found."""
    pass


class DuplicateClientError(SoftwareFJException):
    """Raised when a client already exists."""
    pass


class InvalidReservationError(SoftwareFJException):
    """Raised when a reservation contains invalid information."""
    pass
