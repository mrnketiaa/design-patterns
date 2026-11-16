from strategy_pattern.python.payment import PaymentRequest, PaymentResponse, PaymentStrategy


class MoMoPayment(PaymentStrategy):
     def pay(self, request: PaymentRequest) -> PaymentResponse:

        print(f"Processing MoMo payment for customer {request.customer_id} with amount {request.amount} {request.currency}.")
         
        return PaymentResponse(transaction_id="momo123", success=True, message="Payment successful via MoMo.")