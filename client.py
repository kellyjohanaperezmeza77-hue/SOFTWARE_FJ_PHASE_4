
from entities import Entity


class Client(Entity):
    """Represents a client in the Software FJ system."""

    def __init__(self, name, email, phone):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Client name cannot be empty.")

        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email address.")

        if not isinstance(phone, str) or not phone.isdigit():
            raise ValueError("Phone number must contain only digits.")

        self.__name = name.strip()
        self.__email = email.strip().lower()
        self.__phone = phone

    def get_details(self):
        return (
            f"Client ID: {self.id} | "
            f"Name: {self.__name} | "
            f"Email: {self.__email} | "
            f"Phone: {self.__phone}"
        )

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def update_phone(self, new_phone):
        if not isinstance(new_phone, str) or not new_phone.isdigit():
            raise ValueError("Invalid phone number.")

        self.__phone = new_phone
