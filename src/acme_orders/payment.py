from decimal import Decimal


class FakePaymentGateway:
    def charge(self, customer_id: str, amount: Decimal) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return f"payment-for-{customer_id}"
