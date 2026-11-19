
from client import Client
from services import Service
from reservation import Reservation
from exceptions import (
    DuplicateClientError,
    ClientNotFoundError,
    ServiceNotFoundError,
    ReservationNotFoundError,
)
from logging_config import logger


class SoftwareFJManager:
    """Manages clients, services, and reservations."""

    def __init__(self):
        self.__clients = []
        self.__services = []
        self.__reservations = []

    # CLIENT MANAGEMENT

    def register_client(self, name, email, phone):
        try:
            if not isinstance(email, str) or not email.strip():
                raise ValueError("A valid email address is required.")

            normalized_email = email.strip().lower()

            for client in self.__clients:
                if client.get_email() == normalized_email:
                    raise DuplicateClientError(
                        "A client with this email already exists."
                    )

            client = Client(name, email, phone)
            self.__clients.append(client)

            logger.info(
                "Client registered successfully: %s",
                client.get_email()
            )

            return client

        except DuplicateClientError as error:
            logger.error("Client registration failed: %s", error)
            raise

        except (TypeError, ValueError) as error:
            logger.error("Invalid client information: %s", error)
            raise

    def find_client(self, email):
        try:
            if not isinstance(email, str) or not email.strip():
                raise ValueError("A valid client email is required.")

            normalized_email = email.strip().lower()

            for client in self.__clients:
                if client.get_email() == normalized_email:
                    return client

            raise ClientNotFoundError(
                f"Client not found: {normalized_email}"
            )

        except (ValueError, ClientNotFoundError) as error:
            logger.error("Client lookup failed: %s", error)
            raise

    # SERVICE MANAGEMENT

    def add_service(self, service):
        if not isinstance(service, Service):
            raise TypeError("The object must be a valid service.")

        service.validate_parameters()
        self.__services.append(service)

        logger.info(
            "Service added successfully: %s",
            service.get_name()
        )

        return service

    def find_service(self, service_id):
        for service in self.__services:
            if service.get_id() == service_id:
                return service

        raise ServiceNotFoundError(
            f"Service not found: {service_id}"
        )

    # RESERVATION MANAGEMENT

    def create_reservation(
        self,
        client_email,
        service_id,
        hours,
        discount=0
    ):
        try:
            client = self.find_client(client_email)
            service = self.find_service(service_id)

            reservation = Reservation(
                client,
                service,
                hours,
                discount
            )

            self.__reservations.append(reservation)

            logger.info(
                "Reservation created successfully: %s",
                reservation.get_id()
            )

            return reservation

        except Exception as error:
            logger.error(
                "Reservation creation failed: %s",
                error
            )
            raise

    def find_reservation(self, reservation_id):
        for reservation in self.__reservations:
            if reservation.get_id() == reservation_id:
                return reservation

        raise ReservationNotFoundError(
            f"Reservation not found: {reservation_id}"
        )

    def confirm_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)
        result = reservation.confirm()

        logger.info(
            "Reservation confirmed: %s",
            reservation_id
        )

        return result

    def cancel_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)
        result = reservation.cancel()

        logger.info(
            "Reservation cancelled: %s",
            reservation_id
        )

        return result

    # INFORMATION AND REPORTS

    def list_clients(self):
        return list(self.__clients)

    def list_services(self):
        return list(self.__services)

    def list_reservations(self):
        return list(self.__reservations)
