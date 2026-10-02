from decimal import Decimal

import pytest

from acme_orders.domain import OrderValidationError
from acme_orders.payment import FakePaymentGateway
from acme_orders.repository import InMemoryOrderRepository
from acme_orders.service import OrderService


@pytest.fixture
def service() -> OrderService:
    return OrderService(
        InMemoryOrderRepository(),
        FakePaymentGateway(),
    )


def test_create_order(service: OrderService) -> None:
    order = service.create_order("cust-1", Decimal("100"))
    assert order.customer_id == "cust-1"
    assert order.amount == Decimal("100")


def test_invalid_amount(service: OrderService) -> None:
    with pytest.raises(OrderValidationError):
        service.create_order("cust-1", Decimal("0"))


def test_get_missing_order(service: OrderService) -> None:
    with pytest.raises(LookupError):
        service.get_order("does-not-exist")
