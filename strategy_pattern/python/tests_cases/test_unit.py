"""Unit tests: each class tested on its own, with fakes in place of real strategies."""

import dataclasses
import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from unittest.mock import Mock

from strategy_pattern.python.card_payment import CardPayment
from strategy_pattern.python.checkout import Checkout
from strategy_pattern.python.momo_payment import MoMoPayment
from strategy_pattern.python.payment import PaymentRequest, PaymentResponse, PaymentStrategy


def make_request(**overrides) -> PaymentRequest:
    fields = {"customer_id": "123", "amount": Decimal("100.00"), "currency": "USD"}
    fields.update(overrides)
    return PaymentRequest(**fields)


def run_silently(func, *args):
    """Call func, capturing anything it prints. Returns (result, printed_text)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class PaymentRequestTest(unittest.TestCase):
    def test_stores_fields(self):
        request = make_request()
        self.assertEqual(request.customer_id, "123")
        self.assertEqual(request.amount, Decimal("100.00"))
        self.assertEqual(request.currency, "USD")

    def test_is_immutable(self):
        request = make_request()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            request.amount = Decimal("1.00") # type: ignore

    def test_equal_when_fields_equal(self):
        self.assertEqual(make_request(), make_request())
        self.assertNotEqual(make_request(), make_request(amount=Decimal("99.99")))


class PaymentResponseTest(unittest.TestCase):
    def test_message_defaults_to_empty(self):
        response = PaymentResponse(transaction_id="t1", success=True)
        self.assertEqual(response.message, "")

    def test_is_immutable(self):
        response = PaymentResponse(transaction_id="t1", success=True)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            response.success = False # type: ignore


class PaymentStrategyTest(unittest.TestCase):
    def test_cannot_instantiate_interface(self):
        with self.assertRaises(TypeError):
            PaymentStrategy() # type: ignore

    def test_subclass_without_pay_cannot_be_instantiated(self):
        class IncompletePayment(PaymentStrategy):
            pass

        with self.assertRaises(TypeError):
            IncompletePayment() # type: ignore

    def test_concrete_strategies_implement_interface(self):
        self.assertIsInstance(CardPayment(), PaymentStrategy)
        self.assertIsInstance(MoMoPayment(), PaymentStrategy)


class CardPaymentTest(unittest.TestCase):
    def test_returns_successful_response(self):
        response, _ = run_silently(CardPayment().pay, make_request())
        self.assertEqual(
            response,
            PaymentResponse(transaction_id="card123", success=True, message="Payment successful via Card."),
        )

    def test_prints_request_details(self):
        _, output = run_silently(CardPayment().pay, make_request())
        self.assertEqual(
            output,
            "Processing card payment for customer 123 with amount 100.00 USD.\n",
        )


class MoMoPaymentTest(unittest.TestCase):
    def test_returns_successful_response(self):
        response, _ = run_silently(MoMoPayment().pay, make_request())
        self.assertEqual(
            response,
            PaymentResponse(transaction_id="momo123", success=True, message="Payment successful via MoMo."),
        )

    def test_prints_request_details(self):
        request = make_request(customer_id="456", amount=Decimal("200"), currency="GHS")
        _, output = run_silently(MoMoPayment().pay, request)
        self.assertEqual(
            output,
            "Processing MoMo payment for customer 456 with amount 200 GHS.\n",
        )


class CheckoutTest(unittest.TestCase):
    def make_strategy(self, response: PaymentResponse) -> Mock:
        strategy = Mock(spec=PaymentStrategy)
        strategy.pay.return_value = response
        return strategy

    def test_passes_request_to_strategy(self):
        strategy = self.make_strategy(PaymentResponse("t1", True))
        request = make_request()

        run_silently(Checkout(strategy).checkout, request)

        strategy.pay.assert_called_once_with(request)

    def test_returns_strategy_response_unchanged(self):
        expected = PaymentResponse("t1", True, "ok")
        result, _ = run_silently(Checkout(self.make_strategy(expected)).checkout, make_request())
        self.assertIs(result, expected)

    def test_prints_success_message(self):
        strategy = self.make_strategy(PaymentResponse("t1", True))
        _, output = run_silently(Checkout(strategy).checkout, make_request())

        self.assertEqual(output, "Validating Order...\nPayment successful: Transaction ID t1\n")

    def test_prints_failure_message(self):
        strategy = self.make_strategy(PaymentResponse("t2", False, "Insufficient funds"))
        _, output = run_silently(Checkout(strategy).checkout, make_request())

        self.assertEqual(output, "Validating Order...\nPayment failed: Insufficient funds\n")

    def test_failure_does_not_print_success(self):
        strategy = self.make_strategy(PaymentResponse("t2", False, "Declined"))
        _, output = run_silently(Checkout(strategy).checkout, make_request())

        self.assertNotIn("successful", output)

    def test_returns_failed_response(self):
        failed = PaymentResponse("t2", False, "Declined")
        result, _ = run_silently(Checkout(self.make_strategy(failed)).checkout, make_request())
        self.assertFalse(result.success)


if __name__ == "__main__":
    unittest.main()
