
from manager import SoftwareFJManager
from services import (
    RoomReservationService,
    EquipmentRentalService,
    SpecializedConsultingService,
)
from exceptions import (
    DuplicateClientError,
    ClientNotFoundError,
    ServiceNotFoundError,
    InvalidReservationError,
    ReservationNotFoundError,
)
from logging_config import logger


def display_menu():
    print("\n======================================")
    print("       SOFTWARE FJ MANAGEMENT")
    print("======================================")
    print("1. Register client")
    print("2. Register service")
    print("3. Create reservation")
    print("4. Confirm reservation")
    print("5. Cancel reservation")
    print("6. List clients")
    print("7. List services")
    print("8. List reservations")
    print("9. Run system demonstration")
    print("0. Exit")
    print("======================================")


def register_client(manager):
    print("\n--- CLIENT REGISTRATION ---")

    name = input("Client name: ")
    email = input("Client email: ")
    phone = input("Client phone: ")

    try:
        client = manager.register_client(name, email, phone)

    except (DuplicateClientError, ValueError, TypeError) as error:
        print(f"Registration error: {error}")

    else:
        print("Client registered successfully.")
        print(client.get_details())

    finally:
        print("Client registration process completed.")


def register_service(manager):
    print("\n--- SERVICE REGISTRATION ---")
    print("1. Room reservation")
    print("2. Equipment rental")
    print("3. Specialized consulting")

    option = input("Select service type: ")

    try:
        name = input("Service name: ")
        price = float(input("Hourly price: "))

        if option == "1":
            capacity = int(input("Room capacity: "))
            service = RoomReservationService(
                name, price, capacity
            )

        elif option == "2":
            quantity = int(input("Equipment quantity: "))
            service = EquipmentRentalService(
                name, price, quantity
            )

        elif option == "3":
            specialty = input("Consulting specialty: ")
            service = SpecializedConsultingService(
                name, price, specialty
            )

        else:
            raise ValueError("Invalid service type.")

        manager.add_service(service)

    except (ValueError, TypeError) as error:
        logger.error("Service registration failed: %s", error)
        print(f"Service error: {error}")

    else:
        print("Service registered successfully.")
        print(service.get_details())
        print(f"Service ID: {service.get_id()}")


def create_reservation(manager):
    print("\n--- CREATE RESERVATION ---")

    email = input("Client email: ")
    service_id = input("Service ID: ")

    try:
        hours = float(input("Number of hours: "))
        discount = float(input("Discount percentage (0-100): "))

        reservation = manager.create_reservation(
            email,
            service_id,
            hours,
            discount
        )

    except (
        ClientNotFoundError,
        ServiceNotFoundError,
        InvalidReservationError,
        ValueError,
        TypeError,
    ) as error:
        print(f"Reservation error: {error}")

    else:
        print("Reservation created successfully.")
        print(reservation.get_details())

    finally:
        print("Reservation creation process completed.")


def confirm_reservation(manager):
    print("\n--- CONFIRM RESERVATION ---")
    reservation_id = input("Reservation ID: ")

    try:
        result = manager.confirm_reservation(reservation_id)

    except (ReservationNotFoundError, InvalidReservationError) as error:
        print(f"Confirmation error: {error}")

    else:
        print(result)


def cancel_reservation(manager):
    print("\n--- CANCEL RESERVATION ---")
    reservation_id = input("Reservation ID: ")

    try:
        result = manager.cancel_reservation(reservation_id)

    except (ReservationNotFoundError, InvalidReservationError) as error:
        print(f"Cancellation error: {error}")

    else:
        print(result)


def list_clients(manager):
    print("\n--- REGISTERED CLIENTS ---")

    clients = manager.list_clients()

    if not clients:
        print("No clients registered.")
        return

    for client in clients:
        print(client.get_details())


def list_services(manager):
    print("\n--- REGISTERED SERVICES ---")

    services = manager.list_services()

    if not services:
        print("No services registered.")
        return

    for service in services:
        print(service.get_details())
        print(f"Service ID: {service.get_id()}")


def list_reservations(manager):
    print("\n--- REGISTERED RESERVATIONS ---")

    reservations = manager.list_reservations()

    if not reservations:
        print("No reservations registered.")
        return

    for reservation in reservations:
        print(reservation.get_details())


