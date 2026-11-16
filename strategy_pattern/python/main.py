from decimal import Decimal

from strategy_pattern.python.card_payment import CardPayment
from strategy_pattern.python.checkout import Checkout
from strategy_pattern.python.momo_payment import MoMoPayment
from strategy_pattern.python.payment import PaymentRequest




if __name__ == "__main__":
    # Example usage
    card_payment = CardPayment()
    momo_payment = MoMoPayment()

    checkout_card = Checkout(card_payment)
    checkout_momo = Checkout(momo_payment)

    request_card = PaymentRequest(customer_id="123", amount=Decimal("100.0"), currency="USD")
    request_momo = PaymentRequest(customer_id="456", amount=Decimal("200.0"), currency="VND")

    checkout_card.checkout(request_card)
    checkout_momo.checkout(request_momo)
    