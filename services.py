
import math
from abc import abstractmethod

from entities import Entity


class Service(Entity):
    """Abstract base class for all services."""

    def __init__(self, name, base_price):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Service name cannot be empty.")

        if (
            not isinstance(base_price, (int, float))
            or isinstance(base_price, bool)
            or not math.isfinite(base_price)
            or base_price <= 0
        ):
            raise ValueError("Base price must be a positive number.")

        self.__name = name.strip()
        self.__base_price = float(base_price)
        self.__available = True

    def get_name(self):
        return self.__name

    def get_base_price(self):
        return self.__base_price

    def is_available(self):
        return self.__available

    def set_availability(self, available):
        if not isinstance(available, bool):
            raise ValueError("Availability must be True or False.")

        self.__available = available

    def calculate_final_cost(self, hours, discount=0):
        self._validate_hours(hours)
        self._validate_discount(discount)

        total = self.calculate_cost(hours)
        final_cost = total - (total * discount / 100)

        return final_cost

    def _validate_hours(self, hours):
        if (
            not isinstance(hours, (int, float))
            or isinstance(hours, bool)
            or not math.isfinite(hours)
            or hours <= 0
        ):
            raise ValueError("Hours must be a positive number.")

    def _validate_discount(self, discount):
        if (
            not isinstance(discount, (int, float))
            or isinstance(discount, bool)
            or not math.isfinite(discount)
            or discount < 0
            or discount > 100
        ):
            raise ValueError("Discount must be between 0 and 100.")

    @abstractmethod
    def calculate_cost(self, hours):
        pass

    @abstractmethod
    def validate_parameters(self):
        pass

    @abstractmethod
    def get_details(self):
        pass


class RoomReservationService(Service):
    """Service for renting rooms."""

    def __init__(self, name, base_price, capacity):
        super().__init__(name, base_price)

        if (
            not isinstance(capacity, int)
            or isinstance(capacity, bool)
            or capacity <= 0
        ):
            raise ValueError("Room capacity must be a positive integer.")

        self.__capacity = capacity

    def get_capacity(self):
        return self.__capacity

    def calculate_cost(self, hours):
        self._validate_hours(hours)
        return self.get_base_price() * hours

    def validate_parameters(self):
        if self.__capacity <= 0:
            raise ValueError("Room capacity must be positive.")

        return True

    def get_details(self):
        return (
            f"Room Service: {self.get_name()} | "
            f"Capacity: {self.__capacity} people | "
            f"Hourly Rate: {self.get_base_price():.2f}"
        )


class EquipmentRentalService(Service):
    """Service for renting equipment."""

    def __init__(self, name, base_price, quantity):
        super().__init__(name, base_price)

        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity <= 0
        ):
            raise ValueError(
                "Equipment quantity must be a positive integer."
            )

        self.__quantity = quantity

    def get_quantity(self):
        return self.__quantity

    def calculate_cost(self, hours):
        self._validate_hours(hours)
        return self.get_base_price() * hours

    def validate_parameters(self):
        if self.__quantity <= 0:
            raise ValueError("Equipment quantity must be positive.")

        return True

    def get_details(self):
        return (
            f"Equipment Rental: {self.get_name()} | "
            f"Available Quantity: {self.__quantity} | "
            f"Hourly Rate: {self.get_base_price():.2f}"
        )


class SpecializedConsultingService(Service):
    """Service for specialized professional consulting."""

    def __init__(self, name, base_price, specialty):
        super().__init__(name, base_price)

        if not isinstance(specialty, str) or not specialty.strip():
            raise ValueError("Consulting specialty cannot be empty.")

        self.__specialty = specialty.strip()

    def get_specialty(self):
        return self.__specialty

    def calculate_cost(self, hours):
        self._validate_hours(hours)
        return self.get_base_price() * hours

    def validate_parameters(self):
        if not self.__specialty:
            raise ValueError("Consulting specialty cannot be empty.")

        return True

    def get_details(self):
        return (
            f"Consulting Service: {self.get_name()} | "
            f"Specialty: {self.__specialty} | "
            f"Hourly Rate: {self.get_base_price():.2f}"
        )