def run_demonstration(manager):
    print("\n======================================")
    print("       SYSTEM DEMONSTRATION")
    print("======================================")

    # Operation 1: Register a valid client.
    print("\n1. Registering a valid client...")

    try:
        client = manager.register_client(
            "Laura Martinez",
            "laura@example.com",
            "3001234567"
        )

    except DuplicateClientError:
        client = manager.find_client("laura@example.com")
        print("Client already exists. Using the registered client.")

    except (ValueError, TypeError) as error:
        print("Client registration failed:", error)
        return

    else:
        print("SUCCESS:", client.get_details())

    # Operation 2: Attempt to register a duplicate client.
    print("\n2. Testing duplicate client registration...")

    try:
        manager.register_client(
            "Laura Martinez",
            "laura@example.com",
            "3001234567"
        )

    except DuplicateClientError as error:
        print("EXPECTED ERROR:", error)

    # Operation 3: Attempt to register an invalid client.
    print("\n3. Testing invalid client information...")

    try:
        manager.register_client(
            "",
            "invalid-email",
            "abc123"
        )

    except (ValueError, TypeError) as error:
        print("EXPECTED ERROR:", error)

    # Operation 4: Register a room service.
    print("\n4. Registering a room reservation service...")

    room = RoomReservationService(
        "Conference Room A", 50000, 20
    )
    manager.add_service(room)
    print("SUCCESS:", room.get_details())

    # Operation 5: Register an equipment service.
    print("\n5. Registering an equipment rental service...")

    equipment = EquipmentRentalService(
        "Video Projector", 30000, 5
    )
    manager.add_service(equipment)
    print("SUCCESS:", equipment.get_details())

    # Operation 6: Register a consulting service.
    print("\n6. Registering a consulting service...")

    consulting = SpecializedConsultingService(
        "Technology Consulting",
        80000,
        "Software Development"
    )
    manager.add_service(consulting)
    print("SUCCESS:", consulting.get_details())

    # Operation 7: Attempt to register an invalid service.
    print("\n7. Testing invalid service information...")

    try:
        RoomReservationService(
            "Invalid Room", -5000, 0
        )

    except ValueError as error:
        print("EXPECTED ERROR:", error)

    # Operation 8: Attempt a reservation with invalid hours.
    print("\n8. Testing reservation with invalid hours...")

    try:
        manager.create_reservation(
            "laura@example.com",
            room.get_id(),
            -2,
            0
        )

    except InvalidReservationError as error:
        print("EXPECTED ERROR:", error)

    # Operation 9: Attempt a reservation with an unknown client.
    print("\n9. Testing reservation with an unknown client...")

    try:
        manager.create_reservation(
            "unknown@example.com",
            room.get_id(),
            2,
            0
        )

    except ClientNotFoundError as error:
        print("EXPECTED ERROR:", error)

    # Operation 10: Attempt a reservation with an unknown service.
    print("\n10. Testing reservation with an unknown service...")

    try:
        manager.create_reservation(
            "laura@example.com",
            "invalid-service-id",
            2,
            0
        )

    except ServiceNotFoundError as error:
        print("EXPECTED ERROR:", error)

    # Operation 11: Create a valid reservation.
    print("\n11. Creating a valid reservation...")

    reservation = manager.create_reservation(
        "laura@example.com",
        room.get_id(),
        3,
        10
    )
    print("SUCCESS:", reservation.get_details())

    # Operation 12: Confirm the reservation.
    print("\n12. Confirming the reservation...")

    print(manager.confirm_reservation(reservation.get_id()))

    # Operation 13: Cancel the reservation.
    print("\n13. Cancelling the reservation...")

    print(manager.cancel_reservation(reservation.get_id()))

    # Operation 14: Attempt to find a nonexistent reservation.
    print("\n14. Testing a nonexistent reservation...")

    try:
        manager.find_reservation("invalid-reservation-id")

    except ReservationNotFoundError as error:
        print("EXPECTED ERROR:", error)

    print("\n======================================")
    print("       DEMONSTRATION COMPLETED")
    print("======================================")

    logger.info("System demonstration completed.")


def main():
    manager = SoftwareFJManager()

    print("\nWelcome to Software FJ Management System!")

    while True:
        try:
            display_menu()
            option = input("Select an option: ")

            if option == "1":
                register_client(manager)

            elif option == "2":
                register_service(manager)

            elif option == "3":
                create_reservation(manager)

            elif option == "4":
                confirm_reservation(manager)

            elif option == "5":
                cancel_reservation(manager)

            elif option == "6":
                list_clients(manager)

            elif option == "7":
                list_services(manager)

            elif option == "8":
                list_reservations(manager)

            elif option == "9":
                run_demonstration(manager)

            elif option == "0":
                print("Thank you for using Software FJ.")
                logger.info("Application closed.")
                break

            else:
                print("Invalid option. Please try again.")

        except (KeyboardInterrupt, EOFError):
            print("\nApplication interrupted by the user.")
            logger.warning("Application interrupted by the user.")
            break

        except Exception as error:
            logger.exception(
                "Unexpected application error: %s",
                error
            )
            print(f"An unexpected error occurred: {error}")
            print("The application will continue running.")


if __name__ == "__main__":
    main()
