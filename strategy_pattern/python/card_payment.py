from strategy_pattern.python.payment import PaymentRequest, PaymentResponse, PaymentStrategy


class CardPayment(PaymentStrategy):
     def pay(self, request: PaymentRequest) -> PaymentResponse:
         
         print(f"Processing card payment for customer {request.customer_id} with amount {request.amount} {request.currency}.")
         
         return PaymentResponse(transaction_id="card123", success=True, message="Payment successful via Card.")