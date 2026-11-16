"""Integration tests: Checkout wired to the real payment strategies, end to end."""

import io
import runpy
import unittest
from contextlib import redirect_stdout
from decimal import Decimal

from strategy_pattern.python.card_payment import CardPayment
from strategy_pattern.python.checkout import Checkout
from strategy_pattern.python.momo_payment import MoMoPayment
from strategy_pattern.python.payment import PaymentRequest, PaymentResponse, PaymentStrategy


def checkout_with(strategy: PaymentStrategy, request: PaymentRequest):
    """Run a full checkout. Returns (response, printed_lines)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        response = Checkout(strategy).checkout(request)
    return response, buffer.getvalue().splitlines()


class CheckoutIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.request = PaymentRequest(customer_id="123", amount=Decimal("100.00"), currency="USD")

    def test_card_checkout_end_to_end(self):
        response, lines = checkout_with(CardPayment(), self.request)

        self.assertTrue(response.success)
        self.assertEqual(response.transaction_id, "card123")
        self.assertEqual(lines, [
            "Validating Order...",
            "Processing card payment for customer 123 with amount 100.00 USD.",
            "Payment successful: Transaction ID card123",
        ])

    def test_momo_checkout_end_to_end(self):
        response, lines = checkout_with(MoMoPayment(), self.request)

        self.assertTrue(response.success)
        self.assertEqual(response.transaction_id, "momo123")
        self.assertEqual(lines, [
            "Validating Order...",
            "Processing MoMo payment for customer 123 with amount 100.00 USD.",
            "Payment successful: Transaction ID momo123",
        ])

    def test_same_request_different_strategies_give_different_results(self):
        card_response, _ = checkout_with(CardPayment(), self.request)
        momo_response, _ = checkout_with(MoMoPayment(), self.request)

        self.assertNotEqual(card_response.transaction_id, momo_response.transaction_id)

    def test_strategy_can_be_swapped_at_runtime(self):
        checkout = Checkout(CardPayment())
        with redirect_stdout(io.StringIO()):
            first = checkout.checkout(self.request)
            checkout.payment_strategy = MoMoPayment()
            second = checkout.checkout(self.request)

        self.assertEqual(first.transaction_id, "card123")
        self.assertEqual(second.transaction_id, "momo123")

    def test_new_strategy_works_without_changing_checkout(self):
        """Open/closed principle: a new payment method plugs straight into Checkout."""

        class DecliningPayment(PaymentStrategy):
            def pay(self, request: PaymentRequest) -> PaymentResponse:
                return PaymentResponse(transaction_id="bank001", success=False, message="Account closed")

        response, lines = checkout_with(DecliningPayment(), self.request)

        self.assertFalse(response.success)
        self.assertEqual(lines, ["Validating Order...", "Payment failed: Account closed"])


class MainScriptTest(unittest.TestCase):
    def test_main_runs_both_checkouts(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            runpy.run_module("strategy_pattern.python.main", run_name="__main__")

        self.assertEqual(buffer.getvalue().splitlines(), [
            "Validating Order...",
            "Processing card payment for customer 123 with amount 100.0 USD.",
            "Payment successful: Transaction ID card123",
            "Validating Order...",
            "Processing MoMo payment for customer 456 with amount 200.0 VND.",
            "Payment successful: Transaction ID momo123",
        ])


if __name__ == "__main__":
    unittest.main()
