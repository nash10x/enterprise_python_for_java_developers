from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    amount: Decimal


class OrderValidationError(ValueError):
    pass


class OrderNotFoundError(LookupError):
    pass
