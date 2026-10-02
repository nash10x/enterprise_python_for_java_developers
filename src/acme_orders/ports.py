from typing import Protocol

from .domain import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def find_by_id(self, order_id: str) -> Order | None: ...


class PaymentGateway(Protocol):
    def charge(self, customer_id: str, amount: object) -> str: ...
