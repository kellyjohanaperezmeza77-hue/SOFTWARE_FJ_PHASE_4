
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class Entity(ABC):
    """Abstract base class for system entities."""

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()

    def get_id(self):
        return self.id

    def get_creation_date(self):
        return self.created_at

    @abstractmethod
    def get_details(self):
        """Return the details of the entity."""
        pass
