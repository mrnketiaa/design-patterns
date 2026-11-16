import { formatAmount, type PaymentRequest, type PaymentResponse, type PaymentStrategy } from "./payment";

export class CardPayment implements PaymentStrategy {
  pay(request: PaymentRequest): PaymentResponse {
    console.log(
      `Processing card payment for customer ${request.customerId} with amount ${formatAmount(request.amountMinor, request.currency)}.`,
    );

    return { transactionId: "card123", success: true, message: "Payment successful via Card." };
  }
}
