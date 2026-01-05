from enum import Enum


class OrderStatus(Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"