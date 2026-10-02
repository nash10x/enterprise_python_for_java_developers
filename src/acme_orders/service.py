from decimal import Decimal
from uuid import uuid4

from .domain import Order, OrderNotFoundError, OrderValidationError
from .ports import OrderRepository, PaymentGateway


def audit(func):
    # Intentionally simple. Module 4 will improve this.
    def wrapper(*args, **kwargs):
        print(f"[AUDIT] calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[AUDIT] completed {func.__name__}")
        return result

    return wrapper


class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        payment_gateway: PaymentGateway,
    ) -> None:
        self.repository = repository
        self.payment_gateway = payment_gateway

    @audit
    def create_order(self, customer_id: str, amount: Decimal) -> Order:
        if not customer_id or not isinstance(customer_id, str):
            raise OrderValidationError("Invalid customer_id")

        if not isinstance(amount, Decimal) or amount <= 0:
            raise OrderValidationError("Invalid amount")

        order_id = str(uuid4())
        order = Order(id=order_id, customer_id=customer_id, amount=amount)

        try:
            self.payment_gateway.charge(customer_id, amount)
            self.repository.save(order)
        except Exception as exc:
            # Deliberately broad for now.
            # Module 3 will explain why this is an enterprise-code smell.
            raise OrderValidationError(f"Payment failed: {exc}")

        return order

    def get_order(self, order_id: str) -> Order:
        order = self.repository.find_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(order_id)

        return order
