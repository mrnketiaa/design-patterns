from strategy_pattern.python.payment import PaymentRequest, PaymentResponse, PaymentStrategy


class Checkout:
    def __init__(self, payment_strategy: PaymentStrategy):
        self.payment_strategy = payment_strategy

    def checkout(self, request: PaymentRequest) -> PaymentResponse:

        print("Validating Order...")

        result = self.payment_strategy.pay(request)

        if not result.success:
            print(f"Payment failed: {result.message}")
        else:
            print(f"Payment successful: Transaction ID {result.transaction_id}")
        
        return result