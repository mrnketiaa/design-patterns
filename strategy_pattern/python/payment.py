from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PaymentRequest:
    customer_id: str
    amount: Decimal
    currency: str


@dataclass(frozen=True)
class PaymentResponse:
    transaction_id: str
    success: bool
    message: str = ""


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, request: PaymentRequest) -> PaymentResponse:
        """(Strategy) - pay method to be implemented by concrete payment strategies."""