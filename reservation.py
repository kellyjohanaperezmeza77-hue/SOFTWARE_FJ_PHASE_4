
import math

from entities import Entity
from client import Client
from services import Service
from exceptions import InvalidReservationError


class Reservation(Entity):
    """Represents a reservation made by a client."""

    VALID_STATUSES = ("Pending", "Confirmed", "Cancelled")

    def __init__(self, client, service, hours, discount=0):
        super().__init__()

        if not isinstance(client, Client):
            raise InvalidReservationError(
                "A reservation must have a valid client."
            )

        if not isinstance(service, Service):
            raise InvalidReservationError(
                "A reservation must have a valid service."
            )

        if not service.is_available():
            raise InvalidReservationError(
                "The selected service is not available."
            )

        try:
            self.__validate_hours(hours)
            self.__validate_discount(discount)

            service.validate_parameters()
            total_cost = service.calculate_final_cost(hours, discount)

        except (TypeError, ValueError, OverflowError) as error:
            raise InvalidReservationError(
                "The reservation contains invalid information."
            ) from error

        self.__client = client
        self.__service = service
        self.__hours = hours
        self.__discount = discount
        self.__total_cost = total_cost
        self.__status = "Pending"

    def __validate_hours(self, hours):
        if (
            not isinstance(hours, (int, float))
            or isinstance(hours, bool)
            or not math.isfinite(hours)
            or hours <= 0
        ):
            raise ValueError("Reservation hours must be positive.")

    def __validate_discount(self, discount):
        if (
            not isinstance(discount, (int, float))
            or isinstance(discount, bool)
            or not math.isfinite(discount)
            or discount < 0
            or discount > 100
        ):
            raise ValueError("Discount must be between 0 and 100.")

    def confirm(self):
        if self.__status != "Pending":
            raise InvalidReservationError(
                "Only pending reservations can be confirmed."
            )

        self.__status = "Confirmed"
        return "Reservation confirmed successfully."

    def cancel(self):
        if self.__status == "Cancelled":
            raise InvalidReservationError(
                "This reservation is already cancelled."
            )

        self.__status = "Cancelled"
        return "Reservation cancelled successfully."

    def get_client(self):
        return self.__client

    def get_service(self):
        return self.__service

    def get_hours(self):
        return self.__hours

    def get_discount(self):
        return self.__discount

    def get_total_cost(self):
        return self.__total_cost

    def get_status(self):
        return self.__status

    def get_details(self):
        return (
            f"Reservation ID: {self.id} | "
            f"Client: {self.__client.get_name()} | "
            f"Service: {self.__service.get_name()} | "
            f"Hours: {self.__hours} | "
            f"Discount: {self.__discount}% | "
            f"Total: {self.__total_cost:.2f} | "
            f"Status: {self.__status}"
        )
