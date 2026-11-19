
from client import Client
from services import Service
from reservation import Reservation
from exceptions import (
    DuplicateClientError,
    ClientNotFoundError,
    ServiceNotFoundError,
    ReservationNotFoundError,
    InvalidReservationError,
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

            client = Client(name, normalized_email, phone)
            self.__clients.append(client)

        except DuplicateClientError as error:
            logger.error("Client registration failed: %s", error)
            raise

        except (TypeError, ValueError) as error:
            logger.error("Invalid client information: %s", error)
            raise

        else:
            logger.info(
                "Client registered successfully: %s",
                client.get_email()
            )
            return client

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
        try:
            if not isinstance(service, Service):
                raise TypeError("The object must be a valid service.")

            service.validate_parameters()
            self.__services.append(service)

        except (TypeError, ValueError) as error:
            logger.error("Service registration failed: %s", error)
            raise

        else:
            logger.info(
                "Service added successfully: %s",
                service.get_name()
            )
            return service

    def find_service(self, service_id):
        try:
            if not isinstance(service_id, str) or not service_id.strip():
                raise ValueError("A valid service ID is required.")

            for service in self.__services:
                if service.get_id() == service_id:
                    return service

            raise ServiceNotFoundError(
                f"Service not found: {service_id}"
            )

        except (ValueError, ServiceNotFoundError) as error:
            logger.error("Service lookup failed: %s", error)
            raise

    # RESERVATION MANAGEMENT

    def create_reservation(
        self,
        client_email,
        service_id,
        hours,
        discount=0
    ):
        client = self.find_client(client_email)
        service = self.find_service(service_id)

        try:
            reservation = Reservation(
                client,
                service,
                hours,
                discount
            )

            self.__reservations.append(reservation)

        except InvalidReservationError as error:
            logger.error(
                "Reservation creation failed: %s",
                error
            )
            raise

        else:
            logger.info(
                "Reservation created successfully: %s",
                reservation.get_id()
            )
            return reservation

    def find_reservation(self, reservation_id):
        try:
            if (
                not isinstance(reservation_id, str)
                or not reservation_id.strip()
            ):
                raise ValueError("A valid reservation ID is required.")

            for reservation in self.__reservations:
                if reservation.get_id() == reservation_id:
                    return reservation

            raise ReservationNotFoundError(
                f"Reservation not found: {reservation_id}"
            )

        except (ValueError, ReservationNotFoundError) as error:
            logger.error("Reservation lookup failed: %s", error)
            raise

    def confirm_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)

        try:
            result = reservation.confirm()

        except InvalidReservationError as error:
            logger.error(
                "Reservation confirmation failed: %s",
                error
            )
            raise

        else:
            logger.info(
                "Reservation confirmed: %s",
                reservation_id
            )
            return result

    def cancel_reservation(self, reservation_id):
        reservation = self.find_reservation(reservation_id)

        try:
            result = reservation.cancel()

        except InvalidReservationError as error:
            logger.error(
                "Reservation cancellation failed: %s",
                error
            )
            raise

        else:
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
